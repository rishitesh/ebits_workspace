import json
from django.http import HttpResponse, JsonResponse
from .utils import raw_sql, user_from_request

from .blog_models import BlogArticlePost, BlogEventPost, BlogInterviewPost, BlogUserLikes
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from datetime import date


def all_articles(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)

    if limit and int(limit) > 50:
        raise Exception('spam', 'Invalid limit clause')

    if offset and int(offset) < 0:
        raise Exception('spam', 'Invalid offset clause')
    limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)

    count_query = """
       select count(*) as totalEntries from review_blogarticlepost 
     """

    count_dict = raw_sql(count_query)
    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) > 0 else 0

    user, token = user_from_request(request) or (None, None)

    user_name = ""
    logged_in_user = False
    if user:
        logged_in_user = True
        user_name = user.username

    articles_query = """
            select title,
            subTitle,
            publish_date,
            slug,
            description1 as description,
            thumbnail_image_url as image,
            likes,
            IF (review_bloguserlikes.id IS NULL, 'false', 'true') as user_liked
            from review_blogarticlepost left outer join review_bloguserlikes on  review_blogarticlepost.slug = review_bloguserlikes.blog_slug
            and review_bloguserlikes.user_name = '%s'
            ORDER BY publish_date desc %s 
    """
    articles = raw_sql(articles_query % (user_name, limit_clause))
    final_output = {'totalEntries': total_count, 'result': articles}
    return JsonResponse(final_output)


def all_events(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)

    if limit and int(limit) > 50:
        raise Exception('spam', 'Invalid limit clause')

    if offset and int(offset) < 0:
        raise Exception('spam', 'Invalid offset clause')
    limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)

    count_query = """
       select count(*) as totalEntries from review_blogeventpost 
     """

    count_dict = raw_sql(count_query)

    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) > 0 else 0

    user, token = user_from_request(request) or (None, None)

    user_name = ""
    if user:
        user_name = user.username

    events_query = """
      select title, subTitle, event_time_start, event_time_end,
      suitableFor, fees,
      organiser_name,
      organiser_profile as organiser_tag,
      thumbnailImage_url as organiser_image,
      publish_date, slug, description1 as description,
      desc_image_url1 as image,
      likes,
      IF (review_bloguserlikes.id IS NULL, 'false', 'true') as user_liked
    from review_blogeventpost left outer join review_bloguserlikes on  review_blogeventpost.slug = review_bloguserlikes.blog_slug
    and review_bloguserlikes.user_name = '%s'
    ORDER BY publish_date desc %s 
    """
    events = raw_sql(events_query % (user_name, limit_clause))
    final_output = {'totalEntries': total_count, 'result': events}
    return JsonResponse(final_output)



def all_interviews(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)

    if limit and int(limit) > 50:
        raise Exception('spam', 'Invalid limit clause')

    if offset and int(offset) < 0:
        raise Exception('spam', 'Invalid offset clause')
    limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)

    count_query = """
           select count(*) as totalEntries from review_bloginterviewpost 
         """

    count_dict = raw_sql(count_query)

    total_count = count_dict[0].get("totalEntries") if count_dict and len(count_dict) > 0 else 0

    user, token = user_from_request(request) or (None, None)

    user_name = ""
    if user:
        user_name = user.username

    events_query = """
      select review_bloginterviewpost.*,
      IF (review_bloguserlikes.id IS NULL, 'false', 'true') as user_liked
      from review_bloginterviewpost left outer join review_bloguserlikes on  review_bloginterviewpost.slug = review_bloguserlikes.blog_slug
      and review_bloguserlikes.user_name = '%s'
      ORDER BY publish_date desc %s 
    """
    interviews = raw_sql(events_query % (user_name, limit_clause))
    final_output = {'totalEntries': total_count, 'result': interviews}
    return JsonResponse(final_output)


def article_details(request, slug):
    articles_query = """
          select *  from review_blogarticlepost where slug = '%s' 
        """
    article = raw_sql(articles_query % slug)
    ret = article[0] if article and len(article) > 0 else {}

    descriptions = []
    response = {"id": ret.get("id"),
                "title": ret.get("title"),
                "publish_date": ret.get("publish_date"),
                "slug": ret.get("slug"),
                "likes": ret.get("likes"),
                "blogger_details": ret.get("blogger_details"),
                "blogger_name": ret.get("blogger_name"),
                "blogger_image": ret.get("blogger_image"),
                "banner_image_url": ret.get("banner_image_url"),
                "thumbnail_image_url": ret.get("thumbnail_image_url"),
                }

    for i in range(1, 11):
        qs = ret.get("description" + str(i))
        if qs and qs != "":
            descriptions_dict = {"description": qs, "desc_image_url": ret.get("desc_image_url" + str(i))}
            descriptions.append(descriptions_dict)

    response["descriptions"] = descriptions
    return JsonResponse({'result': response})


def event_details(request, slug):
    event_query = """
          select *  from review_blogeventpost where slug = '%s' 
        """
    event = raw_sql(event_query % slug)
    ret = event[0] if event and len(event) > 0 else {}

    descriptions = []
    programs = []
    response = {"id": ret.get("id"),
                "title": ret.get("title"),
                "publish_date": ret.get("publish_date"),
                "slug": ret.get("slug"),
                "likes": ret.get("likes"),
                "suitableFor": ret.get("suitableFor"),
                "fees": ret.get("fees"),
                "event_time_end": ret.get("event_time_end"),
                "event_time_start": ret.get("event_time_start"),
                "subTitle": ret.get("subTitle"),
                "organiser_name": ret.get("organiser_name"),
                "organiser_profile": ret.get("organiser_profile"),
                "bannerImage_url": ret.get("bannerImage_url"),
                "thumbnailImage_url": ret.get("thumbnailImage_url"),
                }

    for i in range(1, 11):
        qs = ret.get("description" + str(i))
        if qs and qs != "":
            descriptions_dict = {"description": qs, "desc_image_url": ret.get("desc_image_url" + str(i))}
            descriptions.append(descriptions_dict)

    for i in range(1, 5):
        qs = ret.get("program_name" + str(i))
        if qs and qs != "":
            program_dict = {"program_name": qs, "program_time": ret.get("program_time" + str(i))}
            programs.append(program_dict)

    response["descriptions"] = descriptions
    response["program_details"] = programs
    return JsonResponse({'result': response})


def interview_details(request, slug):
    interview_query = """
          select *  from review_bloginterviewpost where slug = '%s' 
        """
    interview = raw_sql(interview_query % slug)
    ret = interview[0] if interview and len(interview) > 0 else {}

    question_answers = []
    response = {"id": ret.get("id"),
                "title": ret.get("title"),
                "publish_date": ret.get("publish_date"),
                "venue": ret.get("venue"),
                "slug": ret.get("slug"),
                "introduction": ret.get("introduction"),
                "conclusion": ret.get("conclusion"),
                "likes": ret.get("likes"),
                "subTitle": ret.get("subTitle"),
                "bannerImage_url": ret.get("bannerImage_url"),
                "thumbnailImage_url": ret.get("thumbnailImage_url"),
                }

    interviewee_details = {"name": ret.get("interviewee_name1"),
                           "profile": ret.get("interviewee_profile1"),
                           "image": ret.get("interviewee_image1"),

                           }

    interviewer_details = {"name": ret.get("interviewer_name2"),
                           "profile": ret.get("interviewer_profile2"),
                           "image": ret.get("interviewee_image2"),

                           }

    response["interviewer_details"] = interviewer_details
    response["interviewee_details"] = interviewee_details

    for i in range(1, 11):
        qs = ret.get("question" + str(i))
        if qs and qs != "":
            question_answer_dict = {"question": qs, "answer": ret.get("response" + str(i))}
            question_answers.append(question_answer_dict)


    response["question_answers"] = question_answers

    return JsonResponse({'result': response})



@require_http_methods(["POST"])
def add_article_likes(request):
    user, token = user_from_request(request) or (None,None)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
    try:
        article = BlogArticlePost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "article with slug %s not found " % slug})

    user_has_liked = False
    try:
        user_like_on_blog = BlogUserLikes.objects.get(blog_slug=slug, user_name=user.username)
        user_has_liked = True
        user_like_on_blog.delete()
    except ObjectDoesNotExist:
        blog_user_likes = BlogUserLikes.objects.create(
            blog_slug=slug, user_name=user.username, like_date=date.today())
       
        blog_user_likes.save()
        user_has_liked = False
    
    total_likes = article.likes
    if user_has_liked:
        if total_likes:
            total_likes = total_likes - 1
        else:
            total_likes = 0
    else:
        if total_likes:
            total_likes = total_likes + 1
        else:
            total_likes = 1

    article.likes = total_likes
    article.save()
    message = "Successfully added article likes"
    return JsonResponse({"message": message})


@require_http_methods(["POST"])
def add_event_likes(request):
    user, token = user_from_request(request) or (None, None)
    if not user:
        return HttpResponse('Unauthorized', status=401)

    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
   
    try:
        event = BlogEventPost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "event with slug %s not found " % slug})

    user_has_liked = False
    try:
        user_like_on_blog = BlogUserLikes.objects.get(blog_slug=slug, user_name=user.username)
        user_has_liked = True
        user_like_on_blog.delete()
    except ObjectDoesNotExist:
        blog_user_likes = BlogUserLikes.objects.create(
            blog_slug=slug, user_name=user.username, like_date=date.today())
        blog_user_likes.save()
        user_has_liked = False
    
    total_likes = event.likes
    if user_has_liked:
        if total_likes:
            total_likes = total_likes - 1
        else:
            total_likes = 0
    else:
        if total_likes:
            total_likes = total_likes + 1
        else:
            total_likes = 1

    total_likes = event.likes
    if total_likes:
        total_likes = total_likes + 1
    else:
        total_likes = 1
    event.likes = total_likes
    event.save()
    message = "Successfully added event likes"
    return JsonResponse({"message": message})


@require_http_methods(["POST"])
def add_interview_likes(request):
    user, token = user_from_request(request) or (None, None)
    if not user:
        return HttpResponse('Unauthorized', status=401)

    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])

    try:
        interview = BlogInterviewPost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "interview with slug %s not found " % slug})

    user_has_liked = False
    try:
        user_like_on_blog = BlogUserLikes.objects.get(blog_slug=slug, user_name=user.username)
        user_has_liked = True
        user_like_on_blog.delete()
    except ObjectDoesNotExist:
        blog_user_likes = BlogUserLikes.objects.create(
            blog_slug=slug, user_name=user.username, like_date=date.today())
        blog_user_likes.save()
        user_has_liked = False
    
    total_likes = interview.likes
    if user_has_liked:
        if total_likes:
            total_likes = total_likes - 1
        else:
            total_likes = 0
    else:
        if total_likes:
            total_likes = total_likes + 1
        else:
            total_likes = 1

    total_likes = interview.likes
    if total_likes:
        total_likes = total_likes + 1
    else:
        total_likes = 1
    interview.likes = total_likes
    interview.save()
    message = "Successfully added interview likes"
    return JsonResponse({"message": message})
