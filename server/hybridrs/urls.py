from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('movies', views.get_movies, name='get_movies'),
    path('like', views.like_movie, name='like_movie'),
    path('dislike', views.dislike_movie, name='dislike_movie'),
]
