from django.contrib import admin

from .models import MoviePost, Platform, Genre, Language, Certificate,\
    MoviePostDetails, MovieToPhotos, CastDetails, CriticReviewDetails, Awards, MovieToAwards, MovieToCertificate,\
    MovieToLanguage, MovieToLabel

admin.site.register(MoviePost)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Certificate)
admin.site.register(MoviePostDetails)
admin.site.register(MovieToPhotos)
admin.site.register(CastDetails)
admin.site.register(CriticReviewDetails)
admin.site.register(Awards)
admin.site.register(MovieToAwards)
admin.site.register(MovieToCertificate)
admin.site.register(MovieToLanguage)
admin.site.register(MovieToLabel)


