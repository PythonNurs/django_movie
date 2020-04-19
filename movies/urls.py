from django.urls import path
from .views import MovieViews, MovieDetailView


urlpatterns = [
    path('', MovieViews.as_view(), name='movie_list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail')
]
