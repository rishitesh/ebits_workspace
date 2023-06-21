import json
from django.http import HttpResponse, JsonResponse
from .utils import raw_sql

from .blog_models import BlogArticlePost, BlogEventPost, BlogInterviewPost
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist


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

    articles_query = """
            select title,
            subTitle,
            publish_date,
            slug,
            description1 as description,
            thumbnail_image_url as image,
             likes
            from review_blogarticlepost ORDER BY publish_date desc %s 
    """ 
    articles = raw_sql(articles_query % limit_clause)
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

    events_query = """
      select title, subTitle, event_time_start, event_time_end, suitableFor, fees, organiser_name, organiser_profile as organiser_tag, thumbnailImage_url as organiser_image,  publish_date, slug, description1 as description, desc_image_url1 as image, likes
         from review_blogeventpost ORDER BY publish_date desc %s 
    """
    events = raw_sql(events_query % limit_clause)
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

    events_query = """
      select *  from review_bloginterviewpost ORDER BY publish_date desc %s 
    """
    interviews = raw_sql(events_query % limit_clause)
    final_output = {'totalEntries': total_count, 'result': interviews}
    return JsonResponse(final_output)


def article_details(request, slug):
    articles_query = """
          select *  from review_blogarticlepost where slug = '%s' 
        """
    article = raw_sql(articles_query % slug)
    ret = article[0] if article and len(article) > 0 else {}
    return JsonResponse({'result': ret})


def event_details(request, slug):
    event_query = """
          select *  from review_blogeventpost where slug = '%s' 
        """
    event = raw_sql(event_query % slug)
    ret = event[0] if event and len(event) > 0 else {}
    return JsonResponse({'result': ret})


def interview_details(request, slug):
    interview_query = """
          select *  from review_bloginterviewpost where slug = '%s' 
        """
    interview = raw_sql(interview_query % slug)
    ret = interview[0] if interview and len(interview) > 0 else {}

    return JsonResponse({'result': ret})


@require_http_methods(["POST"])
def add_article_likes(request):
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
    try:
        article = BlogArticlePost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "article with slug %s not found " % slug})
    
    total_likes = article.likes
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
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])
   
    try:
        event = BlogEventPost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "event with slug %s not found " % slug})

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
    data = json.loads(request.body.decode("utf-8"))
    slug = data.get('slug', [])

    try:
        interview = BlogInterviewPost.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "interview with slug %s not found " % slug})

    total_likes = interview.likes
    if total_likes:
        total_likes = total_likes + 1
    else:
        total_likes = 1
    interview.likes = total_likes
    interview.save()
    message = "Successfully added interview likes"
    return JsonResponse({"message": message})
