from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib
import base64


def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(
            title__icontains=searchTerm
        )
    else:
        movies = Movie.objects.all()

    return render(
        request,
        'home.html',
        {
            'movies': movies,
            'searchTerm': searchTerm
        }
    )


def about(request):
    return render(request, 'about.html')


def signup(request):
    email = request.GET.get('email')

    return render(
        request,
        'signup.html',
        {
            'email': email
        }
    )


def statistics_view(request):
    matplotlib.use('Agg')

    years = Movie.objects.values_list(
        'year',
        flat=True
    ).distinct().order_by('year')

    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5

    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 6))

    plt.bar(
        bar_positions,
        movie_counts_by_year.values(),
        width=bar_width,
        align='center'
    )

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')

    plt.xticks(
        bar_positions,
        movie_counts_by_year.keys(),
        rotation=90
    )

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()

    plt.savefig(
        buffer,
        format='png'
    )

    buffer.seek(0)

    plt.close()

    image_png = buffer.getvalue()

    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    all_movies = Movie.objects.all()

    movie_counts_by_genre = {}

    for movie in all_movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
        else:
            first_genre = "None"

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    genre_positions = range(len(movie_counts_by_genre))

    plt.figure(figsize=(12, 6))

    plt.bar(
        genre_positions,
        movie_counts_by_genre.values(),
        width=bar_width,
        align='center'
    )

    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')

    plt.xticks(
        genre_positions,
        movie_counts_by_genre.keys(),
        rotation=90
    )

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()

    plt.savefig(
        buffer,
        format='png'
    )

    buffer.seek(0)

    plt.close()

    image_png = buffer.getvalue()

    buffer.close()

    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')

    return render(
        request,
        'statistics.html',
        {
            'graphic': graphic,
            'graphic_genre': graphic_genre
        }
    )