from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Movie, Actor, Genre
from .forms import ReviewForm


class GenreYear:
    """Genre and year inside movie"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MovieViews(GenreYear, ListView):
    """List of Film"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


class MovieDetailView(GenreYear, DetailView):
    """Detail of Movie"""
    model = Movie
    slug_field = 'url'


class AddReview(View):
    """Review"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(GenreYear, DetailView):
    """Detail of Actor"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMovie(GenreYear, ListView):
    """Filter Movie"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        )
        return queryset


class JsonFilterMoviesView(ListView):
    """Filter film in json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies': queryset}, safe=False)


