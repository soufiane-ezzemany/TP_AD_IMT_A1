import json
from graphql import GraphQLError

# get the movie based on the id
def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
        raise GraphQLError("No movie found")

# get a movie based on his title
def movie_with_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
        raise GraphQLError("No movie found")

# get the actor based on the id
def actor_with_id(_,info,_id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor
        raise GraphQLError("No actor found")

def all_movies(_,info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]
# get qll the movies in the db

# update the rating of a movie
def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    wfile.close()
    return newmovie

# update the title of a movie
def update_movie_title(_,info,_id,_title):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['title'] = _title
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    wfile.close()
    return newmovie

# resolver to find the actors inside a movie
def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors

# create a new movie
def create_movie(_,info, _movie):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        # check if the movie id exists
        for movie in movies['movies']:
            if movie['id'] == _movie['id']:
                raise GraphQLError("Movie with same id already exists")
        _movie['rating'] = _movie.get('rating', 0.0)
        print(_movie)
        movies["movies"].append(_movie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile)
    wfile.close()
    return _movie

# delete movie
def delete_movie(_,info,_id):
    newmovies = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        filteredmovies = [movie for movie in movies['movies'] if movie['id'] != _id]
        newmovies['movies'] = filteredmovies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    wfile.close()
    return movies["movies"]