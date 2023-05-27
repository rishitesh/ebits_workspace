import json
from pprint import pprint
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.gamesModels import GUserReviewDetail, GamePost, GLanguage, GPlatform, GameAward, GCertificate, \
    GameCollection

from review.gameSerializers import *
from review.utils import format_uuid, is_empty, raw_sql


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_critics_reviews(game_id):
    critics_reviews_query = """select publication_name,\
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   critic_review 
                                   from review_gcriticreviewdetail
                                    where game_id_id = '%s' """ % game_id
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


def get_user_reviews(game_id):
    user_reviews_query = """select 
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   review_text,\
                                   reviewer_image_url,\
                                   review_likes,\
                                   review_dislikes, \
                                   slug 
                                   from review_guserreviewdetail
                                    where game_id_id = '%s' and review_approved is True""" % game_id
    user_review_rows = raw_sql(user_reviews_query)
    user_reviews_list = []
    for row in user_review_rows:
        user_review = {'authorName': row.get("review_author"),
                       'ratings': row.get("review_rating"),
                       'title': row.get("review_title"),
                       'review': row.get("critic_review"),
                       'dateTime': row.get("review_date"),
                       'image': row.get("reviewer_image_url"),
                       'likes': row.get("review_likes"),
                       'dislikes': row.get("review_dislikes"),
                       'slug': row.get("slug")
                       }

        user_reviews_list.append(user_review)

    return user_reviews_list


def get_avg_user_rating(book_id):
    user_reviews_query = """select avg(review_rating) as avgUserRating, count(*) as totalReviews
                                   from review_guserreviewdetail
                                    where game_id_id = '%s' and review_approved is True""" % book_id
    avg_user_ratings = raw_sql(user_reviews_query)

    if avg_user_ratings and len(avg_user_ratings) > 0:
        return avg_user_ratings[0]
    else:
        return {}


def get_game_genres(game_id):
    genre_query = """select genre_id from review_gametogenre where game_id_id = '%s' """ % game_id
    genre_rows = raw_sql(genre_query)
    genre_list = []
    for row in genre_rows:
        genre_list.append(row.get("genre_id"))

    return genre_list


def get_game_certificates(game_id):
    certificate_query = """select certificate_id_id from review_gametocertificate where game_id_id = '%s' """ % game_id
    cert_rows = raw_sql(certificate_query)
    cert_list = []
    for row in cert_rows:
        cert_list.append(row.get("certificate_id_id"))

    return cert_list


def get_game_platforms(game_id):
    platform_query = """select platform_id from review_gametoplatform where game_id_id = '%s' """ % game_id
    platform_rows = raw_sql(platform_query)
    platform_list = []
    for row in platform_rows:
        platform_list.append(row.get("game_id"))

    return platform_list


def get_game_languages(game_id):
    language_query = """select language_id_id from review_gametolanguage where game_id_id = '%s' """ % game_id
    language_rows = raw_sql(language_query)
    language_list = []
    for row in language_rows:
        language_list.append(row.get("language_id_id"))

    return language_list


def get_game_trailers(game_id):
    trailer_query = """select trailers_url from review_gametotrailer where game_id_id = '%s' """ % game_id
    trailer_rows = raw_sql(trailer_query)
    trailer_list = []
    for row in trailer_rows:
        trailer_list.append(row.get("trailers"))

    return trailer_list


def get_game_photos(game_id):
    photo_query = """select name, photo_url from review_gametophoto,\
                       review_gphototype \
                       where review_gametophoto.game_id_id=%s \
                       and review_gametophoto.photo_type_id=review_gphototype.id """ % game_id

    photo_rows = raw_sql(photo_query)
    photo_list = []
    for row in photo_rows:
        photo = {"name": row.get("name"), "photo_url": row.get("photo_url")}
        photo_list.append(photo)

    return photo_list


def get_game_awards(game_id):
    award_query = """select award_name_id, award_for from review_gametoaward where game_id_id = '%s' """ \
                  % game_id
    award_rows = raw_sql(award_query)
    award_list = []
    for row in award_rows:
        award = {"awardName": row.get("award_name_id"), "awardFor": row.get("award_for")}
        award_list.append(award)

    return award_list


@require_http_methods(["POST"])
def add_likes(request):
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
    user_review = GUserReviewDetail.objects.get(slug=slug)
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


@require_http_methods(["POST"])
def add_dislikes(request):
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
    user_review = GUserReviewDetail.objects.get(slug=slug)
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
    game_query = """select id from review_gamepost where slug='%s' limit 1""" % slug
    game_row = raw_sql(game_query)[0]
    game_id = game_row.get("id")

    review_author = data.get('author', [])
    review_rating = data.get('ratings', [])
    review_title = data.get('title', [])
    review_text = data.get('review', [])
    reviewer_image = data.get('image', [])

    game = GamePost.objects.get(id=game_id)

    if not game:
        message = "Invalid podcast reference"
        return JsonResponse({"message": message})

    user_review = GUserReviewDetail(game_id=game,
                                   review_author=review_author,
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
    game_query = """select id from review_gamepost where slug='%s' limit 1""" % slug
    game_row = raw_sql(game_query)[0]
    game_id = game_row.get("id")

    genre_list = get_game_genres(game_id)

    if is_empty(genre_list):
        return JsonResponse({})

    single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
    in_clause = ",".join(single_quoted_list)
    filter_clause = " review_gametogenre.genre_id in (%s)" % in_clause

    final_query = """
                                      SELECT \
                                      review_gamepost.id as id, 
                                      game_name, \
                                      description, \
                                      developer, \
                                      provider, \
                                      release_date, \
                                      ebits_rating, \
                                      critics_rating , \
                                      thumbnail_image_url \
                                      FROM 
                                      review_gamepost,\
                                      review_gametogenre

                                      WHERE review_gamepost.id = review_gametogenre.game_id_id \
                                      and review_gamepost.id != '%s' \
                                      and  %s ORDER BY rand()  limit 10
                                      """ % (game_id, filter_clause)
    # print(final_query)
    similar_game_row = raw_sql(final_query)

    similar_game_list = []
    for row in similar_game_row:
        game = {'id': row.get("id"),
                 'name': row.get("game_name"),
                 'description': row.get("description"),
                 'image': row.get("thumbnail_image_url"),
                 'releaseDate': row.get("release_date"),
                 'ebitsRatings': row.get("ebits_rating"),
                 'criticRatings': row.get("critics_rating"),
                 'developer': row.get("developer"),
                 'provider': row.get("provider"),
                 }

        similar_game_list.append(game)

    return JsonResponse({"games": similar_game_list})


def game_details(request, slug):
    formatted_uuid = format_uuid(slug)

    final_query = """
                                      SELECT \
                                      id, 
                                      slug,
                                      game_name, \
                                      release_date, \
                                      description, \
                                      developer,\
                                      provider,\

                                      ebits_rating,\
                                      ebits_review,\
                                      ebits_reviewer_name,\
                                      ebits_reviewer_image,\
                                      critics_rating,\

                                      positive, \
                                      negative, \
                                      neutral, \

                                      aspect_graphics, \
                                      aspect_performance, \
                                      aspect_animation, \
                                      aspect_easeOfUse, \

                                      ebits_rating, \
                                      thumbnail_image_url \
                                      FROM review_gamepost
                                      where slug = '%s' 
                                      """ % slug

    pprint(final_query)
    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})
    game_dict = row_dict[0]
    game_id = game_dict.get("id")

    genre_list = get_game_genres(game_id)
    cert_list = get_game_certificates(game_id)
    platform_list = get_game_platforms(game_id)
    language_list = get_game_languages(game_id)
    trailer_list = get_game_trailers(game_id)
    photo_list = get_game_photos(game_id)
    critics_reviews_list = get_critics_reviews(game_id)
    user_reviews_list = get_user_reviews(game_id)
    award_list = get_game_awards(game_id)
    avg_usr_rating_details = get_avg_user_rating(game_id)

    gallery_dict = {"trailers": trailer_list, "photos": photo_list}

    sentimeter_dict = {"positive": game_dict.get("positive"),
                       "negative": game_dict.get("negative"),
                       "neutral": game_dict.get("neutral")}
    # graphics, performance, animation, easeOfUse
    aspects_dict = {"graphics": game_dict.get("aspect_graphics"),
                    "performance": game_dict.get("aspect_performance"),
                    "animation": game_dict.get("aspect_animation"),
                    "easeOfUse": game_dict.get("aspect_easeOfUse"),
                    }

    overview_dict = {"releaseDate": game_dict.get("release_date"),
                     "game": game_dict.get("game"),
                     "developer": game_dict.get("developer"),
                     "provider": game_dict.get("provider"),
                     "ebitsRating": game_dict.get("ebits_rating"),
                     "ebitsReview": game_dict.get("ebits_review"),
                     "ebitsReviewer": game_dict.get("ebits_reviewer_name"),
                     "ebitsReviewerImage": game_dict.get("ebits_reviewer_image"),
                     "averageCriticsRating": game_dict.get("critics_rating"),
                     "platforms": platform_list,
                     "language": language_list,
                     "awards": award_list,
                     "gallery": gallery_dict
                     }

    game_detail = {"id": game_dict.get("id"),
                   "slug": game_dict.get("slug"),
                   "title": game_dict.get("game_name"),
                   "sentimeter": sentimeter_dict,
                   "aspects": aspects_dict,
                   "overview": overview_dict,
                   "genres": genre_list,
                   "certifications": cert_list,
                   "criticReviews": critics_reviews_list,
                   "userReviews": user_reviews_list,
                   "avgUserReviews": avg_usr_rating_details
                   }

    return JsonResponse(game_detail)


def all_moods(request):
    final_query = """ select label_id as name , count(*) as cnt from review_gamepost
      left join review_gametolabel on review_gamepost.id = review_gametolabel.game_id_id
      join  review_gamelabel on  review_gametolabel.label_id = review_gamelabel.name
      and LOWER(review_gamelabel.type) = 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["moods"] = records
    return JsonResponse(js_val)


def all_languages(request):
    data = list(GLanguage.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["languages"] = records
    return JsonResponse(js_val, safe=False)


def all_labels(request):
    final_query = """ select label_id as name , count(*) as cnt from review_gamepost
      left join review_gametolabel on review_gamepost.id = review_gametolabel.game_id_id
      join  review_gamelabel on  review_gametolabel.label_id = review_gamelabel.name
      and LOWER(review_gamelabel.type) != 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["categories"] = records
    return JsonResponse(js_val)


def all_genres(request):
    final_query = """ select genre_id as name , count(*) as cnt from review_gamepost \
     left join review_gametogenre on review_gamepost.id = review_gametogenre.game_id_id group by genre_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["genres"] = records
    return JsonResponse(js_val, safe=False)


def all_platforms(request):
    data = list(GPlatform.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["platforms"] = records
    return JsonResponse(js_val, safe=False)


def all_awards(request):
    data = list(GameAward.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["awards"] = records
    return JsonResponse(js_val, safe=False)


def all_certificates(request):
    data = list(GCertificate.objects.values())
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
    pprint("inside all_reports")
    final_query = """Select
                     review_greport.slug as slug, \
                     review_gamecollection.name as name,\
                     description as summary,\
                     chart_data_json as chart, \
                     review_greport.publish_date \
                     from  review_greport, review_gamecollection \
                     where review_greport.collection_id_id = review_gamecollection.id \
                     order by publish_date desc limit 20
                     """
    row_dict = raw_sql(final_query)
    pprint(row_dict)
    reports = []
    for row in row_dict:
        pprint(type(row.get("chart")))
        r = {'slug': row.get("slug"),
             'name': row.get("name"),
             'summary': row.get("summary"),
             'chart': json.loads(row.get("chart")),
             'chartImage': ''
             }

        reports.append(r)

    return JsonResponse({'reports': reports})


def report_details(request, slug):

    final_query = """Select
                         review_greport.id, \
                         review_greport.collection_id_id as collectionId,\
                         review_gamecollection.name as name,\
                         description as summary,\
                         chart_data_json \
                         from  review_greport, review_gamecollection \
                         where review_greport.collection_id_id = review_gamecollection.id \
                         and   review_greport.slug = '%s'
                         """ % slug
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
    This method returns all the book collection list. See BookCollection model object
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
                         release_date \
                         from  review_gamecollection \
                         where not is_report \
                         order by release_date desc limit 10
                         """

    all_cols = raw_sql(final_query)
    pprint(all_cols)
    if is_empty(all_cols):
        return JsonResponse({})

    final_reponse = []
    count = 0
    for col in all_cols:
        col_id = col.get("id")
        slug = col.get("slug")
        col['type'] = 'game'
        collection_entry_data = get_collection_details(col_id, False)
        col['entries'] = collection_entry_data
        final_reponse.append(col)
        count = count + 1

    return JsonResponse({'collections': final_reponse})


def collection_details(request, slug):

    data = GameCollection.objects.raw("""
                                      SELECT \
                                      id, \
                                      name, \
                                      description, \
                                      image_url \
                                      FROM review_gamecollection
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
    report_predicate = "review_gamecollection.is_report"
    if is_report:
        report_predicate = "review_gamecollection.is_report"
    else:
        report_predicate = "not review_gamecollection.is_report"
    pprint("is_report " + str(is_report))
    final_query = """
                                                SELECT \
                                                review_gamecollectiondetail.slug ,\
                                                game_name, \
                                                game_id_id as game_id, \
                                                ebits_rating as rating, \
                                                review_gamecollectiondetail.description,\
                                                thumbnail_image_url as bgImage, \
                                                review_gamecollectiondetail.release_date as releaseDate, \
                                                aspect_graphics, \
                                                aspect_performance, \
                                                aspect_animation, \
                                                aspect_easeOfUse, \
                                                genres  \
                                                FROM review_gamecollectiondetail, review_gamecollection
                                                where
                                                review_gamecollectiondetail.collection_id_id = review_gamecollection.id
                                                and review_gamecollection.id = '%s' and %s
                                                  """ % (collection_id, report_predicate)

    platform_query = """select review_gplatform.name as platform, \
           review_gplatform.platform_url, \
           review_gplatform.image_url as platform_image_url from review_gplatform where name = '%s'
           """

    game_slug_query = """select review_gamepost.slug as \
        game_slug from review_gamepost where review_gamepost.id = %s """

    pprint(final_query)

    pprint(final_query)
    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        games_slug = ""
        if row.get("game_id", None):
            all_games = raw_sql(game_slug_query % row.get("game_id"))
            if len(all_games) > 0:
                games_slug = all_games[0].get("game_slug")

        entry = {"slug": row.get("slug"),
                 "name": row.get("game_name"),
                 "games_slug": games_slug,
                 "ebitsRatings": row.get("rating"),
                 "aspect_graphics": row.get("aspect_graphics"),
                 "aspect_performance": row.get("aspect_performance"),
                 "aspect_animation": row.get("aspect_animation"),
                 "aspect_easeOfUse": row.get("aspect_easeOfUse"),
                 "image": row.get("bgImage")}

        if row.get("platform_id", None):
            platform_dict = raw_sql(platform_query % row.get("platform_id"))
            entry["platform_details"] = platform_dict

        entries.append(entry)

    return entries


@require_http_methods(["POST"])
def games(request):
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
        filter_clause = filter_clause + " review_gametolabel.label_id in (%s)" % in_clause

    if not is_empty(certificate_list):
        single_quoted_list = map(lambda s: "'" + s + "'", certificate_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gametocertificate.certificate_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_gametocertificate.certificate_id_id in (%s)" % in_clause

    if not is_empty(genre_list):
        single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gametogenre.genre_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_gametogenre.genre_id in (%s)" % in_clause

    if not is_empty(language_list):
        single_quoted_list = map(lambda s: "'" + s + "'", language_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gametolanguage.language_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_gametolanguage.language_id_id in (%s)" % in_clause

    if not is_empty(platform_list):
        single_quoted_list = map(lambda s: "'" + s + "'", platform_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gametoplatform.platform_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_gametoplatform.platform_id in (%s)" % in_clause

    if not is_empty(awards_list):
        single_quoted_list = map(lambda s: "'" + s + "'", awards_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gametoaward.award_name_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_gametoaward.award_name_id in (%s)" % in_clause

    if ebits_rating_range and not is_empty(ebits_rating_range):
        between_clause = "%s and %s " % (ebits_rating_range.get("low"), ebits_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gamepost.ebits_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_gamepost.ebits_rating between %s" % between_clause

    if critics_rating_range and not is_empty(critics_rating_range):
        between_clause = "%s and %s " % (critics_rating_range.get("low"), critics_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_gamepost.critics_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_gamepost.critics_rating between %s" % between_clause

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
              left join review_gametogenre on review_gamepost.id = review_gametogenre.game_id_id \
              left join review_gametolabel on review_gamepost.id = review_gametolabel.game_id_id \
              left join review_gametolanguage on review_gamepost.id = review_gametolanguage.game_id_id \
              left join review_gametocertificate on review_gamepost.id = review_gametocertificate.game_id_id \
              left join review_gametoaward on review_gamepost.id = review_gametoaward.game_id_id \
              left join review_gametoplatform on review_gamepost.id = review_gametoplatform.game_id_id\
    """

    final_query = """
                                  SELECT \
                                  distinct
                                  review_gamepost.id,
                                  review_gamepost.slug,
                                  game_name as Title, \
                                  developer as Developer, \
                                  provider as Provider, \
                                  release_date as ReleaseDate, \
                                  ebits_rating as ebitsRating, \
                                  critics_rating as criticsRating, \
                                  thumbnail_image_url as image \
                                  FROM
                                  review_gamepost \
                                  %s 
                                  WHERE   %s
                                  """ % (join_clause, filter_clause)


    count_query = """
                                      SELECT count(DISTINCT review_gamepost.id) as totalEntries  \
                                      FROM
                                      review_gamepost \
                                      %s 
                                      WHERE   %s
                                      """ % (join_clause, count_clause)

    print(final_query)
    row_dict = raw_sql(final_query)
    count_dict = raw_sql(count_query)

    entries = []
    for row in row_dict:
        photo_dict = get_game_photos(row.get("id"))
        trailer_dict = get_game_trailers(row.get("id"))
        row["photos"] = photo_dict
        row["trailers"] = trailer_dict
        row["genres"] = get_game_genres(row.get("id"))
        entries.append(row)

    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) > 0 else 0
    final_output = {'totalEntries': total_count, 'games': entries}
    return JsonResponse(final_output)


def homepage_games(request):
    label = request.GET.get("label", "")
    if is_empty(label):
        print("retrn from empty")
        return []
    final_query = """
                                      SELECT DISTINCT  \
                                      review_gamepost.id,
                                      review_gamepost.slug,
                                      game_name as Title, \
                                      release_date as RelaseDate, \
                                      ebits_rating as ebitsRating, \
                                      thumbnail_image_url as image \
                              
                                      FROM
                                      review_gamepost \
                                      left join review_gametolabel \
                                      on review_gametolabel.id = review_gametolabel.game_id_id \
                                      WHERE   review_gametolabel.label_id = '%s' \
                                       ORDER BY release_date desc limit 10 """ % label
    print(final_query)                                   

    row_dict = raw_sql(final_query)
    return row_dict


def games_search(request):
    keywords = request.GET["keywords"]
    if is_empty(keywords):
        return JsonResponse({'movies': ""})

    serach_query = """SELECT id, slug,\
     release_date, \
     thumbnail_image_url from review_gamepost where MATCH (game_name, description, ebits_review) \
                      AGAINST ('%s' IN NATURAL LANGUAGE MODE) """

    row_dict = raw_sql(serach_query % keywords)
    entries = []
    for row in row_dict:
        row["genres"] = get_game_genres(row.get("id"))
        entries.append(row)

    return entries
