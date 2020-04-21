from django.urls import path
from .views import MovieViews, MovieDetailView, AddReview, ActorDetailView, FilterMovie

urlpatterns = [
    path('', MovieViews.as_view(), name='movie_list'),
    path('filter/', FilterMovie.as_view(), name='filter_movie'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', ActorDetailView.as_view(), name='actors_detail'),
]
