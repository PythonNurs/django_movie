from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actor, Movie, Genre, MovieShort


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name', 'description',)


@register(Actor)
class ActorTranslationOption(TranslationOptions):
    fields = ('name', 'description',)


@register(Movie)
class MovieTranslationOption(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(Genre)
class GenreTranslationOption(TranslationOptions):
    fields = ('name', 'description',)


@register(MovieShort)
class MovieShortTranslationOption(TranslationOptions):
    fields = ('title', 'description',)
