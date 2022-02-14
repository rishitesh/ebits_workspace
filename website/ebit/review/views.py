import json
from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.template import loader
from review.models import MoviePost, MovieToGenre, Genre, Label
from review.serializers import MoviePostSerializer, GenreSerializer, LabelSerializer


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def all_genres(request):
    genres_serialized = GenreSerializer(Genre.objects.all(), many=True)
    all_genre = json.dumps(genres_serialized.data)
    return JsonResponse({'all_genres': all_genre})


def all_moods(request):
    moods_serialized = LabelSerializer(
        Label.objects.raw("select name, photo from review_label where type = 'mood'"), many=True)
    every_moods = json.dumps(moods_serialized.data)
    return JsonResponse({'all_moods': every_moods})


def movie_by_label_genre(request):
    genre = request.GET.get('genre')
    label = request.GET.get('label')
    serializer = MoviePostSerializer(
        MoviePost.objects.raw(("""
                                  SELECT \
                                  review_moviepost.id, 
                                  movie_name, \
                                  release_date, \
                                  positive, \
                                  negative, \
                                  neutral, \
                                  ebits_rating, \
                                  thumbnail_image \
                                  FROM review_moviepost, review_movietogenre , review_movietolabel \
                                  where review_moviepost.id = review_movietogenre.movie_id_id \
                                  and review_moviepost.id = review_movietolabel.movie_id_id \
                                  and  genre_id = '%s'  
                                  and label_id = '%s' 
                                  """ % (genre, label)
                               )
                              )
        , many=True)

    movie_post_data = json.dumps(serializer.data)
    pprint(movie_post_data)
    return JsonResponse({'movie_list': movie_post_data})


def movie_by_label(request):
    label = request.GET.get('label')
    serializer = MoviePostSerializer(
        MoviePost.objects.raw(("""
                                  SELECT \
                                  review_moviepost.id, 
                                  movie_name, \
                                  release_date, \
                                  positive, \
                                  negative, \
                                  neutral, \
                                  ebits_rating, \
                                  thumbnail_image \
                                  FROM review_moviepost , review_movietolabel \
                                  where review_moviepost.id = review_movietolabel.movie_id_id \
                                  and label_id = '%s' 
                                  """ % (label)
                               )
                              )
        , many=True)

    movie_post_data = json.dumps(serializer.data)
    pprint(movie_post_data)
    return JsonResponse({'movie_list': movie_post_data})

