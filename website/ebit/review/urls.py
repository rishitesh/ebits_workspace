from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('movie-genres/', views.all_genres, name='movie-genres'),
    path('api/v1/collections/', views.all_collections, name='collections'),
    path('api/v1/collections/<slug:collection_id>/', views.collection_details, name='collection_details'),
    # path('movie-moods/', views.all_moods, name='movie-moods'),
    # path('movie-by-label/', views.movie_by_label, name='movie-by-label'),
    # path('movie-by-label-genre/', views.movie_by_label_genre, name='movie-by-label-genre'),
    # path('movie-details', views.movie_details, name='movie_details'),
    path('api/v1/movies/', csrf_exempt(views.movies), name='movies'),
    path('', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)