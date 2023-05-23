
from django.http import HttpResponse, JsonResponse
from review.BooksViews import book_search
from review.PodcastsViews import podcast_search
from review.views import  movie_search


def search(request):
    entries = {}
    movies = movie_search(request)
    entries["movies"] = movies
    podcasts = podcast_search(request)
    entries["podcasts"] = podcasts
    books = book_search(request)
    entries["books"] = books
    return JsonResponse({'result': entries})
