import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class PodcastPost(models.Model):
    id = models.AutoField(primary_key=True)

    podcast_name = models.CharField(max_length=120)
    release_date = models.DateField()
    slug = models.SlugField(null=True, unique=True)

    description = models.TextField(default=None, null=True, blank=True)
    isSeries = models.BooleanField(default=False)
    episodes = models.IntegerField()

    # Sentimeter
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()

    # Overview

    duration = models.FloatField(default=2.0)
    podcaster_display_comma_separated = models.CharField(max_length=200, default=None, null=True, blank=True)

    # Ratings & Review
    ebits_rating = models.FloatField()
    ebits_review = models.TextField(default=None, null=True, blank=True)
    ebits_reviewer_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    ebits_reviewer_image = models.CharField(null=True, blank=True, max_length=300)
    critics_rating = models.FloatField(default=None, null=True, blank=True)

    # Aspects -
    # Introduction
    # Content
    # Audio quality
    # Voices
    # Outro
    aspect_introduction = models.FloatField(default=None, null=True, blank=True)
    aspect_content = models.FloatField(default=None, null=True, blank=True)
    aspect_audioQuality = models.FloatField(default=None, null=True, blank=True)
    aspect_voices = models.FloatField(default=None, null=True, blank=True)
    aspect_outro = models.FloatField(default=None, null=True, blank=True)

    # Images
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)
    potrait_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.podcast_name)

    def get_absolute_url(self):
        return reverse("podcasts_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.podcast_name, self.release_date)
        super(PodcastPost, self).save(*args, **kwargs)


class PodcastCollection(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.TextField()
    description = models.TextField()
    image_url = models.CharField(null=True, blank=True, max_length=300)
    home_collection_banner_image = models.CharField(null=True, blank=True, max_length=300)

    is_report = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.publish_date)
        super(PodcastCollection, self).save(*args, **kwargs)



class PPlatform(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    platform_url = models.CharField(primary_key=False, max_length=200)
    image_url = models.CharField(primary_key=False, max_length=200)

    def __str__(self):
        return "%s" % self.name



class PodcastCollectionDetail(models.Model):
    id = models.AutoField(primary_key=True)
    collection_id = models.ForeignKey(PodcastCollection, on_delete=models.CASCADE)
    platform = models.ForeignKey(PPlatform, on_delete=models.CASCADE, default=None, null=True, blank=True)

    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    podcast_name = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()

    slug = models.SlugField(null=True, unique=True)

    # Sentimeter
    positive = models.IntegerField(default=None, null=True, blank=True)
    negative = models.IntegerField(default=None, null=True, blank=True)
    neutral = models.IntegerField(default=None, null=True, blank=True)

    aspect_introduction = models.FloatField(default=None, null=True, blank=True)
    aspect_content = models.FloatField(default=None, null=True, blank=True)
    aspect_audioQuality = models.FloatField(default=None, null=True, blank=True)
    aspect_voices = models.FloatField(default=None, null=True, blank=True)
    aspect_outro = models.FloatField(default=None, null=True, blank=True)
    genres = models.CharField(max_length=150, default=None, null=True, blank=True)
    ebits_rating = models.FloatField()
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.podcast_name)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.release_date)
        super(PodcastCollectionDetail, self).save(*args, **kwargs)


class PodcasterDetail(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    podcaster_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.podcaster_name)


class PCriticReviewDetail(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    publication_name = models.TextField()
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    critic_review = models.TextField()


    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse("CriticReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.podcast_id, self.publication_name, self.review_author, self.review_title)



class PUserReviewDetail(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    review_time = models.DateTimeField(default=datetime.now, blank=True)
    review_text = models.TextField()
    review_approved = models.BooleanField(default=False)
    review_likes = models.IntegerField(default=None, null=True, blank=True)
    review_dislikes = models.IntegerField(default=None, null=True, blank=True)
    reviewer_image_url = models.CharField(null=True, blank=True, max_length=300)

    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse("UserReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.podcast_id, self.review_author, self.review_date, self.review_approved)


class PodcastAward(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class PodcastToAward(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    award_name = models.ForeignKey(PodcastAward, on_delete=models.CASCADE)
    award_for = models.CharField(max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.award_name)


class PCertificate(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=300, default=None, null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class PodcastToCertificate(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    certificate_id = models.ForeignKey(PCertificate, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.certificate_id)


class PLanguage(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class PodcastToLanguage(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    language_id = models.ForeignKey(PLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.language_id)



class PodcastToPlatform(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    platform = models.ForeignKey(PPlatform, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.platform)


class PGenre(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class PodcastToGenre(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    genre = models.ForeignKey(PGenre, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.genre)


class PodcastLabel(models.Model):
    name = models.CharField(primary_key=True, max_length=150)
    type = models.CharField(default='general', max_length=150)
    photo_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s" % self.name


class PodcastToLabel(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    label = models.ForeignKey(PodcastLabel, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.label)


class PodcastToTrailer(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    trailers_url = models.CharField(max_length=200)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.trailers_url)


class PPhotoType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)


class PodcastToPhoto(models.Model):
    podcast_id = models.ForeignKey(PodcastPost, on_delete=models.CASCADE)
    photo_type = models.ForeignKey(PPhotoType, on_delete=models.CASCADE)
    photo_url = models.CharField(null=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.podcast_id, self.photo_url)


class PReport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    publish_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    collection_id = models.ForeignKey(PodcastCollection, on_delete=models.CASCADE, default=None, blank=True, null=True)
    chart_data_json = models.JSONField(default=None, null=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.collection_id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.publish_date)
        super(PReport, self).save(*args, **kwargs)




