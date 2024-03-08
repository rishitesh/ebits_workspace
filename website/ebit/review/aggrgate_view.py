import json
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from review.BooksViews import book_search, homepage_books
from review.PodcastsViews import podcast_search, homepage_podcasts
from review.views import movie_search, homepage_movies
from review.gamesViews import games_search, homepage_games
from . import views, PodcastsViews, BooksViews, gamesViews
from .utils import raw_sql


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
    return JsonResponse({'result': entries})


def post_entries(request):
    entries = {}
    label = request.GET.get("label", "")
    if label == "New And Notable":
        movies = homepage_movies(request)
        entries["movies"] = movies[0:5]
        return JsonResponse({'result': entries})

    movies = homepage_movies(request)
    entries["movies"] = movies
    podcasts = homepage_podcasts(request)
    entries["podcasts"] = podcasts
    books = homepage_books(request)
    entries["books"] = books
    games = homepage_games(request)
    entries["games"] = games
    return JsonResponse({'result': entries})



def send_mail_to(request):
    data = json.loads(request.body.decode("utf-8"))
    name = data.get('name', '')
    email = data.get('email', '')
    company = data.get('company', '')
    designation = data.get('designation', '')
    message = data.get('message', '')

    subject = "Contact Us From : " + str(name) + " - " + str(company) + " - " + str(designation)
    send_mail(subject,
              message,
              email,
              ['rishi80.mishra@gmail.com'], fail_silently=False)
    return JsonResponse({'result': ""})




def reports(request):
    entries = {}
    movies = views.all_reports(request)
    movies_data = json.loads(movies.content)
    entries["movie_reports"] = movies_data.get("reports")
    podcasts = PodcastsViews.all_reports(request)
    podcasts_data = json.loads(podcasts.content)
    entries["podcast_reports"] = podcasts_data.get("reports")
    books = BooksViews.all_reports(request)
    books_data = json.loads(books.content)
    entries["book_reports"] = books_data.get("reports")
    games = gamesViews.all_reports(request)
    games_data = json.loads(games.content)
    entries["game_reports"] = games_data.get("reports")
    return JsonResponse({'result': entries})


def collections(request):
    entries = {}
    movies = views.all_collections(request)
    movies_data = json.loads(movies.content)
    entries["movie_collections"] = movies_data.get("collections")
    podcasts = PodcastsViews.all_collections(request)
    podcasts_data = json.loads(podcasts.content)
    entries["podcast_collections"] = podcasts_data.get("collections")
    books = BooksViews.all_collections(request)
    books_data = json.loads(books.content)
    entries["book_collections"] = books_data.get("collections")
    games = gamesViews.all_collections(request)
    games_data = json.loads(games.content)
    entries["game_collections"] = games_data.get("collections")
    return JsonResponse({'result': entries})


def post_contents(request):
    final_query = """
      select type_name, description from review_posttext
    """
    row_dict = raw_sql(final_query)
    return JsonResponse({'result': row_dict})


def common_images(request):
    query = """
             select type_name, image_url  from review_commonimage
           """
    common_images = raw_sql(query)

    return JsonResponse({'result': common_images})
