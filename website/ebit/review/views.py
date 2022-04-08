import json
from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.models import Platform, Award
from review.serializers import *
from review.utils import format_uuid, is_empty, raw_sql, clean_json_dump


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def movie_details(request):
    template = loader.get_template('review/details.html')
    name = request.GET.get('name')
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
                                      FROM review_moviepost
                                      where movie_name = '%s' 
                                      """ % (name)
                               )
                              )
        , many=True)

    movie_post_data = json.dumps(serializer.data)
    pprint(movie_post_data)
    context = {
        'detail_json': movie_post_data,
    }
    return HttpResponse(template.render(context, request))


def all_moods(request):
    moods_serialized = LabelSerializer(
        Label.objects.raw("select name from review_label where LOWER(type) = 'mood'"), many=True)
    moods = json.dumps(moods_serialized.data)
    return JsonResponse({'moods': moods})


def all_labels(request):
    labels_serialized = LabelSerializer(
        Label.objects.raw("select name from review_label where LOWER(type) != 'mood'"), many=True)
    labels = json.dumps(labels_serialized.data)
    return JsonResponse({'labels': labels})


def all_genres(request):
    genres_serialized = GenreSerializer(Genre.objects.all(), many=True)
    genres = json.dumps(genres_serialized.data)
    return JsonResponse({'genres': genres})


def all_platforms(request):
    platforms_serialized = PlatformSerializer(Platform.objects.all(), many=True)
    platforms = json.dumps(platforms_serialized.data)
    return JsonResponse({'platforms': platforms})


def all_awards(request):
    awards_serialized = PlatformSerializer(Award.objects.all(), many=True)
    awards = json.dumps(awards_serialized.data)
    return JsonResponse({'awards': awards})


def all_languages(request):
    language_serialized = LanguageSerializer(Language.objects.all(), many=True)
    languages = json.dumps(language_serialized.data)
    return JsonResponse({'languages': languages})


def all_certificates(request):
    certificate_serialized = CertificateSerializer(Certificate.objects.all(), many=True)
    certificates = json.dumps(certificate_serialized.data)
    return JsonResponse({'certificates': certificates})


def all_collections(request):
    """
    This method returns all the movie/OTT collection list. See MovieCollection model object
    for the detailed fields.
    :param request:
    :return:
    """
    collections_serialized = CollectionSerializer(MovieCollection.objects.all(), many=True)
    collections = json.dumps(collections_serialized.data)
    return JsonResponse({'collections': collections})


def collection_details(request, collection_id):
    formatted_uuid = format_uuid(collection_id)
    data = MovieCollection.objects.raw("""
                                      SELECT \
                                      id, \
                                      name, \
                                      description, \
                                      bgImage \
                                      FROM review_moviecollection
                                      where id = '%s' 
                                      """ % formatted_uuid
                                       )

    if is_empty(list(data)):
        return JsonResponse({})

    serializer = CollectionSerializer(data, many=True)
    collection_data = json.dumps(serializer.data)
    col_data_json = json.loads(collection_data)

    if is_empty(col_data_json):
        return JsonResponse({})

    col_data_json_dict = col_data_json[0]
    serializer = CollectionDetailSerializer(
        MovieCollectionDetail.objects.raw(("""
                                          SELECT \
                                          id, \
                                          movie_name, \
                                          description, \
                                          release_date, \
                                          positive, \
                                          negative, \
                                          neutral, \
                                          ebits_rating, \
                                          thumbnail_image, \
                                          movie_id_id \
                                          FROM review_moviecollectiondetail
                                          where collection_id_id = '%s' 
                                          """ % formatted_uuid
                                           )
                                          )
        , many=True)

    collection_entry_data = json.dumps(serializer.data)

    col_data_json_dict['entries'] = collection_entry_data
    response = {'collection': col_data_json}
    return JsonResponse(response)


@require_http_methods(["POST"])
def movies(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    category_list = data.get('categories', [])
    genre_list = data.get('genres', [])
    mood_list = data.get('moods', [])
    certificate_list = data.get('certificates', [])
    language_list = data.get('languages', [])
    platform_list = data.get('platforms', [])
    awards_list = data.get('awards', [])
    ebits_rating_range = data.get('ebitsRatingRange', [])
    critics_rating_range = data.get('criticsRatingRange', [])

    filter_clause = ""
    # Add all labels together
    if not is_empty(category_list) or not is_empty(mood_list):
        label_list = category_list + mood_list
        single_quoted_list = map( lambda s :  "'" + s + "'", label_list)
        in_clause = ",".join(single_quoted_list)
        filter_clause = filter_clause + " review_movietolabel.label_id in (%s)" % in_clause

    if not is_empty(certificate_list):
        single_quoted_list = map(lambda s: "'" + s + "'", certificate_list)
        in_clause = ",".join(single_quoted_list)
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_movietocertificate.certificate_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietocertificate.certificate_id_id in (%s)" % in_clause

    if not is_empty(genre_list):
        single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
        in_clause = ",".join(single_quoted_list)
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_movietogenre.genre_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietogenre.genre_id in (%s)" % in_clause

    if not is_empty(language_list):
        single_quoted_list = map(lambda s: "'" + s + "'", language_list)
        in_clause = ",".join(single_quoted_list)
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_movietolanguage.language_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietolanguage.language_id_id in (%s)" % in_clause

    if not is_empty(platform_list):
        single_quoted_list = map(lambda s: "'" + s + "'", platform_list)
        in_clause = ",".join(single_quoted_list)
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_movietoplatform.platform_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietolanguage.platform_id in (%s)" % in_clause

    if not is_empty(awards_list):
        single_quoted_list = map(lambda s: "'" + s + "'", awards_list)
        in_clause = ",".join(single_quoted_list)
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_movietoaward.award_name_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietoaward.award_name_id in (%s)" % in_clause

    if not is_empty(ebits_rating_range):
        between_clause = "%s and %s " % (ebits_rating_range[0], ebits_rating_range[1])
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_moviepost.ebits_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_moviepost.ebits_rating between %s" % between_clause

    if not is_empty(critics_rating_range):
        between_clause = "%s and %s " % (critics_rating_range[0], critics_rating_range[1])
        if len(filter_clause) > 0:
            filter_clause = filter_clause + " and review_moviepost.critics_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_moviepost.critics_rating between %s" % between_clause

    final_query = """
                                  SELECT \
                                  review_moviepost.id, 
                                  movie_name as Title, \
                                  genre_id as Genre, \
                                  label_id as Label, \
                                  actors_display_comma_separated as Actors, \
                                  directors_display_comma_separated as Directors, \
                                  language_id_id as Language,\
                                  certificate_id_id as Certificate, \
                                  award_name_id as Award, \
                                  platform_id as Platform,\
                                  release_date as ReleaseDate, \
                                  ebits_rating as ebitsRating, \
                                  critics_rating as criticsRating, \
                                  thumbnail_image as image \
                                  FROM 
                                  review_moviepost,\
                                  review_movietogenre ,\
                                  review_movietolabel ,\
                                  review_movietolanguage ,\
                                  review_movietocertificate, \
                                  review_movietoaward, \
                                  review_movietoplatform \
                                  WHERE review_moviepost.id = review_movietogenre.movie_id_id \
                                  and review_moviepost.id = review_movietolabel.movie_id_id \
                                  and review_moviepost.id = review_movietocertificate.movie_id_id \
                                  and review_moviepost.id = review_movietoaward.movie_id_id \
                                  and review_moviepost.id = review_movietolanguage.movie_id_id \
                                  and review_moviepost.id = review_movietoplatform.movie_id_id \
                                  and  %s
                                  """ % filter_clause
    print(final_query)
    row_dict = raw_sql(final_query)

    movie_post_data = clean_json_dump(row_dict)
    pprint(movie_post_data)
    return JsonResponse({'movies': movie_post_data})

