from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from . import views, PodcastsViews

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
    # Podcasts report section
    path('api/v1/podcasts/reports/', PodcastsViews.all_reports, name='podcasts-all_reports'),
    path('api/v1/podcasts/reports/<slug:slug>/', PodcastsViews.report_details, name='podcasts-report_details'),
    # Below two should always be at the end of the podcast list of urls
    path('api/v1/podcasts/', csrf_exempt(PodcastsViews.podcasts), name='podcasts'),
    path('api/v1/podcasts/<slug:slug>/', csrf_exempt(PodcastsViews.podcast_details), name='podcasts_details'),

    path('', views.index, name='index'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

