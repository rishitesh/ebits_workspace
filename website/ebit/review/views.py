import json
from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.template import loader
from review.models import MoviePost, MovieToGenre, Genre
from review.serializers import MoviePostSerializer, GenreSerializer


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def all_genres(request):
    genres_serialized = GenreSerializer(Genre.objects.all(), many=True)
    all_genre = json.dumps(genres_serialized.data)
    return JsonResponse({'all_genres': all_genre})


def movie_by_label(request):
    genre = request.GET.get('genre')
    label = request.GET.get('label')
    print(genre)
    print(label)
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

