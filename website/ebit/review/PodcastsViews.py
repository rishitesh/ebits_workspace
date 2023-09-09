import json
from pprint import pprint
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.podcastsModels import PodcastPost, PUserReviewDetail, PPlatform, PodcastAward, PCertificate, \
    PodcastCollection, PLanguage
from review.podcastSerializers import *
from review.utils import format_uuid, is_empty, raw_sql


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_critics_reviews(podcast_id):
    critics_reviews_query = """select publication_name,\
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   critic_review 
                                   from review_pcriticreviewdetail
                                    where podcast_id_id = '%s' """ % podcast_id
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


def get_user_reviews(podcast_id):
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
                                   from review_puserreviewdetail
                                    where podcast_id_id = '%s' and review_approved is True order by review_date desc """ % podcast_id
    user_review_rows = raw_sql(user_reviews_query)
    user_reviews_list = []
    for row in user_review_rows:
        user_review = {'authorName': row.get("review_author"),
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


def get_avg_user_rating(podcast_id):
    user_reviews_query = """select avg(review_rating) as avgUserRating, count(*) as totalReviews
                                   from review_puserreviewdetail
                                    where podcast_id_id = '%s' and review_approved is True""" % podcast_id
    avg_user_ratings = raw_sql(user_reviews_query)

    if avg_user_ratings and len(avg_user_ratings) > 0:
        return avg_user_ratings[0]
    else:
        return {}



def get_podcast_genres(podcast_id):
    genre_query = """select genre_id from review_podcasttogenre where podcast_id_id = '%s' """ % podcast_id
    genre_rows = raw_sql(genre_query)
    genre_list = []
    for row in genre_rows:
        genre_list.append(row.get("genre_id"))

    return genre_list


def get_podcast_certificates(podcast_id):
    certificate_query = """select certificate_id_id from review_podcasttocertificate where podcast_id_id = '%s' """ % podcast_id
    cert_rows = raw_sql(certificate_query)
    cert_list = []
    for row in cert_rows:
        cert_list.append(row.get("certificate_id_id"))

    return cert_list


def get_podcast_platforms(podcast_id):
     platform_query = """select platform_id, image_url, platform_url from review_podcasttoplatform, review_pplatform where \
      review_podcasttoplatform.platform_id=review_pplatform.name and \
      podcast_id_id = '%s' """ % podcast_id
     platform_rows = raw_sql(platform_query)
     platform_list = []
     for row in platform_rows:
         platform = {"name": row.get("platform_id"), "url": row.get("image_url"),
                     "platform_url": row.get("platform_url")}
         platform_list.append(platform)

     return platform_list


def get_podcast_languages(podcast_id):
    language_query = """select language_id_id from review_podcasttolanguage where podcast_id_id = '%s' """ % podcast_id
    language_rows = raw_sql(language_query)
    language_list = []
    for row in language_rows:
        language_list.append(row.get("language_id_id"))

    return language_list


def get_podcast_trailers(podcast_id):
    trailer_query = """select trailers_url from review_podcasttotrailer where podcast_id_id = '%s' """ % podcast_id
    trailer_rows = raw_sql(trailer_query)
    trailer_list = []
    for row in trailer_rows:
        trailer_list.append(row.get("trailers_url"))

    return trailer_list

def get_podcast_photos(podcast_id):
    photo_query = """select name, photo_url from review_podcasttophoto,\
                       review_pphototype \
                       where review_podcasttophoto.podcast_id_id=%s \
                       and review_podcasttophoto.photo_type_id=review_pphototype.id """ % podcast_id

    photo_rows = raw_sql(photo_query)
    photo_json = {}
    for row in photo_rows:
        photo_json[row.get("name")] = row.get("photo_url")

    return photo_json


def get_podcast_awards(podcast_id):
    award_query = """select award_name_id, award_for from review_podcasttoaward where podcast_id_id = '%s' """ \
                  % podcast_id
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
    user_review = PUserReviewDetail.objects.get(slug=slug)
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
    user_review = PUserReviewDetail.objects.get(slug=slug)
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
    podcast_query = """select id from review_podcastpost where slug='%s' limit 1""" % slug
    podcast_row = raw_sql(podcast_query)[0]
    podcast_id = podcast_row.get("id")

    review_author = data.get('author', [])
    review_rating = data.get('ratings', [])
    review_title = data.get('title', [])
    review_text = data.get('review', [])
    reviewer_image = data.get('image', [])

    podcast = PodcastPost.objects.get(id=podcast_id)

    if not podcast:
        message = "Invalid podcast reference"
        return JsonResponse({"message": message})

    user_review = PUserReviewDetail(podcast_id=podcast,
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
    podcast_query = """select id from review_podcastpost where slug='%s' limit 1""" % slug
    podcast_row = raw_sql(podcast_query)[0]
    podcast_id = podcast_row.get("id")

    genre_list = get_podcast_genres(podcast_id)

    if is_empty(genre_list):
        return JsonResponse({})

    single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
    in_clause = ",".join(single_quoted_list)
    filter_clause = " review_podcasttogenre.genre_id in (%s)" % in_clause

    final_query = """
                                      SELECT \
                                      review_podcastpost.slug as slug, 
                                      podcast_name, \
                                      duration, \
                                      description, \
                                      podcaster_display_comma_separated, \
                                      release_date, \
                                      ebits_rating, \
                                      critics_rating , \
                                      thumbnail_image_url \
                                      FROM 
                                      review_podcastpost,\
                                      review_podcasttogenre

                                      WHERE review_podcastpost.id = review_podcasttogenre.podcast_id_id \
                                      and review_podcastpost.id != '%s' \
                                      and  %s ORDER BY rand()  limit 10
                                      """ % (podcast_id, filter_clause)
    # print(final_query)
    similar_podcast_row = raw_sql(final_query)

    similar_podcast_list = []
    for row in similar_podcast_row:
        movie = {'slug': row.get("slug"),
                 'title': row.get("podcast_name"),
                 'description': row.get("duration"),
                 'image': row.get("thumbnail_image_url"),
                 'releaseDate': row.get("release_date"),
                 'duration': row.get("review_date"),
                 'ebitsRatings': row.get("ebits_rating"),
                 'criticRatings': row.get("critics_rating"),
                 'podcaster': row.get("podcaster_display_comma_separated"),
                 }

        similar_podcast_list.append(movie)

    return JsonResponse({"podcasts": similar_podcast_list})


def podcast_details(request, slug):
    formatted_uuid = format_uuid(slug)

    final_query = """
                                      SELECT \
                                      id, 
                                      slug,
                                      podcast_name, \
                                      duration, \
                                      release_date, \
                                      description, \
                                      podcaster_display_comma_separated,\

                                      ebits_rating,\
                                      ebits_review,\
                                      ebits_reviewer_name,\
                                      ebits_reviewer_image,\
                                      critics_rating,\

                                      positive, \
                                      negative, \
                                      neutral, \

                                      aspect_introduction, \
                                      aspect_content, \
                                      aspect_audioQuality, \
                                      aspect_voices, \
                                      aspect_outro, \

                                      ebits_rating, \
                                      thumbnail_image_url \
                                      FROM review_podcastpost
                                      where slug = '%s' 
                                      """ % slug

    pprint(final_query)
    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})
    podcast_dict = row_dict[0]
    podcast_id = podcast_dict.get("id")

    genre_list = get_podcast_genres(podcast_id)
    cert_list = get_podcast_certificates(podcast_id)
    platform_list = get_podcast_platforms(podcast_id)
    language_list = get_podcast_languages(podcast_id)
    trailer_list = get_podcast_trailers(podcast_id)
    photo_list = get_podcast_photos(podcast_id)
    critics_reviews_list = get_critics_reviews(podcast_id)
    user_reviews_list = get_user_reviews(podcast_id)
    award_list = get_podcast_awards(podcast_id)
    avg_usr_rating_details = get_avg_user_rating(podcast_id)

    gallery_dict = {"trailers": trailer_list, "photos": photo_list}

    sentimeter_dict = {"positive": podcast_dict.get("positive"),
                       "negative": podcast_dict.get("negative"),
                       "neutral": podcast_dict.get("neutral")}

    aspects_dict = {"introduction": podcast_dict.get("aspect_introduction"),
                    "content": podcast_dict.get("aspect_content"),
                    "audioQuality": podcast_dict.get("aspect_audioQuality"),
                    "voices": podcast_dict.get("aspect_voices"),
                    "outro": podcast_dict.get("aspect_outro"),
                    }

    overview_dict = {"releaseDate": podcast_dict.get("release_date"),
                     "storyline": podcast_dict.get("description"),
                     "podcaster": podcast_dict.get("podcaster_display_comma_separated"),

                     "ebitsRating": podcast_dict.get("ebits_rating"),
                     "ebitsReview": podcast_dict.get("ebits_review"),
                     "ebitsReviewer": podcast_dict.get("ebits_reviewer_name"),
                     "ebitsReviewerImage": podcast_dict.get("ebits_reviewer_image"),
                     "averageCriticsRating": podcast_dict.get("critics_rating"),
                     "platforms": platform_list,
                     "language": language_list,
                     "awards": award_list,
                     "gallery": gallery_dict
                     }

    podcast_detail = {"id": podcast_dict.get("id"),
                    "slug": podcast_dict.get("slug"),
                    "title": podcast_dict.get("podcast_name"),
                    "length": podcast_dict.get("duration"),
                    "sentimeter": sentimeter_dict,
                    "aspects": aspects_dict,
                    "overview": overview_dict,
                    "genres": genre_list,
                    "certifications": cert_list,
                    "criticReviews": critics_reviews_list,
                    "userReviews": user_reviews_list,
                    "avgUserReviews": avg_usr_rating_details
                    }

    return JsonResponse(podcast_detail)


def all_moods(request):
    final_query = """ select label_id as name , count(*) as cnt from review_podcastpost
      left join review_podcasttolabel on review_podcastpost.id = review_podcasttolabel.podcast_id_id
      join  review_podcastlabel on  review_podcasttolabel.label_id = review_podcastlabel.name
      and LOWER(review_podcastlabel.type) = 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["moods"] = records
    return JsonResponse(js_val)


def all_languages(request):
    data = list(PLanguage.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["languages"] = records
    return JsonResponse(js_val, safe=False)


def all_labels(request):
    final_query = """ select label_id as name , count(*) as cnt from review_podcastpost
      left join review_podcasttolabel on review_podcastpost.id = review_podcasttolabel.podcast_id_id
      join  review_podcastlabel on  review_podcasttolabel.label_id = review_podcastlabel.name
      and LOWER(review_podcastlabel.type) != 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["categories"] = records
    return JsonResponse(js_val)


def all_genres(request):
    final_query = """ select genre_id as name , count(*) as cnt from review_podcastpost \
     left join review_podcasttogenre on review_podcastpost.id = review_podcasttogenre.podcast_id_id group by genre_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["genres"] = records
    return JsonResponse(js_val, safe=False)


def all_platforms(request):
    data = list(PPlatform.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["platforms"] = records
    return JsonResponse(js_val, safe=False)


def all_awards(request):
    data = list(PodcastAward.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["awards"] = records
    return JsonResponse(js_val, safe=False)


def all_certificates(request):
    data = list(PCertificate.objects.values())
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
                     review_preport.slug as slug, \
                     review_podcastcollection.name as title,\
                     description as summary,\
                     chart_data_json as chart, \
                     review_preport.publish_date \
                     from  review_preport, review_podcastcollection \
                     where review_preport.collection_id_id = review_podcastcollection.id \
                     order by publish_date desc limit 20
                     """
    row_dict = raw_sql(final_query)
    pprint(row_dict)
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
                         review_preport.id, \
                         review_preport.collection_id_id as collectionId,\
                         review_podcastcollection.name as title,\
                         description as summary,\
                         chart_data_json \
                         from  review_preport, review_podcastcollection \
                         where review_preport.collection_id_id = review_podcastcollection.id \
                         and   review_preport.slug = '%s'
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
                         publish_date \
                         from  review_podcastcollection \
                         where not is_report \
                         order by publish_date desc limit 10
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
        col['type'] = 'podcast'
        collection_entry_data = get_collection_details(col_id, False)
        col['entries'] = collection_entry_data
        final_reponse.append(col)
        count = count + 1

    return JsonResponse({'collections': final_reponse})


def collection_details(request, slug):

    data = PodcastCollection.objects.raw("""
                                      SELECT \
                                      id, \
                                      name, \
                                      description, \
                                      image_url \
                                      FROM review_podcastcollection
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
    report_predicate = "review_podcastcollection.is_report"
    if is_report:
        report_predicate = "review_podcastcollection.is_report"
    else:
        report_predicate = "not review_podcastcollection.is_report"
    pprint("is_report " + str(is_report))
    final_query = """
                                                SELECT \
                                                review_podcastcollectiondetail.slug ,\
                                                podcast_name as title, \
                                                podcast_id_id as podcast_id, \
                                                ebits_rating as rating, \
                                                review_podcastcollectiondetail.description,\
                                                thumbnail_image_url as bgImage, \
                                                release_date as releaseDate, \
                                                aspect_introduction, \
                                                aspect_content, \
                                                aspect_audioQuality, \
                                                aspect_voices, \
                                                aspect_outro, \
                                                genres,  \
                                                platform_id
                                                FROM review_podcastcollectiondetail, review_podcastcollection
                                                where review_podcastcollectiondetail.collection_id_id = review_podcastcollection.id
                                                and review_podcastcollection.id = '%s' and %s
                                                  """ % (collection_id, report_predicate)
    pprint(final_query)
    row_dict = raw_sql(final_query)

    platform_query = """select name  as platform, image_url, platform_url from review_pplatform where \
      review_pplatform.name = '%s' """

    movie_slug_query = """select review_podcastpost.slug as \
     podcast_slug from review_podcastpost where review_podcastpost.id = %s """

    entries = []
    for row in row_dict:
        podcast_slug = ""
        if row.get("podcast_id", None):
            all_podcasts = raw_sql(movie_slug_query % row.get("podcast_id"))
            if len(all_podcasts) > 0:
                podcast_slug = all_podcasts[0].get("podcast_slug")

        entry = {"slug": row.get("slug"),
                 "name": row.get("title"),
                 "podcast_slug": podcast_slug,
                 "ebitsRatings": row.get("rating"),
                 "description": row.get("description"),
                 "release_date": row.get("releaseDate"),
                 "aspect_introduction": row.get("aspect_introduction"),
                 "aspect_content": row.get("aspect_content"),
                 "aspect_audioQuality": row.get("aspect_audioQuality"),
                 "aspect_voices": row.get("aspect_voices"),
                 "aspect_outro": row.get("aspect_outro"),
                 "genres": row.get("genres"),
                 "image": row.get("bgImage")}
        if row.get("platform_id", None):
           platform_dict = raw_sql(platform_query % row.get("platform_id"))
           entry["platform_details"] = platform_dict

        entries.append(entry)

    return entries



@require_http_methods(["POST"])
def podcasts(request):
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
        filter_clause = filter_clause + " review_podcasttolabel.label_id in (%s)" % in_clause

    if not is_empty(certificate_list):
        single_quoted_list = map(lambda s: "'" + s + "'", certificate_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcasttocertificate.certificate_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_podcasttocertificate.certificate_id_id in (%s)" % in_clause

    if not is_empty(genre_list):
        single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcasttogenre.genre_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_podcasttogenre.genre_id in (%s)" % in_clause

    if not is_empty(language_list):
        single_quoted_list = map(lambda s: "'" + s + "'", language_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcasttolanguage.language_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_podcasttolanguage.language_id_id in (%s)" % in_clause

    if not is_empty(platform_list):
        single_quoted_list = map(lambda s: "'" + s + "'", platform_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcasttoplatform.platform_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_podcasttoplatform.platform_id in (%s)" % in_clause

    if not is_empty(awards_list):
        single_quoted_list = map(lambda s: "'" + s + "'", awards_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcasttoaward.award_name_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_podcasttoaward.award_name_id in (%s)" % in_clause

    if ebits_rating_range and not is_empty(ebits_rating_range):
        between_clause = "%s and %s " % (ebits_rating_range.get("low"), ebits_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcastpost.ebits_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_podcastpost.ebits_rating between %s" % between_clause

    if critics_rating_range and not is_empty(critics_rating_range):
        between_clause = "%s and %s " % (critics_rating_range.get("low"), critics_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_podcastpost.critics_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_podcastpost.critics_rating between %s" % between_clause

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
                                  left join review_podcasttogenre on review_podcastpost.id = review_podcasttogenre.podcast_id_id \
                                  left join review_podcasttolabel on review_podcastpost.id = review_podcasttolabel.podcast_id_id \
                                  left join review_podcasttolanguage on review_podcastpost.id = review_podcasttolanguage.podcast_id_id \
                                  left join review_podcasttocertificate on review_podcastpost.id = review_podcasttocertificate.podcast_id_id \
                                  left join review_podcasttoaward on review_podcastpost.id = review_podcasttoaward.podcast_id_id \
                                  left join review_podcasttoplatform on review_podcastpost.id = review_podcasttoplatform.podcast_id_id\
    """

    final_query = """
                                  SELECT \
                                  distinct
                                  review_podcastpost.id,
                                  review_podcastpost.slug,
                                  podcast_name as Title, \
                                  podcaster_display_comma_separated as Podcaster, \
                                  release_date as ReleaseDate, \
                                  ebits_rating as ebitsRating, \
                                  description, \
                                  critics_rating as criticsRating, \
                                  thumbnail_image_url as image \
                                  FROM
                                  review_podcastpost \
                                  %s 
                                  WHERE   %s
                                  """ % (join_clause, filter_clause)

    count_query = """
                                  SELECT \
                                  count(DISTINCT review_podcastpost.id) as totalEntries
                                  FROM
                                  review_podcastpost \
                                  %s 
                                  WHERE   %s
                                  """ % (join_clause, count_clause)

    print(final_query)
    print(count_query)

    count_dict = raw_sql(count_query)
    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        photo_dict = get_podcast_photos(row.get("id"))
        row["photos"] = photo_dict
        trailer_dict = get_podcast_trailers(row.get("id"))
        row["trailers"] = trailer_dict
        row["genres"] = get_podcast_genres(row.get("id"))
        entries.append(row)

    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) > 0 else 0
    final_output = {'totalEntries': total_count, 'podcasts': entries}
    return JsonResponse(final_output)


def homepage_podcasts(request):
    label = request.GET.get("label", "")
    if is_empty(label):
        return []
    final_query = """
                                      SELECT DISTINCT  \
                                      review_podcastpost.id,
                                      review_podcastpost.slug,
                                      podcast_name as Title, \
                                      release_date as ReleaseDate, \
                                      ebits_rating as ebitsRating, \
                                      thumbnail_image_url as image, \
                                      review_podcastpost.duration, \
                                      aspect_introduction, \
                                      aspect_content, \
                                      aspect_audioQuality, \
                                      aspect_voices, \
                                      aspect_outro \
                                      FROM
                                      review_podcastpost \
                                      left join review_podcasttolabel \
                                      on review_podcastpost.id = review_podcasttolabel.podcast_id_id \
                                      WHERE   review_podcasttolabel.label_id = '%s' \
                                       ORDER BY release_date desc limit 10 """ % label

    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        photo_dict = get_podcast_photos(row.get("id"))
        row["photos"] = photo_dict
        row["genres"] = get_podcast_genres(row.get("id"))
        row["platforms"] = get_podcast_platforms(row.get("id"))
        entries.append(row)

    return entries


def podcast_search(request):
    keywords = request.GET["keywords"]
    if is_empty(keywords):
        return JsonResponse({'podcasts': ""})

    serach_query = """SELECT id, slug,\
     duration, \
     release_date, \
     thumbnail_image_url from review_podcastpost where MATCH (podcast_name, description, ebits_review) \
                      AGAINST ('%s' IN NATURAL LANGUAGE MODE) """

    row_dict = raw_sql(serach_query % keywords)

    entries = []
    for row in row_dict:
        row["genres"] = get_podcast_genres(row.get("id"))
        entries.append(row)

    return entries



