
from django.http import HttpResponse, JsonResponse
from review.BooksViews import book_search, homepage_books
from review.PodcastsViews import podcast_search, homepage_podcasts
from review.views import movie_search, homepage_movies
from review.gamesViews import games_search, homepage_games
from . import views, PodcastsViews, BooksViews, gamesViews


def search(request):
    entries = {}
    movies = movie_search(request)
    entries["movies"] = movies
    podcasts = podcast_search(request)
    entries["podcasts"] = podcasts
    books = book_search(request)
    entries["books"] = books
    games = games_search(request)
    entries["games"] = games
    {'result': entries}


def post_entries(request):
    entries = {}
    movies = homepage_movies(request)
    entries["movies"] = movies
    podcasts = homepage_podcasts(request)
    entries["podcasts"] = podcasts
    books = homepage_books(request)
    entries["books"] = books
    games = homepage_games(request)
    entries["games"] = games
    return JsonResponse({'result': entries})


def reports(request):
    entries = {}
    movies = views.all_reports(request)
    entries["movie_reports"] = movies.get("reports")
    podcasts = PodcastsViews.all_reports(request)
    entries["podcast_reports"] = podcasts.get("reports")
    books = BooksViews.all_reports(request)
    entries["book_reports"] = books.get("reports")
    games = gamesViews.all_reports(request)
    entries["game_reports"] = games.get("reports")
    return JsonResponse({'result': entries})


def collections(request):
    entries = {}
    movies = views.all_collections(request)
    entries["movie_collections"] = movies.get("collections")
    podcasts = PodcastsViews.all_collections(request)
    entries["podcast_collections"] = podcasts.get("collections")
    books = BooksViews.all_collections(request)
    entries["book_collections"] = books.get("collections")
    games = gamesViews.all_collections(request)
    entries["game_collections"] = games.get("collections")
    return JsonResponse({'result': entries})