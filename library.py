import pandas as pd 
import numpy as np
import csv
import recommender


file_name = 'ratings.csv'
movies = recommender.get_movies()
movie_ratings = recommender.get_ratings()

def print_ratings(user_id):
    if user_id in movie_ratings:
        user_ratings = movie_ratings[user_id]
        print("You have rated:")
        for key, value in user_ratings.items():
            print(key, ":", value)
    else:
        print("User not found.")
        
        
def display_movies(word):
    matching_titles = movies[movies['title'].str.contains(word, case=False)]['title']
    for title in matching_titles:
        print(title)
   
def add_new_user(user_id):
    ratings_dic = {}
    movie_ratings[user_id] = ratings_dic
    
def update_rating(user_id, movie_title, new_rating):
    if (1 <= new_rating <= 5): 
        if user_id in movie_ratings:
            user_ratings = movie_ratings[user_id]
            if movie_title in user_ratings:
                user_ratings[movie_title] = new_rating
            else:
                print("You have not rated this movie yet.")
    else:
        print("Invalid rating.")
        
        
        
def delete_rating(user_id, movie_title):
    if user_id in movie_ratings:
        user_ratings = movie_ratings[user_id]
        if movie_title in user_ratings:
            del user_ratings[movie_title]
        else:
            print("You have not rated this movie yet.")
        
   
