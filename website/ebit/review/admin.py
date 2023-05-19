from django.contrib import admin

from .booksModels import BookLabel, BookToLabel, AuthorDetail, BCriticReviewDetail, BookAward, BookToAward, \
    BCertificate, BookToCertificate, BLanguage, BookToLanguage, BPlatform, BookToPlatform, BGenre, BookToGenre, \
    BookToTrailer, BookToPhoto, BPhotoType, BUserReviewDetail, BookPost, BookCollectionDetail, BookCollection, BReport, \
    PublisherDetail

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


class BUserReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_id', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('book_id', 'review_author', 'review_title')}


admin.site.register(BUserReviewDetail, BUserReviewDetailAdmin)


class CriticReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'publication_name', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('publication_name', 'review_author', 'review_title')}


admin.site.register(CriticReviewDetail, CriticReviewDetailAdmin)


class PCriticReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'publication_name', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('publication_name', 'review_author', 'review_title')}


admin.site.register(PCriticReviewDetail, PCriticReviewDetailAdmin)


class BCriticReviewDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'publication_name', 'review_author', 'review_title']
    prepopulated_fields = {'slug': ('publication_name', 'review_author', 'review_title')}


admin.site.register(BCriticReviewDetail, BCriticReviewDetailAdmin)


#Podcasts Section
admin.site.register(PodcastLabel)
admin.site.register(PodcastToLabel)
admin.site.register(PodcasterDetail)
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


#Books Section
admin.site.register(BookLabel)
admin.site.register(BookToLabel)
admin.site.register(AuthorDetail)
admin.site.register(PublisherDetail)
admin.site.register(BookAward)
admin.site.register(BookToAward)
admin.site.register(BCertificate)
admin.site.register(BookToCertificate)
admin.site.register(BLanguage)
admin.site.register(BookToLanguage)
admin.site.register(BPlatform)
admin.site.register(BookToPlatform)
admin.site.register(BGenre)
admin.site.register(BookToGenre)
admin.site.register(BookToTrailer)
admin.site.register(BookToPhoto)
admin.site.register(BPhotoType)


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


class BookPostAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'publish_date', 'author']
    prepopulated_fields = {'slug': ('book_title', 'publish_date')}


admin.site.register(BookPost, BookPostAdmin)


class BCollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date']
    prepopulated_fields = {'slug': ('title', 'publish_date')}


class BCollectionDetailsAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'publish_date', 'genres']
    prepopulated_fields = {'slug': ('book_name', 'publish_date')}


class BReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'publish_date']
    prepopulated_fields = {'slug': ('name', 'publish_date')}


admin.site.register(BookCollectionDetail, BCollectionDetailsAdmin)
admin.site.register(BookCollection, BCollectionAdmin)
admin.site.register(BReport, BReportAdmin)