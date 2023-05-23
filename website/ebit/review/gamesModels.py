import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class GamePost(models.Model):
    id = models.AutoField(primary_key=True)

    game_name = models.CharField(max_length=120)
    release_date = models.DateField()
    slug = models.SlugField(null=True, unique=True)

    description = models.TextField(default=None, null=True, blank=True)
    #isSeries = models.BooleanField(default=False)
    #episodes = models.IntegerField()

    # Sentimeter
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()

    # Overview

    # duration = models.FloatField(default=2.0)
    provider = models.CharField(max_length=200, default=None, null=True, blank=True)
    developer = models.CharField(max_length=200, default=None, null=True, blank=True)

    # Ratings & Review
    ebits_rating = models.FloatField()
    ebits_review = models.TextField(default=None, null=True, blank=True)
    ebits_reviewer_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    ebits_reviewer_image = models.CharField(null=True, blank=True, max_length=300)
    critics_rating = models.FloatField(default=None, null=True, blank=True)

    # Aspects -
    # Graphics, Performance, Ease of Use, Animation
    aspect_graphics = models.FloatField(default=None, null=True, blank=True)
    aspect_performance = models.FloatField(default=None, null=True, blank=True)
    aspect_easeOfUse = models.FloatField(default=None, null=True, blank=True)
    aspect_animation = models.FloatField(default=None, null=True, blank=True)
    #aspect_conflict = models.FloatField(default=None, null=True, blank=True)

    # Images
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)
    portrait_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.game_name)

    def get_absolute_url(self):
        return reverse("games_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.game_name, self.release_date)
        super(GamePost, self).save(*args, **kwargs)


class GameCollection(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.TextField()
    description = models.TextField()
    image_url = models.CharField(null=True, blank=True, max_length=300)
    is_report = models.BooleanField(default=False)
    release_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.release_date)
        super(GameCollection, self).save(*args, **kwargs)


class GameCollectionDetail(models.Model):
    id = models.AutoField(primary_key=True)
    collection_id = models.ForeignKey(GameCollection, on_delete=models.CASCADE)

    game_id = models.ForeignKey(GamePost, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    game_name = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    slug = models.SlugField(null=True, unique=True)

    # Sentimeter
    positive = models.IntegerField(default=None, null=True, blank=True)
    negative = models.IntegerField(default=None, null=True, blank=True)
    neutral = models.IntegerField(default=None, null=True, blank=True)

    #aspects - Graphics, Performance, Ease of Use, Animation
    aspect_graphics = models.FloatField(default=None, null=True, blank=True)
    aspect_performance = models.FloatField(default=None, null=True, blank=True)
    aspect_easeOfUse = models.FloatField(default=None, null=True, blank=True)
    aspect_animation = models.FloatField(default=None, null=True, blank=True)
    #aspect_conflict = models.FloatField(default=None, null=True, blank=True)
    genres = models.CharField(max_length=150, default=None, null=True, blank=True)
    ebits_rating = models.FloatField()
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.game_name)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.game_name, self.release_date)
        super(GameCollectionDetail, self).save(*args, **kwargs)


class DeveloperDetail(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    developer_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.developer_name)


class ProviderDetail(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.provider_name)


class GCriticReviewDetail(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    publication_name = models.TextField()
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    critic_review = models.TextField()
    review_likes = models.IntegerField(default=None, null=True, blank=True)
    review_dislikes = models.IntegerField(default=None, null=True, blank=True)

    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse("GCriticReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.game_id, self.publication_name, self.review_author, self.review_title)


class GUserReviewDetail(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    review_text = models.TextField()
    review_approved = models.BooleanField(default=False)
    review_likes = models.IntegerField(default=None, null=True, blank=True)
    review_dislikes = models.IntegerField(default=None, null=True, blank=True)
    reviewer_image_url = models.CharField(null=True, blank=True, max_length=300)

    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse("GUserReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.game_id, self.review_author, self.review_date, self.review_approved)


class GameAward(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class GameToAward(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    award_name = models.ForeignKey(GameAward, on_delete=models.CASCADE)
    award_for = models.CharField(max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.award_name)


class GCertificate(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=300, default=None, null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class GameToCertificate(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    certificate_id = models.ForeignKey(GCertificate, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.certificate_id)


class GLanguage(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class GameToLanguage(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    language_id = models.ForeignKey(GLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.language_id)


class GPlatform(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class GameToPlatform(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    platform = models.ForeignKey(GPlatform, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.platform)


class GGenre(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class GameToGenre(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    genre = models.ForeignKey(GGenre, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.genre)


class GameLabel(models.Model):
    name = models.CharField(primary_key=True, max_length=150)
    type = models.CharField(default='general', max_length=150)
    photo_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s" % self.name


class GameToLabel(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    label = models.ForeignKey(GameLabel, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.label)


class GameToTrailer(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    trailers_url = models.CharField(max_length=200)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.trailers_url)


class GPhotoType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)


class GameToPhoto(models.Model):
    game_id = models.ForeignKey(GamePost, on_delete=models.CASCADE)
    photo_type = models.ForeignKey(GPhotoType, on_delete=models.CASCADE)
    photo_url = models.CharField(null=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.game_id, self.photo_type, self.photo_url)


class GReport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    publish_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    collection_id = models.ForeignKey(GameCollection, on_delete=models.CASCADE, default=None, blank=True, null=True)
    chart_data_json = models.JSONField(default=None, null=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.collection_id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.publish_date)
        super(GReport, self).save(*args, **kwargs)

