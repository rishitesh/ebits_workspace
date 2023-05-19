import json
from pprint import pprint
from datetime import date

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from review.booksModels import BookPost, BUserReviewDetail, BPlatform, BookAward, BCertificate, \
    BookCollection, BLanguage
from review.bookSerializers import *
from review.utils import format_uuid, is_empty, raw_sql


def index(request):
    template = loader.get_template('review/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_critics_reviews(book_id):
    critics_reviews_query = """select publication_name,\
                                   review_author, \
                                   review_rating, \
                                   review_title, \
                                   review_date, \
                                   critic_review 
                                   from review_bcriticreviewdetail
                                    where book_id_id = '%s' """ % book_id
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


def get_user_reviews(book_id):
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
                                   from review_buserreviewdetail
                                    where book_id_id = '%s' and review_approved is True""" % book_id
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


def get_book_genres(book_id):
    genre_query = """select genre_id from review_booktogenre where book_id_id = '%s' """ % book_id
    genre_rows = raw_sql(genre_query)
    genre_list = []
    for row in genre_rows:
        genre_list.append(row.get("genre_id"))

    return genre_list


def get_book_certificates(book_id):
    certificate_query = """select certificate_id_id from review_booktocertificate where book_id_id = '%s' """ % book_id
    cert_rows = raw_sql(certificate_query)
    cert_list = []
    for row in cert_rows:
        cert_list.append(row.get("certificate_id_id"))

    return cert_list


def get_book_platforms(book_id):
    platform_query = """select platform_id from review_booktoplatform where book_id_id = '%s' """ % book_id
    platform_rows = raw_sql(platform_query)
    platform_list = []
    for row in platform_rows:
        platform_list.append(row.get("book_id"))

    return platform_list


def get_book_languages(book_id):
    language_query = """select language_id_id from review_booktolanguage where book_id_id = '%s' """ % book_id
    language_rows = raw_sql(language_query)
    language_list = []
    for row in language_rows:
        language_list.append(row.get("language_id_id"))

    return language_list


def get_book_trailers(book_id):
    trailer_query = """select trailers_url from review_booktotrailer where book_id_id = '%s' """ % book_id
    trailer_rows = raw_sql(trailer_query)
    trailer_list = []
    for row in trailer_rows:
        trailer_list.append(row.get("trailers"))

    return trailer_list


def get_book_photos(book_id):
    photo_query = """select name, photo_url from review_booktophoto,\
                       review_bphototype \
                       where review_booktophoto.book_id_id=%s \
                       and review_booktophoto.photo_type_id=review_bphototype.id """ % book_id

    photo_rows = raw_sql(photo_query)
    photo_list = []
    for row in photo_rows:
        photo = {"name": row.get("name"), "photo_url": row.get("photo_url")}
        photo_list.append(photo)

    return photo_list


def get_book_awards(book_id):
    award_query = """select award_name_id, award_for from review_booktoaward where book_id_id = '%s' """ \
                  % book_id
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
    user_review = BUserReviewDetail.objects.get(slug=slug)
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
    user_review = BUserReviewDetail.objects.get(slug=slug)
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
    book_query = """select id from review_bookpost where slug='%s' limit 1""" % slug
    book_row = raw_sql(book_query)[0]
    book_id = book_row.get("id")

    review_author = data.get('author', [])
    review_rating = data.get('ratings', [])
    review_title = data.get('title', [])
    review_text = data.get('review', [])
    reviewer_image = data.get('image', [])

    book = BookPost.objects.get(id=book_id)

    if not book:
        message = "Invalid podcast reference"
        return JsonResponse({"message": message})

    user_review = BUserReviewDetail(book_id=book,
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
    book_query = """select id from review_bookpost where slug='%s' limit 1""" % slug
    book_row = raw_sql(book_query)[0]
    book_id = book_row.get("id")

    genre_list = get_book_genres(book_id)

    if is_empty(genre_list):
        return JsonResponse({})

    single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
    in_clause = ",".join(single_quoted_list)
    filter_clause = " review_booktogenre.genre_id in (%s)" % in_clause

    final_query = """
                                      SELECT \
                                      review_bookpost.id as id, 
                                      book_title, \
                                      synopsis, \
                                      author, \
                                      publisher, \
                                      publish_date, \
                                      ebits_rating, \
                                      critics_rating , \
                                      thumbnail_image_url \
                                      FROM 
                                      review_bookpost,\
                                      review_booktogenre

                                      WHERE review_bookpost.id = review_booktogenre.book_id_id \
                                      and review_bookpost.id != '%s' \
                                      and  %s ORDER BY rand()  limit 10
                                      """ % (book_id, filter_clause)
    # print(final_query)
    similar_book_row = raw_sql(final_query)

    similar_book_list = []
    for row in similar_book_row:
        book = {'id': row.get("id"),
                 'title': row.get("book_title"),
                 'synopsis': row.get("synopsis"),
                 'image': row.get("thumbnail_image_url"),
                 'publishDate': row.get("publish_date"),
                 'ebitsRatings': row.get("ebits_rating"),
                 'criticRatings': row.get("critics_rating"),
                 'author': row.get("author"),
                 'publisher': row.get("publisher"),
                 }

        similar_book_list.append(book)

    return JsonResponse({"books": similar_book_list})


def book_details(request, slug):
    formatted_uuid = format_uuid(slug)

    final_query = """
                                      SELECT \
                                      id, 
                                      slug,
                                      book_title, \
                                      isFiction, \
                                      pages, \
                                      publish_date, \
                                      synopsis, \
                                      author,\
                                      publisher,\

                                      ebits_rating,\
                                      ebits_review,\
                                      ebits_reviewer_name,\
                                      ebits_reviewer_image,\
                                      critics_rating,\

                                      positive, \
                                      negative, \
                                      neutral, \

                                      aspect_plot, \
                                      aspect_setting, \
                                      aspect_characters, \
                                      aspect_pointOfView, \
                                      aspect_conflict, \
                                      aspect_premise,\
                                      aspect_structure,\
                                      aspect_styleOfWriting,\
                                      aspect_visuals,\
                                      aspect_takeaway,\
                                      

                                      ebits_rating, \
                                      thumbnail_image_url \
                                      FROM review_bookpost
                                      where slug = '%s' 
                                      """ % slug

    pprint(final_query)
    row_dict = raw_sql(final_query)
    if is_empty(row_dict):
        return JsonResponse({})
    book_dict = row_dict[0]
    book_id = book_dict.get("id")

    genre_list = get_book_genres(book_id)
    cert_list = get_book_certificates(book_id)
    platform_list = get_book_platforms(book_id)
    language_list = get_book_languages(book_id)
    trailer_list = get_book_trailers(book_id)
    photo_list = get_book_photos(book_id)
    critics_reviews_list = get_critics_reviews(book_id)
    user_reviews_list = get_user_reviews(book_id)
    award_list = get_book_awards(book_id)

    gallery_dict = {"trailers": trailer_list, "photos": photo_list}

    sentimeter_dict = {"positive": book_dict.get("positive"),
                       "negative": book_dict.get("negative"),
                       "neutral": book_dict.get("neutral")}
    # plot, setting, characters, point of view, and conflict
    aspects_dict = {"plot": book_dict.get("aspect_plot"),
                    "setting": book_dict.get("aspect_setting"),
                    "characters": book_dict.get("aspect_characters"),
                    "pointOfView": book_dict.get("aspect_pointOfView"),
                    "conflict": book_dict.get("aspect_conflict"),
                    "premise": book_dict.get("aspect_premise"),
                    "structure": book_dict.get("aspect_structure"),
                    "styleOfWriting": book_dict.get("aspect_styleOfWriting"),
                    "visuals": book_dict.get("aspect_visuals"),
                    "takeaway": book_dict.get("aspect_takeaway"),
                    }

    overview_dict = {"publishDate": book_dict.get("publish_date"),
                     "storyline": book_dict.get("description"),
                     "author": book_dict.get("author"),
                     "publisher": book_dict.get("publisher"),

                     "ebitsRating": book_dict.get("ebits_rating"),
                     "ebitsReview": book_dict.get("ebits_review"),
                     "ebitsReviewer": book_dict.get("ebits_reviewer_name"),
                     "ebitsReviewerImage": book_dict.get("ebits_reviewer_image"),
                     "averageCriticsRating": book_dict.get("critics_rating"),
                     "platforms": platform_list,
                     "language": language_list,
                     "awards": award_list,
                     "gallery": gallery_dict
                     }

    book_detail = {"id": book_dict.get("id"),
                    "slug": book_dict.get("slug"),
                    "title": book_dict.get("book_title"),
                    "isFiction": book_dict.get("isFiction"),
                    "pages": book_dict.get("pages"),
                    "sentimeter": sentimeter_dict,
                    "aspects": aspects_dict,
                    "overview": overview_dict,
                    "genres": genre_list,
                    "certifications": cert_list,
                    "criticReviews": critics_reviews_list,
                    "userReviews": user_reviews_list
                    }

    return JsonResponse(book_detail)


def all_moods(request):
    final_query = """ select label_id as name , count(*) as cnt from review_bookpost
      left join review_booktolabel on review_bookpost.id = review_booktolabel.book_id_id
      join  review_booklabel on  review_booktolabel.label_id = review_booklabel.name
      and LOWER(review_booklabel.type) = 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["moods"] = records
    return JsonResponse(js_val)


def all_languages(request):
    data = list(BLanguage.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["languages"] = records
    return JsonResponse(js_val, safe=False)


def all_labels(request):
    final_query = """ select label_id as name , count(*) as cnt from review_bookpost
      left join review_booktolabel on review_bookpost.id = review_booktolabel.book_id_id
      join  review_booklabel on  review_booktolabel.label_id = review_booklabel.name
      and LOWER(review_booklabel.type) != 'mood' group by label_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["categories"] = records
    return JsonResponse(js_val)


def all_genres(request):
    final_query = """ select genre_id as name , count(*) as cnt from review_bookpost \
     left join review_booktogenre on review_bookpost.id = review_booktogenre.book_id_id group by genre_id """
    row_dict = raw_sql(final_query)
    js_val = {}
    records = []
    for d in row_dict:
        datum = {"name": d.get("name"), "count": d.get("cnt")}
        records.append(datum)
    js_val["genres"] = records
    return JsonResponse(js_val, safe=False)


def all_platforms(request):
    data = list(BPlatform.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["platforms"] = records
    return JsonResponse(js_val, safe=False)


def all_awards(request):
    data = list(BookAward.objects.values())
    js_val = {}
    records = []
    for d in data:
        datum = {"name": d.get("name")}
        records.append(datum)
    js_val["awards"] = records
    return JsonResponse(js_val, safe=False)


def all_certificates(request):
    data = list(BCertificate.objects.values())
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
                     review_breport.slug as slug, \
                     review_bookcollection.title as title,\
                     synopsis as summary,\
                     chart_data_json as chart, \
                     review_breport.publish_date \
                     from  review_breport, review_bookcollection \
                     where review_breport.collection_id_id = review_bookcollection.id \
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
                         review_breport.id, \
                         review_breport.collection_id_id as collectionId,\
                         review_bookcollection.title as title,\
                         synopsis as summary,\
                         chart_data_json \
                         from  review_breport, review_bookcollection \
                         where review_breport.collection_id_id = review_bookcollection.id \
                         and   review_breport.slug = '%s'
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
                         title,\
                         synopsis,\
                         image_url , \
                         publish_date \
                         from  review_bookcollection \
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
        col['type'] = 'book'
        collection_entry_data = get_collection_details(col_id, False)
        col['entries'] = collection_entry_data
        final_reponse.append(col)
        count = count + 1

    return JsonResponse({'collections': final_reponse})


def collection_details(request, slug):

    data = BookCollection.objects.raw("""
                                      SELECT \
                                      id, \
                                      title, \
                                      synopsis, \
                                      image_url \
                                      FROM review_bookcollection
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
    report_predicate = "review_bookcollection.is_report"
    if is_report:
        report_predicate = "review_bookcollection.is_report"
    else:
        report_predicate = "not review_bookcollection.is_report"
    pprint("is_report " + str(is_report))
    final_query = """
                                                SELECT \
                                                review_bookcollectiondetail.slug ,\
                                                book_name, \
                                                ebits_rating as rating, \
                                                review_bookcollectiondetail.synopsis,\
                                                thumbnail_image_url as bgImage, \
                                                review_bookcollectiondetail.publish_date as publishDate, \
                                                # #aspects - plot, setting, characters, point of view, and conflict
                                                aspect_plot as plot, \
                                                aspect_setting as setting, \
                                                aspect_characters as characters, \
                                                aspect_pointOfView as pointOfView, \
                                                aspect_conflict as conflict, \
                                                aspect_premise as premise, \
                                                aspect_structure as structure, \
                                                aspect_styleOfWriting as styleOfWriting, \
                                                aspect_visuals as visuals, \
                                                aspect_takeaway as takeaway, \
                                                genres  \
                                                FROM review_bookcollectiondetail, review_bookcollection
                                                where
                                                review_bookcollectiondetail.collection_id_id = review_bookcollection.id
                                                and review_bookcollection.id = '%s' and %s
                                                  """ % (collection_id, report_predicate)
    pprint(final_query)
    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        entry = {"slug": row.get("slug"),
                 "name": row.get("book_name"),
                 "ebitsRatings": row.get("rating"),
                 "image": row.get("bgImage")}
        entries.append(entry)

    return entries


@require_http_methods(["POST"])
def books(request):
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
        filter_clause = filter_clause + " review_booktolabel.label_id in (%s)" % in_clause

    if not is_empty(certificate_list):
        single_quoted_list = map(lambda s: "'" + s + "'", certificate_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_booktocertificate.certificate_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_booktocertificate.certificate_id_id in (%s)" % in_clause

    if not is_empty(genre_list):
        single_quoted_list = map(lambda s: "'" + s + "'", genre_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_booktogenre.genre_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_booktogenre.genre_id in (%s)" % in_clause

    if not is_empty(language_list):
        single_quoted_list = map(lambda s: "'" + s + "'", language_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_booktolanguage.language_id_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_booktolanguage.language_id_id in (%s)" % in_clause

    if not is_empty(platform_list):
        single_quoted_list = map(lambda s: "'" + s + "'", platform_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_booktoplatform.platform_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_booktoplatform.platform_id in (%s)" % in_clause

    if not is_empty(awards_list):
        single_quoted_list = map(lambda s: "'" + s + "'", awards_list)
        in_clause = ",".join(single_quoted_list)
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_booktoaward.award_name_id in (%s)" % in_clause
        else:
            filter_clause = filter_clause + " and review_booktoaward.award_name_id in (%s)" % in_clause

    if ebits_rating_range and not is_empty(ebits_rating_range):
        between_clause = "%s and %s " % (ebits_rating_range.get("low"), ebits_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_bookpost.ebits_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_bookpost.ebits_rating between %s" % between_clause

    if critics_rating_range and not is_empty(critics_rating_range):
        between_clause = "%s and %s " % (critics_rating_range.get("low"), critics_rating_range.get("high"))
        if is_empty(filter_clause):
            filter_clause = filter_clause + " review_bookpost.critics_rating between %s" % between_clause
        else:
            filter_clause = filter_clause + " and review_bookpost.critics_rating between %s" % between_clause

    filter_clause = filter_clause + " ORDER BY publish_date desc "

    if offset_range and not is_empty(offset_range):
        limit = offset_range.get("limit")
        offset = offset_range.get("offset")
        if limit and int(limit) > 50:
            raise Exception('spam', 'Invalid limit clause')

        if offset and int(offset) < 0:
            raise Exception('spam', 'Invalid offset clause')

        limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)
        filter_clause = filter_clause + limit_clause

    final_query = """
                                  SELECT \
                                  distinct
                                  review_bookpost.id,
                                  review_bookpost.slug,
                                  book_title as Title, \
                                  author as Author, \
                                  publisher as Publisher, \
                                  publish_date as PublishDate, \
                                  ebits_rating as ebitsRating, \
                                  critics_rating as criticsRating, \
                                  thumbnail_image_url as image \
                                  FROM
                                  review_bookpost \
                                  left join review_booktogenre on review_bookpost.id = review_booktogenre.book_id_id \
                                  left join review_booktolabel on review_bookpost.id = review_booktolabel.book_id_id \
                                  left join review_booktolanguage on review_bookpost.id = review_booktolanguage.book_id_id \
                                  left join review_booktocertificate on review_bookpost.id = review_booktocertificate.book_id_id \
                                  left join review_booktoaward on review_bookpost.id = review_booktoaward.book_id_id \
                                  left join review_booktoplatform on review_bookpost.id = review_booktoplatform.book_id_id\
                                  WHERE   %s
                                  """ % filter_clause
    print(final_query)
    row_dict = raw_sql(final_query)

    entries = []
    for row in row_dict:
        photo_dict = get_book_photos(row.get("id"))
        row["photos"] = photo_dict
        entries.append(row)

    return JsonResponse({'books': entries})
