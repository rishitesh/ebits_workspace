
from django.http import HttpResponse, JsonResponse
from review.BooksViews import book_search
from review.PodcastsViews import podcast_search
from review.views import movie_search


def search(request):
    entries = [movie_search(request), podcast_search(request), book_search(request)]
    return JsonResponse({'result': entries})
