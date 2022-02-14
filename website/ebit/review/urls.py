from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('movie-genres/', views.all_genres, name='movie-genres'),
    path('movie-moods/', views.all_moods, name='movie-moods'),
    path('movie-by-label/', views.movie_by_label, name='movie-by-label'),
    path('movie-by-label-genre/', views.movie_by_label_genre, name='movie-by-label-genre'),
    path('', views.index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)