from django.contrib import admin

from .models import MoviePost, Platform, Genre, Language, Certificate, \
    MovieToPhoto, CastDetail, CriticReviewDetail, Award, MovieToAward, MovieToCertificate, \
    MovieToLanguage, MovieToLabel, MovieToGenre, Label, MovieCollection, MovieCollectionDetail, \
    MovieToPlatform, Report, MovieToTrailer, UserReviewDetail, PhotoType

from .podcastsModels import PodcastPost, PodcastLabel, PodcastToLabel, PodcasterDetail, PCriticReviewDetail, \
    PUserReviewDetail, PodcastAward, PodcastToAward, PCertificate, PodcastToCertificate, PLanguage, \
    PodcastToLanguage, PPlatform, PodcastToPlatform, PGenre, PodcastToGenre, PodcastToTrailer, \
    PodcastToPhoto, PodcastCollectionDetail, PodcastCollection, PReport, PPhotoType

# Movie Section
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(MovieToGenre)
admin.site.register(Language)
admin.site.register(Certificate)
admin.site.register(MovieToPhoto)
admin.site.register(CastDetail)
admin.site.register(Award)
admin.site.register(MovieToAward)
admin.site.register(MovieToCertificate)
admin.site.register(MovieToLanguage)
admin.site.register(MovieToLabel)
admin.site.register(Label)
admin.site.register(MovieToPlatform)
admin.site.register(MovieToTrailer)
admin.site.register(PhotoType)


class UserReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_id', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('movie_id', 'review_author', 'review_title')}


admin.site.register(UserReviewDetail, UserReviewDetailAdmin)


class PUserReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'podcast_id', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('podcast_id', 'review_author', 'review_title')}


admin.site.register(PUserReviewDetail, PUserReviewDetailAdmin)


class CriticReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'publication_name', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('publication_name', 'review_author', 'review_title')}


admin.site.register(CriticReviewDetail, CriticReviewDetailAdmin)

#Podcasts Section
admin.site.register(PodcastLabel)
admin.site.register(PodcastToLabel)
admin.site.register(PodcasterDetail)
admin.site.register(PCriticReviewDetail)
admin.site.register(PodcastAward)
admin.site.register(PodcastToAward)
admin.site.register(PCertificate)
admin.site.register(PodcastToCertificate)
admin.site.register(PLanguage)
admin.site.register(PodcastToLanguage)
admin.site.register(PPlatform)
admin.site.register(PodcastToPlatform)
admin.site.register(PGenre)
admin.site.register(PodcastToGenre)
admin.site.register(PodcastToTrailer)
admin.site.register(PodcastToPhoto)
admin.site.register(PPhotoType)


class MoviePostAdmin(admin.ModelAdmin):
    list_display = ['movie_name', 'release_date', 'actors_display_comma_separated']
    prepopulated_fields = {'slug': ('movie_name', 'release_date')}


admin.site.register(MoviePost, MoviePostAdmin)


class ColectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


class ColectionDetailsAdmin(admin.ModelAdmin):
    list_display = ['collection_id', 'movie_name', 'release_date', 'genres']
    prepopulated_fields = {'slug': ('movie_name', 'release_date')}


class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


admin.site.register(MovieCollectionDetail, ColectionDetailsAdmin)
admin.site.register(MovieCollection, ColectionAdmin)
admin.site.register(Report, ReportAdmin)


class PodcastPostAdmin(admin.ModelAdmin):
    list_display = ['podcast_name', 'release_date', 'podcaster_display_comma_separated']
    prepopulated_fields = {'slug': ('podcast_name', 'release_date')}


admin.site.register(PodcastPost, PodcastPostAdmin)


class PCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


class PCollectionDetailsAdmin(admin.ModelAdmin):
    list_display = ['podcast_name', 'release_date', 'genres']
    prepopulated_fields = {'slug': ('podcast_name', 'release_date')}


class PReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


admin.site.register(PodcastCollectionDetail, PCollectionDetailsAdmin)
admin.site.register(PodcastCollection, PCollectionAdmin)
admin.site.register(PReport, PReportAdmin)
