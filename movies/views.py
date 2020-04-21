from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Movie, Actor
from .forms import ReviewForm


class MovieViews(ListView):
    """List of Film"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
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


class ActorDetailView(DetailView):
    """Detail of Actor"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'

