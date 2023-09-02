import json
from pprint import pprint
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.models import Award, UserReviewDetail
from review.serializers import *
from review.utils import format_uuid, is_empty, raw_sql, authenticated


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
                                   from review_criticreviewdetail
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
    user_reviews_query = """select id, \
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   review_text,\
                                   reviewer_image_url,\
                                   review_likes,\
                                   review_dislikes, \
                                   slug \
                                   from review_userreviewdetail
                                    where movie_id_id = '%s' and review_approved is True order by review_date desc""" % movie_id
    user_review_rows = raw_sql(user_reviews_query)
    user_reviews_list = []
    for row in user_review_rows:
        user_review = {'id': row.get("id"),
                       'authorName': row.get("review_author"),
                       'ratings': row.get("review_rating"),
                       'title': row.get("review_title"),
                       'review': row.get("review_text"),
                       'dateTime': row.get("review_date"),
                       'image': row.get("reviewer_image_url"),
                       'likes': row.get("review_likes"),
                       'dislikes': row.get("review_dislikes"),
                       'slug': row.get("slug")
                       }

        user_reviews_list.append(user_review)

    return user_reviews_list


def get_avg_user_rating(movie_id):
    user_reviews_query = """select avg(review_rating) as avgUserRating, count(*) as totalReviews
                                   from review_userreviewdetail
                                    where movie_id_id = '%s' and review_approved is True""" % movie_id
    avg_user_ratings = raw_sql(user_reviews_query)

    if avg_user_ratings and len(avg_user_ratings) > 0:
        return avg_user_ratings[0]
    else:
        return {}


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
    platform_query = """select platform_id, image_url, platform_url from review_movietoplatform, review_platform \
    where review_movietoplatform.platform_id=review_platform.name and  movie_id_id = '%s' """ % movie_id
    platform_rows = raw_sql(platform_query)
    platform_list = []
    for row in platform_rows:
        platform = {"name": row.get("platform_id"), "url": row.get("image_url"), "platform_url": row.get("platform_url")}
        platform_list.append(platform)

    return platform_list


def get_movie_languages(movie_id):
    language_query = """select language_id_id from review_movietolanguage where movie_id_id = '%s' """ % movie_id
    language_rows = raw_sql(language_query)
    language_list = []
    for row in language_rows:
        language_list.append(row.get("language_id_id"))

    return language_list


def get_movie_trailers(movie_id):
    trailer_query = """select trailers_url from review_movietotrailer where movie_id_id = '%s' """ % movie_id
    trailer_rows = raw_sql(trailer_query)
    trailer_list = []
    for row in trailer_rows:
        trailer_list.append(row.get("trailers_url"))

    return trailer_list


def get_movie_photos(movie_id):
    photo_query = """select name, photo_url from review_movietophoto,\
                    review_phototype \
                    where review_movietophoto.movie_id_id=%s \
                    and review_movietophoto.photo_type_id=review_phototype.id """ % movie_id
    photo_rows = raw_sql(photo_query)
    photo_json = {}
    for row in photo_rows:
        photo_json[row.get("name")] = row.get("photo_url")

    return photo_json


def get_movie_awards(movie_id):
    award_query = """select award_name_id, award_for from review_movietoaward where movie_id_id = '%s' """ \
                  % movie_id
    award_rows = raw_sql(award_query)
    award_list = []
    for row in award_rows:
        award = {"awardName": row.get("award_name_id"), "awardFor": row.get("award_for")}
        award_list.append(award)

    return award_list


@require_http_methods(["POST"])
def add_likes(request):
    if authenticated(request):
        data = json.loads(request.body.decode("utf-8"))
        slug = data.get('slug', [])
        user_review = UserReviewDetail.objects.get(slug=slug)
        if not user_review:
            return JsonResponse({"message": "User review with slug %s not found " % slug})

        total_likes = user_review.review_likes
        if total_likes:
            total_likes = total_likes + 1
        else:
            total_likes = 1
        user_review.review_likes = total_likes
        user_review.save()
        message = "Successfully added user comment likes"
        return JsonResponse({"message": message})
    else:
        return HttpResponse('Unauthorized', status=401)



@require_http_methods(["POST"])
def add_dislikes(request):
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
    user_review = UserReviewDetail.objects.get(slug=slug)
    if not user_review:
        return JsonResponse({"message": "User review with slug %s not found " % slug})

    total_dislikes = user_review.review_dislikes
    if total_dislikes:
        total_dislikes = total_dislikes + 1
    else:
        total_dislikes = 1
    user_review.review_dislikes = total_dislikes
    user_review.save()
    message = "Successfully added user comment dislikes"
    return JsonResponse({"message": message})


@require_http_methods(["POST"])
def add_user_comment(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    slug = data.get('slug', [])
    movie_query = """select id from review_moviepost where slug='%s' limit 1""" % slug
    movie_row = raw_sql(movie_query)[0]
    movie_id = movie_row.get("id")

    review_author = data.get('author', [])
    review_rating = data.get('ratings', [])
    review_title = data.get('title', [])
    review_text = data.get('review', [])
    reviewer_image = data.get('image', [])

    movie = MoviePost.objects.get(id=movie_id)

    if not movie:
        message = "Invalid movie reference"
        return JsonResponse({"message": message})

    user_review = UserReviewDetail(movie_id=movie,
                                   review_author= review_author,
                                   review_rating=review_rating,
                                   review_title=review_title,
                                   review_date=date.today(),
                                   review_text=review_text,
                                   reviewer_image_url=reviewer_image,
                                   review_approved=False)

    user_review.save()

    message = "Successfully added user review"
    return JsonResponse({"message": message})


def similar_by_genres(request, slug):
    movie_query  = """select id from review_moviepost where slug='%s' limit 1""" % slug
    movie_row = raw_sql(movie_query)[0]
    movie_id = movie_row.get("id")

    genre_list = get_movie_genres(movie_id)

    if is_empty(genre_list):
        return JsonResponse({})

    single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
    in_clause = ",".join(single_quoted_list)
    filter_clause = " review_movietogenre.genre_id in (%s)" % in_clause

    final_query = """
                                      SELECT DISTINCT \
                                      review_moviepost.slug as slug, 
                                      movie_name, \
                                      duration, \
                                      description, \
                                      actors_display_comma_separated, \
                                      directors_display_comma_separated, \
                                      release_date, \
                                      ebits_rating, \
                                      critics_rating , \
                                      photo_url \
                                      FROM 
                                      review_moviepost,\
                                      review_movietogenre,\
                                      review_movietophoto,\
                                      review_phototype \
                                      
                                      WHERE review_moviepost.id = review_movietogenre.movie_id_id \
                                      and review_movietophoto.movie_id_id = review_moviepost.id \
                                      and review_moviepost.id != '%s' \
                                      and review_phototype.id = review_movietophoto.photo_type_id \
                                      and review_phototype.name = 'Cards_Listing_Similar_By_Genre' \
                                      
                                      and  %s ORDER BY rand()  limit 10
                                      """ % (movie_id, filter_clause)
    # print(final_query)
    similar_movies_row = raw_sql(final_query)

    similar_movies_list = []
    for row in similar_movies_row:
        movie = {'slug': row.get("slug"),
                               'title': row.get("movie_name"),
                               'description': row.get("description"),
                               'image': row.get("photo_url"),
                               'releaseDate': row.get("release_date"),
                               'duration': row.get("duration"),
                               'ebitsRatings': row.get("ebits_rating"),
                               'criticRatings': row.get("critics_rating"),
                               'directors': row.get("directors_display_comma_separated"),
                               'casts': row.get("actors_display_comma_separated")
                               }

        similar_movies_list.append(movie)

    return JsonResponse({"movies": similar_movies_list})



def movie_details(request, slug):
    formatted_uuid = format_uuid(slug)

    final_query = """
                                      SELECT \
                                      id, 
                                      slug,
                                      movie_name, \
                                      isSeries,
                                      episodes,        
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
                                      aspect_vfx, \
                                      
                                      ebits_rating, \
                                      thumbnail_image_url \
                                      FROM review_moviepost
                                      where slug = '%s' 
                                      """ % slug

    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})
    movie_dict = row_dict[0]
    
    movie_id = movie_dict.get("id")
    genre_list = get_movie_genres(movie_id)
    cert_list = get_movie_certificates(movie_id)
    platform_list = get_movie_platforms(movie_id)
    language_list = get_movie_languages(movie_id)
    trailer_list = get_movie_trailers(movie_id)
    photo_list = get_movie_photos(movie_id)
    critics_reviews_list = get_critics_reviews(movie_id)
    user_reviews_list = get_user_reviews(movie_id)
    award_list = get_movie_awards(movie_id)
    avg_usr_rating_details = get_avg_user_rating(movie_id)


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
                    "slug": movie_dict.get("slug"),
                    "title": movie_dict.get("movie_name"),
                    "length": movie_dict.get("duration"),
                    "isSeries": movie_dict.get("isSeries"),
                    "episodes": movie_dict.get("episodes"),
                    "sentimeter": sentimeter_dict,
                    "aspects": aspects_dict,
                    "overview": overview_dict,
                    "genres": genre_list,
                    "certifications": cert_list,
                    "criticReviews": critics_reviews_list,
                    "userReviews": user_reviews_list,
                    "avgUserReviews": avg_usr_rating_details
                    }

    return JsonResponse(movie_detail)


def all_moods(request):
    final_query = """ select label_id as name ,photo_url as url,  count(*) as cnt from review_moviepost
      left join review_movietolabel on review_moviepost.id = review_movietolabel.movie_id_id
      join  review_label on  review_movietolabel.label_id = review_label.name
      and LOWER(review_label.type) = 'mood' group by label_id, photo_url """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"),
                 "url": d.get("url"),
                 "count": d.get("cnt")}
        records.append(datum)
    js_val["moods"] = records
    return JsonResponse(js_val)


def all_labels(request):
    final_query = """ select label_id as name , count(*) as cnt from review_moviepost
      left join review_movietolabel on review_moviepost.id = review_movietolabel.movie_id_id
      join  review_label on  review_movietolabel.label_id = review_label.name
      and LOWER(review_label.type) != 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["categories"] = records
    return JsonResponse(js_val)


def all_genres(request):
    final_query = """ select genre_id as name , count(*) as cnt from review_moviepost \
     left join review_movietogenre on review_moviepost.id = review_movietogenre.movie_id_id group by genre_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["geners"] = records
    return JsonResponse(js_val, safe=False)


def all_platforms(request):
    data = list(Platform.objects.values())
    priority_list = ["Prime Video", "Netflix", "SonyLIV", "TVFPlay", "Disney+Hotstar", "Hotstar"]
    js_val = {}
    records = []
    priority = []
    for d in data:
        datum = {"name": d.get("name"), "image_url": d.get("image_url"), "platform_url": d.get("platform_url")}
        if d.get("name") in  priority_list:
            priority.append(datum)
        else:
            records.append(datum)

    priority.extend(records)
    js_val["platforms"] = priority
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
                     review_report.slug as slug, \
                     review_moviecollection.name as title,\
                     description as summary,\
                     chart_data_json as chart, \
                     review_report.publish_date \
                     from  review_report, review_moviecollection \
                     where review_report.collection_id_id = review_moviecollection.id \
                     order by publish_date desc limit 20
                     """
    row_dict = raw_sql(final_query)

    reports = []
    for row in row_dict:
        pprint(type(row.get("chart")))
        r = {'slug': row.get("slug"),
             'title': row.get("title"),
             'summary': row.get("summary"),
             'chart': json.loads(row.get("chart")),
             'chartImage': ''
             }

        reports.append(r)

    return JsonResponse({'reports': reports})


def report_details(request, slug):

    final_query = """Select
                         review_report.id, \
                         review_report.slug as slug, \
                         review_report.collection_id_id as collectionId,\
                         review_moviecollection.name as title,\
                         description as summary,\
                         chart_data_json as chart \
                         from  review_report, review_moviecollection \
                         where review_report.collection_id_id = review_moviecollection.id \
                         and   review_report.slug = '%s'
                         """ % slug
    row_dict = raw_sql(final_query)
    pprint(row_dict)
    if is_empty(row_dict):
        return JsonResponse({})

    first_entry = row_dict[0]
    collection_id = first_entry.get("collectionId", None)
    if not collection_id:
        return JsonResponse({})

    report = {'slug': first_entry.get("slug"),
         'title': first_entry.get("title"),
         'summary': first_entry.get("summary"),
         'chart': json.loads(first_entry.get("chart"))
         }

    collection_entry_data = get_collection_details(collection_id, True)

    report['entries'] = collection_entry_data
    response = {'report': report}

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
                         slug, \
                         name,\
                         description,\
                         image_url , \
                         home_collection_banner_image, \
                         publish_date \
                         from  review_moviecollection \
                         where not is_report \
                         order by publish_date desc limit 10
                         """

    all_colls = raw_sql(final_query)
    pprint(all_colls)
    if is_empty(all_colls):
        return JsonResponse({})

    final_reponse = []
    count = 0
    for col in all_colls:
        col_id = col.get("id")
        slug = col.get("slug")
        col['type'] = 'movie'
        collection_entry_data = get_collection_details(col_id, False)
        col['entries'] = collection_entry_data
        final_reponse.append(col)
        count = count + 1

    return JsonResponse({'collections': final_reponse})


def collection_details(request, slug):

    data = MovieCollection.objects.raw("""
                                      SELECT \
                                      id, \
                                      name, \
                                      description, \
                                      image_url \
                                      FROM review_moviecollection
                                      where slug = '%s'
                                      """ % slug
                                       )

    if is_empty(list(data)):
        return JsonResponse({})

    serializer = CollectionSerializer(data, many=True)
    collection_data = json.dumps(serializer.data)
    col_data_json = json.loads(collection_data)

    if is_empty(col_data_json):
        return JsonResponse({})

    col_data_json_dict = col_data_json[0]
    collection_id = col_data_json_dict.get("id")
    print("collection_id " + str(collection_id))
    collection_entry_data = get_collection_details(collection_id, False)

    col_data_json_dict['entries'] = collection_entry_data
    response = {'collection': col_data_json}
    return JsonResponse(response)



def get_collection_details(collection_id, is_report):
    report_predicate = "review_moviecollection.is_report" 
    if is_report:
        report_predicate = "review_moviecollection.is_report"
    else:
        report_predicate = "not review_moviecollection.is_report"
    pprint("is_report " + str(is_report))
    final_query = """
                                                SELECT \
                                                review_moviecollectiondetail.slug ,\
                                                movie_name as title, \
                                                movie_id_id as movie_id, \
                                                ebits_rating as rating, \
                                                review_moviecollectiondetail.description,\
                                                thumbnail_image_url as bgImage, \
                                                release_date as releaseDate, \
                                                aspect_story, \
                                                aspect_direction,\
                                                aspect_music, \
                                                aspect_performance, \
                                                aspect_costume, \
                                                aspect_screenplay, \
                                                aspect_vfx, \
                                                genres,  \
                                                platform_id
                                                FROM review_moviecollectiondetail, review_moviecollection
                                                where
                                                review_moviecollectiondetail.collection_id_id = review_moviecollection.id
                                                and review_moviecollection.id = '%s' and %s
                                                  """ % (collection_id, report_predicate)

    platform_query = """select review_platform.name as platform, \
        review_platform.platform_url, \
        review_platform.image_url as platform_image_url from review_platform where name = '%s'
        """

    movie_slug_query = """select review_moviepost.slug as \
     movie_slug from review_moviepost where review_moviepost.id = %s """

    pprint(final_query)
    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        movie_slug = ""
        if row.get("movie_id", None):
            all_movies = raw_sql(movie_slug_query % row.get("movie_id"))
            if len(all_movies) > 0:
                movie_slug = all_movies[0].get("movie_slug")

        entry = {"slug": row.get("slug"),
                 "name": row.get("title"),
                 "movie_slug": movie_slug,
                 "ebitsRatings": row.get("rating"),
                 "description": row.get("description"),
                 "release_date": row.get("releaseDate"),
                 "aspect_story": row.get("aspect_story"),
                 "aspect_direction": row.get("aspect_direction"),
                 "aspect_music": row.get("aspect_music"),
                 "aspect_performance": row.get("aspect_performance"),
                 "aspect_costume": row.get("aspect_costume"),
                 "aspect_screenplay": row.get("aspect_screenplay"),
                 "aspect_vfx": row.get("aspect_vfx"),
                 "genres": row.get("genres"),
                 "image": row.get("bgImage")}

        if row.get("platform_id", None):
            platform_dict = raw_sql(platform_query % row.get("platform_id"))
            entry["platform_details"] = platform_dict

        entries.append(entry)

    return entries


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
    ebits_rating_range = data.get('ebitsRatingRange', {})
    critics_rating_range = data.get('criticsRatingRange', {})
    offset_range = data.get('offsetRange', {})

    filter_clause = ""
    join_clause = ""
    # Add all labels together
    if not is_empty(category_list) or not is_empty(mood_list):
        label_list = category_list + mood_list
        single_quoted_list = map(lambda s: "'" + s + "'", label_list)
        in_clause = ",".join(single_quoted_list)
        filter_clause = filter_clause + " review_movietolabel.label_id in (%s)" % in_clause

    if not is_empty(certificate_list):
        single_quoted_list = map(lambda s: "'" + s + "'", certificate_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_movietocertificate.certificate_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietocertificate.certificate_id_id in (%s)" % in_clause

    if not is_empty(genre_list):
        single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_movietogenre.genre_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietogenre.genre_id in (%s)" % in_clause

    if not is_empty(language_list):
        single_quoted_list = map(lambda s: "'" + s + "'", language_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_movietolanguage.language_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietolanguage.language_id_id in (%s)" % in_clause

    if not is_empty(platform_list):
        single_quoted_list = map(lambda s: "'" + s + "'", platform_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_movietoplatform.platform_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietoplatform.platform_id in (%s)" % in_clause

    if not is_empty(awards_list):
        single_quoted_list = map(lambda s: "'" + s + "'", awards_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_movietoaward.award_name_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_movietoaward.award_name_id in (%s)" % in_clause

    if ebits_rating_range and not is_empty(ebits_rating_range):
        between_clause = "%s and %s " % (ebits_rating_range.get("low"), ebits_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_moviepost.ebits_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_moviepost.ebits_rating between %s" % between_clause

    if critics_rating_range and not is_empty(critics_rating_range):
        between_clause = "%s and %s " % (critics_rating_range.get("low"), critics_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_moviepost.critics_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_moviepost.critics_rating between %s" % between_clause

    count_clause = filter_clause
    filter_clause = filter_clause + " ORDER BY release_date desc "

    if offset_range and not is_empty(offset_range):
        limit = offset_range.get("limit")
        offset = offset_range.get("offset")
        if limit and int(limit) > 50:
            raise Exception('spam', 'Invalid limit clause')

        if offset and int(offset) < 0:
            raise Exception('spam', 'Invalid offset clause')

        limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)
        filter_clause = filter_clause + limit_clause


    join_clause = """
                                  left join review_movietogenre on review_moviepost.id = review_movietogenre.movie_id_id \
                                  left join review_movietolabel on review_moviepost.id = review_movietolabel.movie_id_id \
                                  left join review_movietolanguage on review_moviepost.id = review_movietolanguage.movie_id_id \
                                  left join review_movietocertificate on review_moviepost.id = review_movietocertificate.movie_id_id \
                                  left join review_movietoaward on review_moviepost.id = review_movietoaward.movie_id_id \
                                  left join review_movietoplatform on review_moviepost.id = review_movietoplatform.movie_id_id\
    """
    final_query = """
                                  SELECT DISTINCT  \
                                  review_moviepost.id,
                                  review_moviepost.slug,
                                  movie_name as Title, \
                                  actors_display_comma_separated as Actors, \
                                  directors_display_comma_separated as Directors, \
                                  release_date as ReleaseDate, \
                                  ebits_rating as ebitsRating, \
                                  critics_rating as criticsRating, \
                                  thumbnail_image_url as image, \
                                  review_moviepost.description, \
                                  review_moviepost.duration
                                  FROM
                                  review_moviepost \
                                  %s 
                                  WHERE   %s
                                  """ % (join_clause, filter_clause)

    count_query = """
                                      SELECT count(DISTINCT review_moviepost.id) as totalEntries  \
                                      FROM
                                      review_moviepost \
                                      %s 
                                      WHERE   %s
                                      """ % (join_clause, count_clause)

    print(final_query)


    count_dict = raw_sql(count_query)
    row_dict = raw_sql(final_query)

    entries = []

    for row in row_dict:
        photo_dict = get_movie_photos(row.get("id"))
        trailer_dict = get_movie_trailers(row.get("id"))
        row["photos"] = photo_dict
        row["trailers"] = trailer_dict
        row["genres"] = get_movie_genres(row.get("id"))
        entries.append(row)

    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) >0 else 0
    final_output = {'totalEntries': total_count, 'movies': entries}
    return JsonResponse(final_output)


def homepage_movies(request):
    label = request.GET.get("label", "")
    if is_empty(label):
        return []
    final_query = """
                                      SELECT DISTINCT  \
                                      review_moviepost.id,
                                      review_moviepost.slug,
                                      movie_name as Title, \
                                      release_date as ReleaseDate, \
                                      ebits_rating as ebitsRating, \
                                      thumbnail_image_url as image, \
                                      review_moviepost.duration, \
                                      aspect_story, \
                                      aspect_direction, \
                                      aspect_music, \
                                      aspect_performance, \
                                      aspect_costume, \
                                      aspect_screenplay, \
                                      aspect_vfx \
                                      FROM
                                      review_moviepost \
                                      left join review_movietolabel \
                                      on review_moviepost.id = review_movietolabel.movie_id_id \
                                      WHERE   review_movietolabel.label_id = '%s' \
                                      ORDER BY release_date desc limit 10 """ % label

    row_dict = raw_sql(final_query)
    entries = []
    for row in row_dict:
        photo_dict = get_movie_photos(row.get("id"))
        row["photos"] = photo_dict
        row["genres"] = get_movie_genres(row.get("id"))
        row["platforms"] = get_movie_platforms(row.get("id"))
        entries.append(row)

    return entries


def movie_search(request):
    keywords = request.GET["keywords"]
    if is_empty(keywords):
        return JsonResponse({'movies': ""})

    serach_query = """SELECT id, slug,\
     duration, \
     release_date, \
     thumbnail_image_url from review_moviepost where MATCH (movie_name, description, ebits_review) \
                      AGAINST ('%s' IN NATURAL LANGUAGE MODE) """

    row_dict = raw_sql(serach_query % keywords)
    entries = []
    for row in row_dict:
        row["genres"] = get_movie_genres(row.get("id"))
        entries.append(row)

    return entries
