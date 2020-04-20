from django import template
from movies.models import Category, Movie


register = template.Library()


@register.simple_tag()
def get_categories():
    """Get all Categories"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count):
    movies = Movie.objects.order_by('pk')[:count]
    return {'last_movies': movies}
