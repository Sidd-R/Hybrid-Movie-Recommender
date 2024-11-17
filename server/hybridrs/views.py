from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def like_movie(request):
    movie_id = request.GET.get('movie_id')
    
    
    
    return render(request, 'like_movie.html')
  
  
  
@api_view(['GET'])
def get_movies(request):
  
    user = request.user
    
    prefrences = user.prefrences.split('.')
    
    
    
    return render(request, 'get_movie.html')