from django.db import models
from datetime import date


class Category(models.Model):
    """Category"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категорий"


class Actor(models.Model):
    """Actor and producer"""
    name = models.CharField('Name', max_length=150)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='actros/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер и режиссер'
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Genre"""
    name = models.CharField('Name', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Movie"""
    title = models.CharField('Title', max_length=150)
    tagline = models.CharField('Tagline', max_length=100, default="")
    description = models.TextField('Description')
    poster = models.ImageField('Poster', upload_to='movie/')
    year = models.PositiveSmallIntegerField('Release date', default=2019)
    country = models.CharField('Country', max_length=150)
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='file_director')
    actors = models.ManyToManyField(Actor, verbose_name='актер', related_name='file_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанр', related_name='file_genres')
    world_premiere = models.DateField('Premiere', default=date.today)
    budget = models.PositiveIntegerField('Budget', default=0, help_text="Indicate the amount in $")
    fees_in_usa = models.PositiveIntegerField('Fees in USA', default=0, help_text="Indicate the amount in $")
    fees_in_world = models.PositiveIntegerField(
        'Fees in the World', default=0, help_text="Indicate the amount in $"
    )
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField('Draft', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = "Фильмы"


class MovieShort(models.Model):
    """Movie short"""
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description')
    image = models.ImageField('Image', upload_to='movie_sort/')
    movie = models.ForeignKey(Movie, verbose_name='Фильмы', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Rating star"""
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("Ip addres", max_length=20)
    star = models.ForeignKey(RatingStar, verbose_name='звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField('Name', max_length=150)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name='фильмы', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

