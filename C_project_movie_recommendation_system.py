####################################################################################
# Building a movie recommendations system using movies from tastedive which helps
# us find similar movies(also series,etc). We will then use Omdb to obtain rating
# of the similar movies. At the end we will have a function to enter a list of movies
# and get back similar movies sorted by highest to lowest rotten tomatoes rating
#####################################################################################

# https://tastedive.com/read/api   -testdive api documentation
# test dive key 379353-Supreeth-B8H9MFPG  ---quota 300/hr
import requests
import json

def get_movies_from_tastedive(search):
    """Takes a search query as string and returns a dictionary of 5 similar
    movies with some info about each"""
    queries={"q":search,"type":"movies","limit":"5","k":"379353-Supreeth-B8H9MFPG"}
    resp=requests.get("https://tastedive.com/api/similar",params=queries)
    resp_json=resp.json()
    return resp_json

def extract_movie_titles(movies):
    """Takes a dictionary of movies and extracts the titles of movies"""
    movie_titles=[]
    for movie in movies["Similar"]["Results"]:
        movie_titles.append(movie['Name'])
    return movie_titles

def get_related_titles(movie_titles):
    """Takes in a list of movies, generates 5 similar movies for each and puts
    all those movies into a list with no duplicates"""
    final_with_duplicates=[]
    final=[]
    for title in movie_titles:
        similar_movies=get_movies_from_tastedive(title)
        similar_movie_titles=extract_movie_titles(similar_movies)
        final_with_duplicates.extend(similar_movie_titles)
    for title in final_with_duplicates:
        if title not in final:
            final.append(title)
    return final

#Omdb api documentation- https://www.omdbapi.com/
# Omdb key-    fd464212   --quota 1000/day
def get_movie_data(movie_title):
    """Returns data as dict from Omdb by movie_title(string)"""
    queries={"t":movie_title,"r":"json","apikey":"fd464212"}
    resp=requests.get("http://www.omdbapi.com/",params=queries)
    resp_json=resp.json()
    return resp_json

def get_movie_rating(movie_details):
    """Uses as dict of movie details to return Rotten Tomatoes rating"""
    for rating in movie_details["Ratings"]:
        if rating["Source"]=="Rotten Tomatoes":
            return int(rating['Value'].replace("%",""))
    return 0

def get_sorted_recommendations(movies_l):
    """Input a list of movies to get upto 5 recommendations for each and
    the sorted from highest to lowest rotten tomatoes score. In case of
    tie, reverse alphabetical order used as tie breaker"""
    related_movie_titles=get_related_titles(movies_l)
    sorting_fn=lambda m:(get_movie_rating(get_movie_data(m)),m)
    sorted_movie_titles=sorted(related_movie_titles,key=sorting_fn,reverse=True)
    return sorted_movie_titles

#test
print(get_sorted_recommendations(["Cars, Frozen"]))
