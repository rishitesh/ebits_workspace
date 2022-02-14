from django.db import models
import uuid


class MoviePost(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    movie_name = models.TextField()
    release_date = models.DateField()
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()
    ebits_rating = models.FloatField()
    thumbnail_image = models.ImageField(default=None, null=True, upload_to='upload/')

    def __str__(self):
        return "%s->%s" % (self.id, self.movie_name)


class CastDetail(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    cast_name = models.TextField()
    cast_role = models.TextField()
    cast_image = models.ImageField(default=None, null=True, upload_to='upload/')

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


class Award(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToAward(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    award_name = models.ForeignKey(Award, on_delete=models.CASCADE)

    def __str__(self):
        return "%s->%s" % (self.movie_id, self.award_name)


class Certificate(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToCertificate(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    certificate_id = models.ForeignKey(Certificate, on_delete=models.CASCADE)


class Language(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return "%s" % self.name


class MovieToLanguage(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)


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


class MoviePostDetail(models.Model):
    movie_id = models.ForeignKey(MoviePost, on_delete=models.CASCADE)
    ebits_review = models.TextField()

    def __str__(self):
        return "%s" % self.movie_id


