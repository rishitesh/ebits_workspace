from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from . import views

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
    path('api/v1/similarbygenres/<slug:movie_id>/', csrf_exempt(views.similar_by_genres), name='similar_by_genres'),

    path('api/v1/addusercomment/', csrf_exempt(views.add_user_comment), name='add_user_comment'),
    # Reports Section
    path('api/v1/reports/', views.all_reports, name='all_reports'),
    path('api/v1/reports/<slug:slug>/', views.report_details, name='report_details'),
    path('', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

