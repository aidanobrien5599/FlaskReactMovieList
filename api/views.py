from flask import Blueprint, jsonify, request
from . import db 
from .models import Movie

main = Blueprint('main', __name__)

@main.route('/add_movie', methods=['POST'])
def add_movie():
    try: 
        movie_data = request.get_json()
        
        rating = int(movie_data.get('rating'))
        
        if rating < 0 or rating > 5:
            return 'Invalid rating', 400 #bad request code
        else:
            new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

            db.session.add(new_movie)
            db.session.commit()

            return 'Done', 201
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)
        

@main.route('/movies', methods=['GET'])
def movies():
    movie_list = Movie.query.all()
    movies = []

    for movie in movie_list:
        movies.append({'title' : movie.title, 'rating' : movie.rating})

    return jsonify({'movies' : movies})

@main.route('/delete_movie/<string:movie_title>', methods=['DELETE'])
def delete_movies(movie_title):
    movie = Movie.query.filter_by(title=movie_title).first()
    if not movie:
        return 'Movie not found', 404
    else:
        db.session.delete(movie)
        db.session.commit()
        return 'Done', 200