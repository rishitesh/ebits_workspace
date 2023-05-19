import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class BookPost(models.Model):
    id = models.AutoField(primary_key=True)

    book_title = models.CharField(max_length=120)
    publish_date = models.DateField()
    slug = models.SlugField(null=True, unique=True)

    synopsis = models.TextField(default=None, null=True, blank=True)
    isFiction = models.BooleanField(default=False)
    pages = models.IntegerField()

    # Sentimeter
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()

    # Overview

    #Pages = models.FloatField(default=2.0)
    publisher = models.CharField(max_length=200, default=None, null=True, blank=True)
    author = models.CharField(max_length=200, default=None, null=True, blank=True)

    # Ratings & Review
    ebits_rating = models.FloatField()
    ebits_review = models.TextField(default=None, null=True, blank=True)
    ebits_reviewer_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    ebits_reviewer_image = models.CharField(null=True, blank=True, max_length=300)
    critics_rating = models.FloatField(default=None, null=True, blank=True)

    # Aspects -
    # Fiction - plot, setting, characters, point of view, and conflict
    # Non-Fiction - Clear Premise, a solid takeaway,Consistent Structure, Style of writing, Visuals
    aspect_plot = models.FloatField(default=None, null=True, blank=True)
    aspect_setting = models.FloatField(default=None, null=True, blank=True)
    aspect_characters = models.FloatField(default=None, null=True, blank=True)
    aspect_pointOfView = models.FloatField(default=None, null=True, blank=True)
    aspect_conflict = models.FloatField(default=None, null=True, blank=True)
    aspect_premise = models.FloatField(default=None, null=True, blank=True)
    aspect_structure = models.FloatField(default=None, null=True, blank=True)
    aspect_styleOfWriting = models.FloatField(default=None, null=True, blank=True)
    aspect_visuals = models.FloatField(default=None, null=True, blank=True)
    aspect_takeaway = models.FloatField(default=None, null=True, blank=True)

    # Images
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)
    portrait_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.book_title)

    def get_absolute_url(self):
        return reverse("books_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.book_title, self.publish_date)
        super(BookPost, self).save(*args, **kwargs)


class BookCollection(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.TextField()
    synopsis = models.TextField()
    image_url = models.CharField(null=True, blank=True, max_length=300)
    is_report = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, self.publish_date)
        super(BookCollection, self).save(*args, **kwargs)


class BookCollectionDetail(models.Model):
    id = models.AutoField(primary_key=True)
    collection_id = models.ForeignKey(BookCollection, on_delete=models.CASCADE)

    book_id = models.ForeignKey(BookPost, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    book_name = models.CharField(max_length=100)
    synopsis = models.TextField()
    publish_date = models.DateField()
    publisher = models.CharField(max_length=200, default=None, null=True, blank=True)

    slug = models.SlugField(null=True, unique=True)

    # Sentimeter
    positive = models.IntegerField(default=None, null=True, blank=True)
    negative = models.IntegerField(default=None, null=True, blank=True)
    neutral = models.IntegerField(default=None, null=True, blank=True)

    #aspects - plot, setting, characters, point of view, and conflict
    #Clear Premise, a solid takeaway,Consistent Structure, Style of writing, Visuals
    aspect_plot = models.FloatField(default=None, null=True, blank=True)
    aspect_setting = models.FloatField(default=None, null=True, blank=True)
    aspect_characters = models.FloatField(default=None, null=True, blank=True)
    aspect_pointOfView = models.FloatField(default=None, null=True, blank=True)
    aspect_conflict = models.FloatField(default=None, null=True, blank=True)
    aspect_premise = models.FloatField(default=None, null=True, blank=True)
    aspect_structure = models.FloatField(default=None, null=True, blank=True)
    aspect_styleOfWriting = models.FloatField(default=None, null=True, blank=True)
    aspect_visuals = models.FloatField(default=None, null=True, blank=True)
    aspect_takeaway = models.FloatField(default=None, null=True, blank=True)
    genres = models.CharField(max_length=150, default=None, null=True, blank=True)
    ebits_rating = models.FloatField()
    thumbnail_image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.book_name)

    def get_absolute_url(self):
        return reverse("collection_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.book_name, self.publish_date)
        super(BookCollectionDetail, self).save(*args, **kwargs)


class AuthorDetail(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.author_name)


class PublisherDetail(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    publisher_name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.publisher_name)


class BCriticReviewDetail(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
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
        return reverse("BUserReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.book_id, self.publication_name, self.review_author, self.review_title)


class BUserReviewDetail(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
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
        return reverse("UserReviewDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return "%s->%s->%s->%s" % (self.book_id, self.review_author, self.review_date, self.review_approved)


class BookAward(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class BookToAward(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    award_name = models.ForeignKey(BookAward, on_delete=models.CASCADE)
    award_for = models.CharField(max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.award_name)


class BCertificate(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=300, default=None, null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class BookToCertificate(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    certificate_id = models.ForeignKey(BCertificate, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.certificate_id)


class BLanguage(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class BookToLanguage(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    language_id = models.ForeignKey(BLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.language_id)


class BPlatform(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class BookToPlatform(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    platform = models.ForeignKey(BPlatform, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.platform)


class BGenre(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return "%s" % self.name


class BookToGenre(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    genre = models.ForeignKey(BGenre, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.genre)


class BookLabel(models.Model):
    name = models.CharField(primary_key=True, max_length=150)
    type = models.CharField(default='general', max_length=150)
    photo_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s" % self.name


class BookToLabel(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    label = models.ForeignKey(BookLabel, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.label)


# book trailers??
class BookToTrailer(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    trailers_url = models.CharField(max_length=200)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.trailers_url)


class BPhotoType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)


class BookToPhoto(models.Model):
    book_id = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    photo_type = models.ForeignKey(BPhotoType, on_delete=models.CASCADE)
    photo_url = models.CharField(null=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.book_id, self.photo_type, self.photo_url)


class BReport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    publish_date = models.DateField(default=datetime.now)

    slug = models.SlugField(null=True, unique=True)

    collection_id = models.ForeignKey(BookCollection, on_delete=models.CASCADE, default=None, blank=True, null=True)
    chart_data_json = models.JSONField(default=None, null=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.collection_id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.publish_date)
        super(BReport, self).save(*args, **kwargs)

