from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Movie


class MovieViews(ListView):
    """List of Film"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
    """Detail of Movie"""
    model = Movie
    slug_field = 'url'
