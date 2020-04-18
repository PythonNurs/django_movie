from django.contrib import admin
from .models import Category, Genre, Movie, MovieShort, Actor, Rating, RatingStar

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShort)
admin.site.register(Actor)
admin.site.register(RatingStar)
admin.site.register(Rating)
