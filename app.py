
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={'/': {'origins': '*'}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE OPTIONS')
    return response
  
  # Get all actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get actors')
  def get_actors(payload):
    actors = Actor.query.all()
    all_actors = [actor.format() for actor in actors]

    try:
      return jsonify({
        'success': True,
        'actors': all_actors
      })
    except:
      abort(404)
  

  # Get all movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get movies')
  def get_movies(payload):
    movies = Movie.query.all()
    all_movies = [movie.format() for movie in movies]

    # get the actors data for each movie
    for movie in all_movies:
      movie['actors'] = [i.format() for i in movie['actors']]

    try:
      return jsonify({
        'success': True,
        'movies': all_movies
      })
    except:
      abort(400)
  
  # create a new movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('add movie')
  def new_movie(payload):
    try:
      body = request.get_json()
      title = body.get('title', None)
      release = body.get('release', None)
      
      movie = Movie(title=title, release=release)
      movie.insert()
      
    except:
      abort(422)

    finally:
      new_movie = Movie.query.get(movie.id)
      new_movie = new_movie.format()

      return jsonify({
        'success': True,
        'created': movie.id,
        'new_movie': new_movie
      })

  # create an actor
  @app.route('/actors', methods=['POST'])
  @requires_auth('create actor')
  def new_actor(payload):
    try:
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      movie_id = body.get('movie_id', None)

      actor = Actor(name=name, age=age, movie_id=movie_id)
      actor.insert()

    except:
      abort(422)
    
    finally:
      new_actor = Actor.query.get(actor.id)
      new_actor = new_actor.format()

      return jsonify({
        'success': True,
        'created': actor.id,
        'new_actor': new_actor
      })
  
  # delete movie
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete movie')
  def delete_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        movie.delete()
    except:
        abort(422)
    finally:
        return jsonify({
          'success': True,
          'delete': id
        })
  
  # delete actor
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete actor')
  def delete_actor(payload, id):
    try:
      actor = Actor.query.get(id)
      actor.delete()
    except:
      abort(422)
    finally:
      return jsonify({
        'success': True,
        'delete': id
      })
  
  # patch movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('edit movie')
  def patch_movie(payload, id):
    try:
      movie = Movie.query.get(id)
      body = request.get_json()
      title = body.get('title')
      release = body.get('release')
      
      if title is not None:
        movie.title = title
      
      if release is not None:
        movie.release = release
      
      movie.update()
    except:
      abort(400)
    finally:
      return jsonify({
        'success': True,
        'id': id
      })
  
  # patch actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('edit actor')
  def patch_actor(payload, id):
    try:
      actor = Actor.query.get(id)
      body = request.get_json()
      name = body.get('name')
      gender = body.get('gender')
      age = body.get('age')

      if name is not None:
        actor.name = name
      
      if gender is not None:
        actor.gender = gender
      
      if age is not None:
        actor.age = age
      
      actor.update()
    except:
      abort(400)
    
    finally:
      return jsonify({
        'success': True,
        'id': id
      })

  
  ## Error Handling
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400
  
  @app.errorhandler(404)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError):
    return jsonify({
        'success': False,
        'error': AuthError.status_code,
        'message': AuthError.error
    }), 401



  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)