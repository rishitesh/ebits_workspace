import uuid
from datetime import datetime

from django.db import models


class MovieCollection(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, help_text='Unique ID for this particular item')
    name = models.TextField()
    description = models.TextField()
    bgImage = models.ImageField(default=None, null=True, upload_to='upload/')
    is_report = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.now)

    def __str__(self):
        return "%s->%s" % (self.id, self.name)


class MoviePost(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    movie_name = models.CharField(max_length=120)
    description = models.TextField(default=None, null=True, blank=True)

    # Sentimeter
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()

    # Overview
    release_date = models.DateField()
    duration = models.FloatField(default=2.0)
    actors_display_comma_separated = models.CharField(max_length=200, default=None, null=True, blank=True)
    directors_display_comma_separated = models.CharField(max_length=200, default=None, null=True, blank=True)

    # Ratings & Review
    ebits_rating = models.FloatField()
    ebits_review = models.TextField(default=None, null=True, blank=True)
    ebits_reviewer_name = models.CharField(max_length=100, default=None, null=True, blank=True)
    ebits_reviewer_image = models.ImageField(default=None, null=True, blank=True, upload_to='upload/')
    critics_rating = models.FloatField(default=None, null=True, blank=True)

    # Aspects
    aspect_story = models.FloatField(default=None, null=True, blank=True)
    aspect_direction = models.FloatField(default=None, null=True, blank=True)
    aspect_music = models.FloatField(default=None, null=True, blank=True)
    aspect_performance = models.FloatField(default=None, null=True, blank=True)
    aspect_costume = models.FloatField(default=None, null=True, blank=True)
    aspect_screenplay = models.FloatField(default=None, null=True, blank=True)
    aspect_vxf = models.FloatField(default=None, null=True, blank=True)

    # Images
    thumbnail_image = models.ImageField(default=None, null=True, upload_to='upload/')
    potrait_image = models.ImageField(default=None, null=True,blank=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s" % (self.id, self.movie_name)


class MovieCollectionDetail(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, help_text='Unique ID for this particular item')
    collection_id = models.ForeignKey(MovieCollection, on_delete=models.CASCADE)

    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE, default=None, blank=True, null=True)
    movie_name = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    aspect_story = models.FloatField(default=None, null=True, blank=True)
    aspect_direction = models.FloatField(default=None, null=True, blank=True)
    aspect_music = models.FloatField(default=None, null=True, blank=True)
    aspect_performance = models.FloatField(default=None, null=True, blank=True)
    aspect_costume = models.FloatField(default=None, null=True, blank=True)
    aspect_screenplay = models.FloatField(default=None, null=True, blank=True)
    aspect_vxf = models.FloatField(default=None, null=True, blank=True)
    genres = models.CharField(max_length=150, default=None, null=True, blank=True)
    ebits_rating = models.FloatField()
    thumbnail_image = models.ImageField(default=None, null=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s" % (self.id, self.movie_name)


class CastDetail(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    cast_name = models.TextField()
    cast_role = models.TextField(default=None, null=True, blank=True)
    director = models.BooleanField(default=False)
    music_director = models.BooleanField(default=False)
    lyricist = models.BooleanField(default=False)
    choreographer = models.BooleanField(default=False)
    costume_director = models.BooleanField(default=False)
    producer = models.BooleanField(default=False)
    cinematographer = models.BooleanField(default=False)
    cast_image = models.ImageField(default=None, null=True, blank=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.cast_name)


class CriticReviewDetail(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    publication_name = models.TextField()
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    critic_review = models.TextField()

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.publication_name)


class UserReviewDetail(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    review_author = models.TextField()
    review_rating = models.FloatField()
    review_title = models.TextField()
    review_date = models.DateField()
    review_text = models.TextField()
    review_approved = models.BooleanField(default=False)
    reviewer_image = models.ImageField(default=None, null=True, blank=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s->%s->%s" % (self.movie_id, self.review_author, self.review_date, self.review_approved)


class Award(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToAward(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    award_name = models.ForeignKey(Award, on_delete=models.CASCADE)
    award_for = models.CharField(max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.award_name)


class Certificate(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToCertificate(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    certificate_id = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.certificate_id)


class Language(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToLanguage(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.language_id)


class Platform(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToPlatform(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.platform)


class Genre(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToGenre(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.genre)


class Label(models.Model):
    name = models.TextField(primary_key=True)
    type = models.TextField(default='general')
    photo = models.ImageField(default=None, null=True, upload_to='upload/')

    def __str__(self):
        return "%s" % self.name


class MovieToLabel(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.label)


class MovieToTrailer(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    trailers = models.TextField()

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.trailers)


class MovieToPhoto(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    photo = models.ImageField(default=None, null=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.photo)


class Report(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, help_text='Unique ID for this particular item')
    collection_id = models.ForeignKey(MovieCollection, on_delete=models.CASCADE, default=None, blank=True,
                                             null=True)
    chart_data_json = models.TextField(default=None, null=True)

    def __str__(self):
        return "%s->%s" % (self.id, self.collection_id)
