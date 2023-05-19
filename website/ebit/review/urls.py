from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/v1/collections/', views.all_collections, name='collections'),
    path('api/v1/collections/<slug:slug>/', views.collection_details, name='collection_details'),
    path('api/v1/moods/', views.all_moods, name='movie-moods'),
    path('api/v1/genres/', views.all_genres, name='movie-genres'),
    path('api/v1/platforms/', views.all_platforms, name='movie-platforms'),
    path('api/v1/awards/', views.all_awards, name='movie-awards'),
    path('api/v1/labels/', views.all_labels, name='movie-labels'),
    path('api/v1/certificates/', views.all_certificates, name='all_certificates'),
    path('api/v1/languages/', views.all_languages, name='all_languages'),
    path('api/v1/movies/', csrf_exempt(views.movies), name='movies'),
    path('api/v1/movies/<slug:slug>/', csrf_exempt(views.movie_details), name='movie_details'),
    path('api/v1/similarbygenres/<slug:slug>/', csrf_exempt(views.similar_by_genres), name='similar_by_genres'),
    path('api/v1/addusercomment/', csrf_exempt(views.add_user_comment), name='add_user_comment'),
    path('api/v1/addusercommentlikes/', csrf_exempt(views.add_likes), name='add_user_comment_likes'),
    path('api/v1/addusercommentdislikes/', csrf_exempt(views.add_dislikes), name='add_user_comment_dislikes'),
    path('api/v1/reports/', views.all_reports, name='all_reports'),
    path('api/v1/reports/<slug:slug>/', views.report_details, name='report_details'),
    path('api/v1/search/', views.search, name='search'),


    # Podcasts Section
    path('api/v1/podcasts/collections/', PodcastsViews.all_collections, name='p-collections'),
    path('api/v1/podcasts/collections/<slug:slug>/', PodcastsViews.collection_details, name='p-collection_details'),
    path('api/v1/podcasts/moods/', PodcastsViews.all_moods, name='podcasts-moods'),
    path('api/v1/podcasts/genres/', PodcastsViews.all_genres, name='podcasts-genres'),
    path('api/v1/podcasts/platforms/', PodcastsViews.all_platforms, name='podcasts-platforms'),
    path('api/v1/podcasts/awards/', PodcastsViews.all_awards, name='podcasts-awards'),
    path('api/v1/podcasts/labels/', PodcastsViews.all_labels, name='podcasts-labels'),
    path('api/v1/podcasts/certificates/', PodcastsViews.all_certificates, name='podcasts-all_certificates'),
    path('api/v1/podcasts/languages/', PodcastsViews.all_languages, name='podcasts-all_languages'),

    path('api/v1/podcasts/similarbygenres/<slug:slug>/', csrf_exempt(PodcastsViews.similar_by_genres), name='podcasts-similar_by_genres'),

    path('api/v1/podcasts/addusercomment/', csrf_exempt(PodcastsViews.add_user_comment), name='podcasts-add_user_comment'),
    path('api/v1/podcasts/addusercommentlikes/', csrf_exempt(PodcastsViews.add_likes), name='add_user_comment_likes'),
    path('api/v1/podcasts/addusercommentdislikes/', csrf_exempt(PodcastsViews.add_dislikes), name='add_user_comment_dislikes'),
    # Podcasts report section
    path('api/v1/podcasts/reports/', PodcastsViews.all_reports, name='podcasts-all_reports'),
    path('api/v1/podcasts/reports/<slug:slug>/', PodcastsViews.report_details, name='podcasts-report_details'),
    path('api/v1/podcasts/search/', PodcastsViews.search, name='search'),
    # Below two should always be at the end of the podcast list of urls
    path('api/v1/podcasts/', csrf_exempt(PodcastsViews.podcasts), name='podcasts'),
    path('api/v1/podcasts/<slug:slug>/', csrf_exempt(PodcastsViews.podcast_details), name='podcasts_details'),


    # Books Section
    path('api/v1/books/collections/', BooksViews.all_collections, name='b-collections'),
    path('api/v1/books/collections/<slug:slug>/', BooksViews.collection_details, name='b-collection_details'),
    path('api/v1/books/moods/', BooksViews.all_moods, name='books-moods'),
    path('api/v1/books/genres/', BooksViews.all_genres, name='books-genres'),
    path('api/v1/books/platforms/', BooksViews.all_platforms, name='books-platforms'),
    path('api/v1/books/awards/', BooksViews.all_awards, name='books-awards'),
    path('api/v1/books/labels/', BooksViews.all_labels, name='books-labels'),
    path('api/v1/books/certificates/', BooksViews.all_certificates, name='books-all_certificates'),
    path('api/v1/books/languages/', BooksViews.all_languages, name='books-all_languages'),

    path('api/v1/books/similarbygenres/<slug:slug>/', csrf_exempt(BooksViews.similar_by_genres), name='books-similar_by_genres'),

    path('api/v1/books/addusercomment/', csrf_exempt(BooksViews.add_user_comment), name='books-add_user_comment'),
    path('api/v1/books/addusercommentlikes/', csrf_exempt(BooksViews.add_likes), name='add_user_comment_likes'),
    path('api/v1/books/addusercommentdislikes/', csrf_exempt(BooksViews.add_dislikes), name='add_user_comment_dislikes'),
    # Books report section
    path('api/v1/books/reports/', BooksViews.all_reports, name='books-all_reports'),
    path('api/v1/books/reports/<slug:slug>/', BooksViews.report_details, name='books-report_details'),
    # Below two should always be at the end of the book list of urls
    path('api/v1/books/', csrf_exempt(BooksViews.books), name='books'),
    path('api/v1/books/<slug:slug>/', csrf_exempt(BooksViews.book_details), name='books_details'),

    path('', views.index, name='index'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

