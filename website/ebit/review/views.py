import json
from pprint import pprint
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.models import Award, UserReviewDetail
from review.serializers import *
from review.utils import format_uuid, is_empty, raw_sql


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_critics_reviews(movie_id):
    critics_reviews_query = """select publication_name,\
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   critic_review 
                                   from review_CriticReviewDetail
                                    where movie_id_id = '%s' """ % movie_id
    critics_review_rows = raw_sql(critics_reviews_query)
    critics_reviews_list = []
    for row in critics_review_rows:
        critics_review = {'authorName': row.get("review_author"),
                          'publication': row.get("publication_name"),
                          'ratings': row.get("review_rating"),
                          'title': row.get("review_title"),
                          'review': row.get("critic_review"),
                          'dateTime': row.get("review_date")
                          }

        critics_reviews_list.append(critics_review)

    return critics_reviews_list


def get_user_reviews(movie_id):
    user_reviews_query = """select 
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   review_text,\
                                   reviewer_image
                                   from review_UserReviewDetail
                                    where movie_id_id = '%s' and review_approved is True""" % movie_id
    user_review_rows = raw_sql(user_reviews_query)
    user_reviews_list = []
    for row in user_review_rows:
        user_review = {'authorName': row.get("review_author"),
                       'ratings': row.get("review_rating"),
                       'title': row.get("review_title"),
                       'review': row.get("critic_review"),
                       'dateTime': row.get("review_date"),
                       'image': row.get("reviewer_image")
                       }

        user_reviews_list.append(user_review)

    return user_reviews_list


def get_movie_genres(movie_id):
    genre_query = """select genre_id from review_movietogenre where movie_id_id = '%s' """ % movie_id
    genre_rows = raw_sql(genre_query)
    genre_list = []
    for row in genre_rows:
        genre_list.append(row.get("genre_id"))

    return genre_list


def get_movie_certificates(movie_id):
    certificate_query = """select certificate_id_id from review_movietocertificate where movie_id_id = '%s' """ % movie_id
    cert_rows = raw_sql(certificate_query)
    cert_list = []
    for row in cert_rows:
        cert_list.append(row.get("certificate_id_id"))

    return cert_list


def get_movie_platforms(movie_id):
    platform_query = """select platform_id from review_MovieToPlatform where movie_id_id = '%s' """ % movie_id
    platform_rows = raw_sql(platform_query)
    platform_list = []
    for row in platform_rows:
        platform_list.append(row.get("platform_id"))

    return platform_list


def get_movie_languages(movie_id):
    language_query = """select language_id_id from review_MovieToLanguage where movie_id_id = '%s' """ % movie_id
    language_rows = raw_sql(language_query)
    language_list = []
    for row in language_rows:
        language_list.append(row.get("language_id_id"))

    return language_list


def get_movie_trailers(movie_id):
    trailer_query = """select trailers from review_MovieToTrailer where movie_id_id = '%s' """ % movie_id
    trailer_rows = raw_sql(trailer_query)
    trailer_list = []
    for row in trailer_rows:
        trailer_list.append(row.get("trailers"))

    return trailer_list


def get_movie_photos(movie_id):
    photo_query = """select photo from review_MovieToPhoto where movie_id_id = '%s' """ % movie_id
    photo_rows = raw_sql(photo_query)
    photo_list = []
    for row in photo_rows:
        photo_list.append(row.get("photo"))

    return photo_list


def get_movie_awards(movie_id):
    award_query = """select award_name_id, award_for from review_MovieToAward where movie_id_id = '%s' """ \
                  % movie_id
    award_rows = raw_sql(award_query)
    award_list = []
    for row in award_rows:
        award = {"awardName": row.get("award_name_id"), "awardFor": row.get("award_for")}
        award_list.append(award)

    return award_list


@require_http_methods(["POST"])
def add_user_comment(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    movie_id = data.get('id', [])
    review_author = data.get('author', [])
    review_rating = data.get('ratings', [])
    review_title = data.get('title', [])
    review_text = data.get('review', [])
    reviewer_image = data.get('image', [])

    formatted_uuid = format_uuid(movie_id)
    movie = MoviePost.objects.get(id=formatted_uuid)

    if not movie:
        message = "Invalid movie reference"
        return JsonResponse({"message": message})

    user_review = UserReviewDetail(movie_id=movie,
                                   review_author= review_author,
                                   review_rating=review_rating,
                                   review_title=review_title,
                                   review_date=date.today(),
                                   review_text=review_text,
                                   reviewer_image=reviewer_image,
                                   review_approved=False)

    user_review.save()

    message = "Successfully added user review"
    return JsonResponse({"message": message})


def similar_by_genres(request, movie_id):
    formatted_uuid = format_uuid(movie_id)
    genre_list = get_movie_genres(formatted_uuid)
    if is_empty(genre_list):
        return JsonResponse({})

    single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
    in_clause = ",".join(single_quoted_list)
    filter_clause = " review_movietogenre.genre_id in (%s)" % in_clause

    final_query = """
                                      SELECT \
                                      review_moviepost.id as id, 
                                      movie_name, \
                                      duration, \
                                      description, \
                                      actors_display_comma_separated, \
                                      directors_display_comma_separated, \
                                      release_date, \
                                      ebits_rating, \
                                      critics_rating , \
                                      thumbnail_image \
                                      FROM 
                                      review_moviepost,\
                                      review_movietogenre
                                      
                                      WHERE review_moviepost.id = review_movietogenre.movie_id_id \
                                      and review_moviepost.id != '%s' \
                                      and  %s ORDER BY random()  limit 10
                                      """ % (formatted_uuid, filter_clause)
    # print(final_query)
    similar_movies_row = raw_sql(final_query)

    similar_movies_list = []
    for row in similar_movies_row:
        movie = {'id': row.get("id"),
                               'title': row.get("movie_name"),
                               'description': row.get("duration"),
                               'image': row.get("thumbnail_image"),
                               'releaseDate': row.get("release_date"),
                               'duration': row.get("review_date"),
                               'ebitsRatings': row.get("ebits_rating"),
                               'criticRatings': row.get("critics_rating"),
                               'directors': row.get("directors_display_comma_separated"),
                               'casts': row.get("actors_display_comma_separated")
                               }

        similar_movies_list.append(movie)

    return JsonResponse({"movies": similar_movies_list})


def movie_details(request, movie_id):
    formatted_uuid = format_uuid(movie_id)

    final_query = """
                                      SELECT \
                                      id, 
                                      movie_name, \
                                      duration, \
                                      release_date, \
                                      description, \
                                      directors_display_comma_separated, \
                                      actors_display_comma_separated,\
                                      
                                      ebits_rating,\
                                      ebits_review,\
                                      ebits_reviewer_name,\
                                      ebits_reviewer_image,\
                                      critics_rating,\
                                      
                                      positive, \
                                      negative, \
                                      neutral, \
                                      
                                      aspect_story, \
                                      aspect_direction, \
                                      aspect_music, \
                                      aspect_performance, \
                                      aspect_costume, \
                                      aspect_screenplay, \
                                      aspect_vxf, \
                                      
                                      ebits_rating, \
                                      thumbnail_image \
                                      FROM review_moviepost
                                      where id = '%s' 
                                      """ % formatted_uuid

    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})
    movie_dict = row_dict[0]

    genre_list = get_movie_genres(formatted_uuid)
    cert_list = get_movie_certificates(formatted_uuid)
    platform_list = get_movie_platforms(formatted_uuid)
    language_list = get_movie_languages(formatted_uuid)
    trailer_list = get_movie_trailers(formatted_uuid)
    photo_list = get_movie_photos(formatted_uuid)
    critics_reviews_list = get_critics_reviews(formatted_uuid)
    user_reviews_list = get_user_reviews(formatted_uuid)
    award_list = get_movie_awards(formatted_uuid)

    gallery_dict = {"trailers": trailer_list, "photos": photo_list}

    sentimeter_dict = {"positive": movie_dict.get("positive"),
                       "negative": movie_dict.get("negative"),
                       "neutral": movie_dict.get("neutral")}

    aspects_dict = {"story": movie_dict.get("aspect_story"),
                    "direction": movie_dict.get("aspect_direction"),
                    "music": movie_dict.get("aspect_music"),
                    "performance": movie_dict.get("aspect_performance"),
                    "costume": movie_dict.get("aspect_costume"),
                    "screenplay": movie_dict.get("aspect_screenplay"),
                    "vxf": movie_dict.get("aspect_vxf"),
                    }

    overview_dict = {"realeaseDate": movie_dict.get("release_date"),
                     "storyline": movie_dict.get("description"),
                     "directors": movie_dict.get("directors_display_comma_separated"),
                     "casts": movie_dict.get("actors_display_comma_separated"),

                     "ebitsRating": movie_dict.get("ebits_rating"),
                     "ebitsReview": movie_dict.get("ebits_review"),
                     "ebitsReviewer": movie_dict.get("ebits_reviewer_name"),
                     "ebitsReviewerImage": movie_dict.get("ebits_reviewer_image"),
                     "averageCriticsRating": movie_dict.get("critics_rating"),
                     "platforms": platform_list,
                     "language": language_list,
                     "awards": award_list,
                     "gallery": gallery_dict
                     }

    movie_detail = {"id": movie_dict.get("id"),
                    "title": movie_dict.get("movie_name"),
                    "length": movie_dict.get("duration"),
                    "sentimeter": sentimeter_dict,
                    "aspects": aspects_dict,
                    "overview": overview_dict,
                    "genres": genre_list,
                    "certifications": cert_list,
                    "criticReviews": critics_reviews_list,
                    "userReviews": user_reviews_list
                    }

    return JsonResponse(movie_detail)


def all_moods(request):
    moods = Label.objects.raw("select name, photo from review_label where LOWER(type) = 'mood'")
    js_val = {}
    records = []
    for d in moods:
        obj = {"name": d.name, "photo": ""}
        records.append(obj)
    js_val["moods"] = records
    return JsonResponse(js_val)


def all_labels(request):
    labels = Label.objects.raw("select name from review_label where LOWER(type) != 'mood'")
    js_val = {}
    records = []
    for d in labels:
        obj = {"name": d.name, "photo": ""}
        records.append(obj)
    js_val["categories"] = records
    return JsonResponse(js_val)


def all_genres(request):
    data = list(Genre.objects.values())
    js_val = {}
    records = []
    for d in data:
        records.append(d.get("name"))
    js_val["geners"] = records
    return JsonResponse(js_val, safe=False)


def all_platforms(request):
    data = list(Platform.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["platforms"] = records
    return JsonResponse(js_val, safe=False)


def all_awards(request):
    data = list(Award.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["awards"] = records
    return JsonResponse(js_val, safe=False)


def all_languages(request):
    data = list(Language.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["languages"] = records
    return JsonResponse(js_val, safe=False)


def all_certificates(request):
    data = list(Certificate.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["certifications"] = records
    return JsonResponse(js_val, safe=False)


def all_reports(request):
    """
    This method returns all the Report collection list. See Report model object
    for the detailed fields.
    :param request:
    :return:
    """
    final_query = """Select
                     review_report.id as id, \
                     review_moviecollection.name as title,\
                     description as summary,\
                     chart_data_json as chart, \
                     publish_date \
                     from  review_report, review_moviecollection \
                     where review_report.collection_id_id = review_moviecollection.id \
                     order by publish_date desc limit 20       
                     """
    row_dict = raw_sql(final_query)

    reports = []
    for row in row_dict:
        pprint(type(row.get("chart")))
        r = {'id': row.get("id"),
             'title': row.get("title"),
             'summary': row.get("summary"),
             'chart': json.loads(row.get("chart")),
             'chartImage': ''
             }

        reports.append(r)

    return JsonResponse({'reports': reports})


def report_details(request, report_id):
    formatted_uuid = format_uuid(report_id)
    final_query = """Select
                         review_report.id, \
                         review_report.collection_id_id as collectionId,\
                         review_moviecollection.name as title,\
                         description as summary,\
                         chart_data_json \
                         from  review_report, review_moviecollection \
                         where review_report.collection_id_id = review_moviecollection.id \
                         and   review_report.id = '%s'   
                         """ % formatted_uuid
    row_dict = raw_sql(final_query)
    pprint(row_dict)
    if is_empty(row_dict):
        return JsonResponse({})

    first_entry = row_dict[0]
    collection_id = first_entry.get("collectionId", None)
    if not collection_id:
        return JsonResponse({})

    collection_entry_data = get_collection_details(collection_id, True)

    first_entry['entries'] = collection_entry_data
    response = {'report': first_entry}

    return JsonResponse(response)


def all_collections(request):
    """
    This method returns all the movie/OTT collection list. See MovieCollection model object
    for the detailed fields.
    :param request:
    :return:
    """
    final_query = """Select
                         id, \
                         name,\
                         description as summary,\
                         bgImage , \
                         publish_date \
                         from  review_moviecollection \
                         where not is_report \
                         order by publish_date desc limit 20       
                         """

    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})

    return JsonResponse({'collections': row_dict})


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
    collection_entry_data = get_collection_details(formatted_uuid, False)

    col_data_json_dict['entries'] = collection_entry_data
    response = {'collection': col_data_json}
    return JsonResponse(response)


def get_collection_details(collection_id, is_report):
    report_redicate = "review_moviecollection.is_report" \
        if is_report else "not review_moviecollection.is_report"
    final_query = """
                                                SELECT \
                                                review_moviecollectiondetail.id ,\
                                                movie_name as title, \
                                                ebits_rating as rating, \
                                                review_moviecollectiondetail.description,\
                                                thumbnail_image as bgImage, \
                                                release_date as releaseDate, \
                                                aspect_story as story, \
                                                aspect_direction as direction,\
                                                aspect_music as music, \
                                                aspect_performance as performance, \
                                                aspect_costume as costume, \
                                                aspect_screenplay as screenplay, \
                                                aspect_vxf as vxf, \
                                                genres  \
                                                FROM review_moviecollectiondetail, review_moviecollection
                                                where 
                                                review_moviecollectiondetail.collection_id_id = review_moviecollection.id 
                                                and collection_id_id = '%s' and %s
                                                  """ % (collection_id, report_redicate)
    pprint(final_query)
    row_dict = raw_sql(final_query)
    return row_dict


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
        single_quoted_list = map(lambda s: "'" + s + "'", label_list)
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
    # print(final_query)
    row_dict = raw_sql(final_query)
    return JsonResponse({'movies': row_dict})
