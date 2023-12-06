import pandas as pd 
import math
import numpy as np
import csv
import json
from itertools import islice


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_ratings():
    movie_ratings1 = read_json('user_data.json')
    movie_ratings = {key: value for key, value in movie_ratings1.items()}  #converts the the key from string to int 
    return movie_ratings

def get_movies():   
    movies = pd.read_csv('movies.csv')                                                             
    movies['title'] = movies['title'].str.extract('(.+?)\s\(\d{4}\)', expand=False)               #clean up the title from dates 
    movies['title'] = movies['title'].fillna('')                                                  #fills all NULL values 
    return movies



movies = get_movies()
movie_ratings = get_ratings()


def pearson_corr(p1, p2):                   #assuming strings
    #  Params: integer user_ids
    #  Computes the pearson_corr between 2 users
    #  returns a float number 
    #movie_ratings = user_ratings()
    both_rated = {}
    p1_ratings = movie_ratings[p1]        
    p2_ratings = movie_ratings[p2]
    for movie_id in p1_ratings:
        if movie_id in p2_ratings:
            both_rated[movie_id] = 1
    
    len_both_rated = len(both_rated)
    if len_both_rated  == 0:
        return 0

    
    sum_p1 = sum(p1_ratings[movie] for movie in both_rated)
    avg_p1 = sum_p1 / float(len_both_rated)
    sum_p2 = sum(p2_ratings[movie] for movie in both_rated)
    avg_p2 = sum_p2 / float(len_both_rated)
    
    numerator = 0
    sum_squared_p1 = 0
    sum_squared_p2 = 0
    for movie in both_rated:
        numerator += (p1_ratings[movie]-avg_p1)*(p2_ratings[movie]-avg_p2)
        sum_squared_p1 += (p1_ratings[movie]-avg_p1)**2
        sum_squared_p2 += (p2_ratings[movie]-avg_p2)**2
    

    denominator = math.sqrt(sum_squared_p1) * math.sqrt(sum_squared_p2)
    if denominator == 0:
        return 0
    
    correlation = numerator/denominator
    return correlation
        
        
def closest_users(person):
    # Compute pearson corr between persoon against all other users
    # returns a dictionary with user-id : rating_score from
    # most similar to least similar 
    closest = {}
    for user in movie_ratings:
        if user != person:
            correlation = pearson_corr(person, user)
            if correlation > 0:
                closest[user] = correlation
    
    closest_sorted = dict(sorted(closest.items(), key=lambda item: item[1], reverse=True))
    
    return closest_sorted



##Helper function 
def get_movies_by_genre(movies, target_genres):
    movies_by_genres = movies
    for genre in target_genres:
        movies_by_genres = movies_by_genres[movies_by_genres['genres'].str.contains(genre, case=False, na=False)]

    movies_by_genres = movies_by_genres[movies_by_genres['genres'].apply(lambda x: all(genre in x for genre in target_genres))]
    titles = movies_by_genres['title']
    return titles


def recommendation(person):
    if person in movie_ratings:
        others = closest_users(person)
        high_rated_movies = [] 
        user_ratings = movie_ratings[person]  

        for user, correlation in others.items():
            user_rating = movie_ratings[user] 
            for title, rating in user_rating.items():

                if rating >= 2 and  title not in user_ratings and title not in high_rated_movies:
                    high_rated_movies.append(title) 
        
        predicted_ratings = {}
        for movie in high_rated_movies:
            score_numerator = 0
            score_denominator = 0
            
            for user, value in others.items():
                ratings = movie_ratings.get(user, {})
                user_rating_on_movie = ratings.get(movie, 0)
                score_numerator += value * user_rating_on_movie
                score_denominator += value
            
            if score_denominator != 0:
                score = score_numerator / score_denominator
                predicted_ratings[movie] = score
        sorted_predicted = dict(sorted(predicted_ratings.items(), key=lambda item: item[1], reverse=True))
        print("Predicted ratings")
        print(sorted_predicted)
        #print(predicted_ratings)

        #return high_rated_movies, predicted_ratings
    
    else:
        print("You are a new user, we will recommend some of our popular movies.")
        genres = input("Enter genres you like separated by comma: ")
        target_genres = [genre.strip() for genre in genres.split(',')]
        movies_by_genres = get_movies_by_genre(movies, target_genres)
        popular_movies = []
        for user_id, user_rating in movie_ratings.items():
            for title in movies_by_genres:
                if title in user_rating:
                    rating = user_rating[title]
                    if rating > 3.5:
                        popular_movies.append(title)
        print("Here are some of our popular movies: ")
        print(popular_movies)
        #return popular_movies
        return
