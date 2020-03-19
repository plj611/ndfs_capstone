import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Gender, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app, os.getenv('SQLALCHEMY_DATABASE_URI'))

  return app

APP = create_app()

# ADD PAGINATION??

@APP.route('/actors', methods=['GET'])
def get_actors():

  try:
    ans = Actor.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'actors': formatted_ans,      # Add page
          'total_actors': len(formatted_ans),
          'success': True,
  })

@APP.route('/movies', methods=['GET'])
def get_movies():

  try:
    ans = Movie.query.all()
    formatted_ans = []
    for i in ans:
      formatted_ans.append(i.format())
  except:
    abort(422)
  return jsonify({
          'movies': formatted_ans,    # Add page
          'total_movies': len(formatted_ans),
          'success': True,
  })

@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
  error = None
  
  try:
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
  except:
    # processing error
    abort(422)
  
  if actor:
    print('if')
    try:
      actor.delete()
    except:
      # processing error
      abort(422)
  else:
    # actor not found
    print('else')
    abort(404)

  return jsonify({
            'delete': actor_id,
            'success': True,
  })
    
      
@APP.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)