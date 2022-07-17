from django.contrib import admin

from .models import MoviePost, Platform, Genre, Language, Certificate, \
    MovieToPhoto, CastDetail, CriticReviewDetail, Award, MovieToAward, MovieToCertificate, \
    MovieToLanguage, MovieToLabel, MovieToGenre, Label, MovieCollection, MovieCollectionDetail, \
    MovieToPlatform, Report, MovieToTrailer, UserReviewDetail

# Movie Section
admin.site.register(MoviePost)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(MovieToGenre)
admin.site.register(Language)
admin.site.register(Certificate)
admin.site.register(MovieToPhoto)
admin.site.register(CastDetail)
admin.site.register(CriticReviewDetail)
admin.site.register(Award)
admin.site.register(MovieToAward)
admin.site.register(MovieToCertificate)
admin.site.register(MovieToLanguage)
admin.site.register(MovieToLabel)
admin.site.register(Label)
admin.site.register(MovieToPlatform)
admin.site.register(MovieToTrailer)
admin.site.register(UserReviewDetail)

# Collection Section
admin.site.register(MovieCollection)
admin.site.register(MovieCollectionDetail)

# Chart Section
admin.site.register(Report)


