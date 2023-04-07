from django.contrib import admin

from .models import MoviePost, Platform, Genre, Language, Certificate, \
    MovieToPhoto, CastDetail, CriticReviewDetail, Award, MovieToAward, MovieToCertificate, \
    MovieToLanguage, MovieToLabel, MovieToGenre, Label, MovieCollection, MovieCollectionDetail, \
    MovieToPlatform, Report, MovieToTrailer, UserReviewDetail

# Movie Section
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


class MoviePostAdmin(admin.ModelAdmin):
    list_display = ['movie_name', 'release_date', 'actors_display_comma_separated']
    prepopulated_fields = {'slug': ('movie_name', 'release_date')}


admin.site.register(MoviePost, MoviePostAdmin)


class ColectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


class ColectionDetailsAdmin(admin.ModelAdmin):
    list_display = ['movie_name', 'release_date', 'genres']
    prepopulated_fields = {'slug': ('movie_name', 'release_date')}


class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


admin.site.register(MovieCollectionDetail, ColectionDetailsAdmin)
admin.site.register(MovieCollection, ColectionAdmin)
admin.site.register(Report, ReportAdmin)

