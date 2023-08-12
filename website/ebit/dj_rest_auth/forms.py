
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from .app_settings import api_settings
from allauth.account.models import EmailConfirmationHMAC


if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import ResetPasswordForm as DefaultPasswordResetForm
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (
        filter_users_by_email,
        user_pk_to_url_str,
        user_username,
    )
    from allauth.utils import build_absolute_uri


class AllAuthPasswordResetForm(DefaultPasswordResetForm):
    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        if len(self.users) == 0:
            raise forms.ValidationError(
                ("The e-mail address is not assigned to any user account")
            )
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            from allauth.account.models import EmailAddress

            emailaddress = EmailAddress.objects.get_for_user(user, email)
            print(emailaddress)
            emailEmac = EmailConfirmationHMAC(emailaddress)
            key = emailEmac.key

            context = {
                'current_site': current_site,
                'user': user,
                'request': request,
                'key' : key
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']


class AllAuthPasswordResetConfirmForm(DefaultPasswordResetForm):

    user = None

    new_password = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        users = filter_users_by_email(email, is_active=True)
        if users and len(users) > 0:
            self.user = users[0]
        else:
            self.user = None

        return self.cleaned_data["email"]

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        password_validation.validate_password(password, self.user)
        return password

    def save(self, request, **kwargs):
        password = self.cleaned_data.get('new_password')
        self.user.set_password(password)
        self.user.save()
        return self.user



