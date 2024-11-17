from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('api/movies', views.get_movies, name='get_movies'),
    path('api/like', views.like_movie, name='like_movie'),
    path('api/dislike', views.dislike_movie, name='dislike_movie'),
]
