from django.contrib import admin

from .models import MoviePost, Platform, Genre, Language, Certificate, \
    MoviePostDetail, MovieToPhoto, CastDetail, CriticReviewDetail, Award, MovieToAward, MovieToCertificate, \
    MovieToLanguage, MovieToLabel, MovieToGenre, Label

admin.site.register(MoviePost)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(MovieToGenre)
admin.site.register(Language)
admin.site.register(Certificate)
admin.site.register(MoviePostDetail)
admin.site.register(MovieToPhoto)
admin.site.register(CastDetail)
admin.site.register(CriticReviewDetail)
admin.site.register(Award)
admin.site.register(MovieToAward)
admin.site.register(MovieToCertificate)
admin.site.register(MovieToLanguage)
admin.site.register(MovieToLabel)
admin.site.register(Label)

