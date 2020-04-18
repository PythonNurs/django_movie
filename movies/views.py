from django.views.generic import View
from django.shortcuts import render
from .models import Movie


class MovieViews(View):
    """List of Film"""
    def get(self, request):
        movie = Movie.objects.all()
        return render(request, 'movies/movies.html', {"movie_list": movie})
