from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ratings = pd.read_csv("hybridrs/dataset/ratings.csv")
if 'timestamp' in ratings.columns:
    ratings.drop('timestamp', axis = 1, inplace=True)
    ratings.to_csv("hybridrs/dataset/ratings.csv", index = False)

movies = pd.read_csv("hybridrs/dataset/movies.csv")
genres_df = movies['genres'].str.get_dummies(sep='|')
movies = pd.concat([movies, genres_df], axis=1)
movies.drop('(no genres listed)', axis=1, inplace=True)
movies.dropna(inplace=True)
movies.to_csv("hybridrs/dataset/movies.csv", index = False)

def content_prep(movies):
    cosine_sim = cosine_similarity(movies.iloc[:, 3:])
    cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['movieId'], columns=movies['movieId'])
    return cosine_sim_df

def collaborative_prep(ratings):
    movie_features = ratings.pivot(index = 'movieId', columns = 'userId', values = 'rating').fillna(0)
    item_similarity = cosine_similarity(movie_features)
    item_similarity[np.isnan(item_similarity)] = 0
    item_predicted_ratings = np.dot(movie_features.T, item_similarity)

    dummy_ratings = ratings.copy()
    dummy_ratings['rating'] = dummy_ratings['rating'].apply(lambda x: 0 if x>=0 else 1)
    dummy_ratings = dummy_ratings.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(1)

    item_final_ratings = np.multiply(item_predicted_ratings, dummy_ratings)
    return item_final_ratings

cosine_sim_df = content_prep(movies)
item_final_ratings = collaborative_prep(ratings)

def new_user(user_id, user_preferences, movies, n):
    user_vector = np.array([1 if genre in user_preferences else 0 for genre in movies.columns[3:]])
    movie_vectors = movies.iloc[:, 3:].values
    similarities = cosine_similarity([user_vector], movie_vectors).flatten()
    movies['similarity'] = similarities
    top_movies = movies.sort_values(by='similarity', ascending=False)
    return top_movies['movieId'].head(n).tolist()

def content_based_recommendation(user_id, cosine_sim_df, ratings):
    cosine_sim_df = cosine_sim_df.copy()
    user_ratings = ratings[ratings['userId'] == user_id]
    top_ratings = user_ratings.sort_values(by='rating', ascending=False)

    top_n_movies = []
    for movie_id in top_ratings['movieId']:
        if movie_id not in cosine_sim_df.index:
            continue
        movie_row = cosine_sim_df.loc[movie_id, :].sort_values(ascending=False)
        top_5_similar = movie_row[1:6].index.tolist()
        top_n_movies.extend(top_5_similar)

    top_n_movies = [movie for movie in top_n_movies if movie not in set(user_ratings) ]
    return top_n_movies


def collaborative_recommendationsfn(user_id, item_final_ratings):
    movie_recc = item_final_ratings.loc[user_id].sort_values(ascending=False)
    movie_recc = movie_recc.index.tolist()
    return movie_recc


def hybrid_recommendations(user_id, top_n=25):
    content_recommendations = content_based_recommendation(user_id, cosine_sim_df, ratings)
    collaborative_recommendations = collaborative_recommendationsfn(user_id, item_final_ratings)
    combined_recommendations = []
    content_set, collab_set = set(content_recommendations), set(collaborative_recommendations)
    
    # print('collab',collaborative_recommendations)

    # Add movies present in both lists first
    both_recommendations = list(content_set.intersection(collab_set))
    both_recommendations = set(both_recommendations)
    
    for rec in content_recommendations:
        if rec in both_recommendations:
            combined_recommendations.append({'movieId': rec, 'recommended_from': 'content'})
            
    for rec in collaborative_recommendations:
        if rec in both_recommendations and rec not in content_set:
            combined_recommendations.append({'movieId': rec, 'recommended_from': 'collaborative'})
            
    # Remove duplicates from both lists
    content_recommendations = [rec for rec in content_recommendations if rec not in both_recommendations]
    collaborative_recommendations = [rec for rec in collaborative_recommendations if rec not in both_recommendations]

    # Add remaining in 3:2 order
    content_idx, collab_idx = 0, 0
    while len(combined_recommendations) < top_n and (content_idx < len(content_recommendations) or collab_idx < len(collaborative_recommendations)):
        for rec in content_recommendations[content_idx:content_idx+3]:
            combined_recommendations.append({'movieId': rec, 'recommended_from': 'content'})
        content_idx += 3

        for rec in collaborative_recommendations[collab_idx:collab_idx+2]:
            combined_recommendations.append({'movieId': rec, 'recommended_from': 'collaborative'})
        collab_idx += 2

    # Truncate to top_n if needed
    return combined_recommendations[:top_n]


@api_view(['GET'])
def get_movies(request):
    user = request.user
    preferences = user.prefrences.split('.') 
    
    n = 25  # Number of recommendations to return, default to 25

    if not preferences:
        return Response({'error': 'No preferences provided'}, status=400)

    if user.id not in ratings['userId'].values:  # Check if the user has ratings
        recommended_ids = new_user(user.id, preferences, movies, n)
        recommended_movies = movies[movies['movieId'].isin(recommended_ids)][['movieId', 'title']].to_dict(orient='records')
        for movie in recommended_movies:
            movie['recommended_from'] = 'content'
    else:
        recommended_items = hybrid_recommendations(user.id, n)
        recommended_movies = []
        for item in recommended_items:
            movie = movies[movies['movieId'] == item['movieId']][['movieId', 'title']].to_dict(orient='records')[0]
            movie['recommended_from'] = item['recommended_from']
            recommended_movies.append(movie)

    return Response({'recommended_movies': recommended_movies})



@api_view(['GET'])
def like_movie(request):
    user_id = request.user.id
    movie_id = request.GET.get('movie_id')
    
    print(user_id, movie_id)
    if not user_id or not movie_id:
        return Response({'error': 'user_id and movie_id are required'}, status=400)

    # Add new entry
    global ratings
    
    if ((ratings['userId'] == user_id) & (ratings['movieId'] == movie_id)).any():
        ratings.loc[(ratings['userId'] == user_id) & (ratings['movieId'] == movie_id), 'rating'] = 5
    else:
        new_entry = {'userId': int(user_id), 'movieId': int(movie_id), 'rating': 5}
        
        new_entry_df = pd.DataFrame([new_entry])  # Create a DataFrame for the new entry
        ratings = pd.concat([ratings, new_entry_df], ignore_index=True)

    # Save to CSV
    ratings.to_csv("hybridrs/dataset/ratings.csv", index=False)
    global item_final_ratings
    item_final_ratings = collaborative_prep(ratings)
    
    return Response({'message': 'Movie liked successfully!'}, status=200)



@api_view(['GET'])
def dislike_movie(request):
    user_id = request.user.id
    movie_id = request.GET.get('movie_id')

    if not user_id or not movie_id:
        return Response({'error': 'user_id and movie_id are required'}, status=400)

    # Update rating to 0 if entry exists
    global ratings
    user_id = int(user_id)
    movie_id = int(movie_id)

    if ((ratings['userId'] == user_id) & (ratings['movieId'] == movie_id)).any():
        ratings.loc[(ratings['userId'] == user_id) & (ratings['movieId'] == movie_id), 'rating'] = 0
    else:
        return Response({'error': 'No existing entry found to dislike'}, status=404)

    # Save to CSV
    ratings.to_csv("hybridrs/dataset/ratings.csv", index=False)
    global item_final_ratings
    item_final_ratings = collaborative_prep(ratings)
    return Response({'message': 'Movie disliked successfully!'}, status=200)
