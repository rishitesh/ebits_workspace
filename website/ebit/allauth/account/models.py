from datetime import datetime

from django.core import signing
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .. import app_settings as allauth_app_settings
from . import app_settings, signals
from .adapter import get_adapter
from .managers import EmailAddressManager, EmailConfirmationManager
from .utils import user_email
from pprint import pprint
import pyotp
import base64

class EmailAddress(models.Model):

    user = models.ForeignKey(
        allauth_app_settings.USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=app_settings.UNIQUE_EMAIL,
        max_length=app_settings.EMAIL_MAX_LENGTH,
        verbose_name=_("e-mail address"),
    )
    verified = models.BooleanField(verbose_name=_("verified"), default=False)
    primary = models.BooleanField(verbose_name=_("primary"), default=False)
    counter = models.IntegerField(default=0, blank=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        if not app_settings.UNIQUE_EMAIL:
            unique_together = [("user", "email")]

    def __str__(self):
        return self.email

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        user_email(self.user, self.email)
        if app_settings.USER_MODEL_EMAIL_FIELD:
            self.user.save(update_fields=[app_settings.USER_MODEL_EMAIL_FIELD])
        return True

    def send_confirmation(self, request=None, signup=False):
        if app_settings.EMAIL_CONFIRMATION_HMAC:
            confirmation = EmailConfirmationHMAC(self)
        else:
            confirmation = EmailConfirmation.create(self)
        confirmation.send(request, signup=signup)
        return confirmation

    def change(self, request, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            user_email(self.user, new_email)
            if app_settings.USER_MODEL_EMAIL_FIELD:
                self.user.save(update_fields=[app_settings.USER_MODEL_EMAIL_FIELD])
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation(request)


class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(
        EmailAddress,
        verbose_name=_("e-mail address"),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)
    sent = models.DateTimeField(verbose_name=_("sent"), null=True)
    key = models.CharField(verbose_name=_("key"), max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for %s" % self.email_address

    @classmethod
    def create(cls, email_address):
        key = get_adapter().generate_emailconfirmation_key(email_address.email)
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        )
        return expiration_date <= timezone.now()

    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            get_adapter(request).confirm_email(request, email_address)
            signals.email_confirmed.send(
                sender=self.__class__,
                request=request,
                email_address=email_address,
            )
            return email_address

    def send(self, request=None, signup=False):
        get_adapter(request).send_confirmation_mail(request, self, signup)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(
            sender=self.__class__,
            request=request,
            confirmation=self,
            signup=signup,
        )


class generateKey:
    @staticmethod
    def returnValue(email_address):
        return str(email_address) + str(datetime.date(datetime.now())) + "abracadabra"


class EmailConfirmationHMAC:
    def __init__(self, email_address):
        self.email_address = email_address

    @property
    def key(self):
        self.email_address.counter += 1  # Update Counter At every Call
        self.email_address.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(self.email_address.email).encode())  # Key is generated
        OTP = pyotp.HOTP(key)
        pprint(OTP.at(self.email_address.counter))
        return OTP.at(self.email_address.counter)

    @classmethod
    def from_key(cls, key, email_address):
        try:
            keygen = generateKey()
            encoded_key = base64.b32encode(keygen.returnValue(email_address).encode())  # Generating Key
            OTP = pyotp.HOTP(encoded_key)  # HOTP Model
            email = EmailAddress.objects.get(email=email_address, verified=False)
            email_address_obj = EmailConfirmationHMAC(email)
            if email and OTP.verify(key, email.counter):
                email.isVerified = True
                email.save()

        except (
            signing.SignatureExpired,
            signing.BadSignature,
            EmailAddress.DoesNotExist,
        ):
            email_address_obj = None
        return email_address_obj

    def confirm(self, request):
        if not self.email_address.verified:
            email_address = self.email_address
            get_adapter(request).confirm_email(request, email_address)
            signals.email_confirmed.send(
                sender=self.__class__,
                request=request,
                email_address=email_address,
            )
            return email_address

    def send(self, request=None, signup=False):
        pprint("Sending confirmation email")
        get_adapter(request).send_confirmation_mail(request, self, signup)
        signals.email_confirmation_sent.send(
            sender=self.__class__,
            request=request,
            confirmation=self,
            signup=signup,
        )
