from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


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
    paginate_by = 1


class MovieDetailView(GenreYear, DetailView):
    """Detail of Movie"""
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


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
    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args,  **kwargs):
        content = super().get_context_data(*args, **kwargs)
        content['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        content['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return content


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


class AddRatingStar(View):
    """Add Rating to Movie"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARD_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Search Film"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}"
        return context
