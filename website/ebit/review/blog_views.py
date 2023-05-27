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

    articles_query = """
      select *  from review_blogarticlepost ORDER BY publish_date desc %s 
    """
    articles = raw_sql(articles_query % limit_clause)

    return JsonResponse({'result': articles})


def all_events(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)

    if limit and int(limit) > 50:
        raise Exception('spam', 'Invalid limit clause')

    if offset and int(offset) < 0:
        raise Exception('spam', 'Invalid offset clause')
    limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)

    events_query = """
      select *  from review_blogeventpost ORDER BY publish_date desc %s 
    """
    events = raw_sql(events_query % limit_clause)

    return JsonResponse({'result': events})


def all_interviews(request):
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 20)

    if limit and int(limit) > 50:
        raise Exception('spam', 'Invalid limit clause')

    if offset and int(offset) < 0:
        raise Exception('spam', 'Invalid offset clause')
    limit_clause = " LIMIT %s OFFSET %s " % (limit, offset)

    events_query = """
      select *  from review_bloginterviewpost ORDER BY publish_date desc %s 
    """
    events = raw_sql(events_query % limit_clause)

    return JsonResponse({'result': events})


def article_details(request, slug):
    articles_query = """
          select *  from review_blogarticlepost where slug = '%s' 
        """
    article = raw_sql(articles_query % slug)

    return JsonResponse({'result': article})


def event_details(request, slug):
    event_query = """
          select *  from review_blogeventpost where slug = '%s' 
        """
    event = raw_sql(event_query % slug)

    return JsonResponse({'result': event})


def interview_details(request, slug):
    interview_query = """
          select *  from review_bloginterviewpost where slug = '%s' 
        """
    interview = raw_sql(interview_query % slug)

    return JsonResponse({'result': interview})


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
