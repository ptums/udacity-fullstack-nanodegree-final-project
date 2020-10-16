
from dotenv import load_dotenv
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Movie, Actor

load_dotenv()

executive_token=os.getenv('executive_token')
executive_token = 'Bearer ' + executive_token
director_token=os.getenv('director_token')
director_token = 'Bearer ' + director_token
false_token = 'Bearer abc123'


class CastingTestCase(unittest.TestCase):
    """ This class represents the casting test case """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        db_password=os.getenv("db_password")
        db_username=os.getenv("db_username")
        database_path_url=os.getenv("database_path_url")
        self.database_path = database_path_url
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Will Smith',
            'age': '33',
            'gender': 'male',
            'movie_id': 4
        }

        self.new_movie = {
            'title': 'Independence Day',
            'release': '1994'
        }
        
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # test all actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': executive_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['actors']), 0)
    
    # test all actors error
    def test_get_actors_error(self):
        res = self.client().get('/actors', headers={'Authorization': false_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
    
    # test all movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': executive_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['movies']), 0)
    
    # test all movies error
    def test_get_movies_error(self):
        res = self.client().get('/movies', headers={'Authorization': false_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
    
    # delete an actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers={'Authorization': executive_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
    
    # delete an actor error
    def test_delete_actor_error(self):
        res = self.client().delete('/actors/2', headers={'Authorization': false_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'invalid_token')
    
    # delete a movies
    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers={'Authorization': executive_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
    
    # delete an movies error
    def test_delete_movies_error(self):
        res = self.client().delete('/movies/2', headers={'Authorization': false_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'invalid_token')
    
    # edit an actor
    def test_edit_actor(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers={'Authorization': executive_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'], 1)

    # edit an actor error
    def test_edit_actor_error(self):
        res = self.client().patch('/actors/1', json=self.new_actor, headers={'Authorization': false_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'invalid_token')
   
    # edit an movie
    def test_edit_movies(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers={'Authorization': executive_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'], 1)

    # edit an movie error
    def test_edit_movie_error(self):
        res = self.client().patch('/movies/1', json=self.new_movie, headers={'Authorization': false_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'invalid_token')

    # test director error privileges
    def test_director_error_privileges(self):
        res = self.client().delete('/movies/2', headers={'Authorization': director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'unauthorized')

    # test director privileges
    def test_director_privileges(self):
        res = self.client().get('/movies', headers={'Authorization': director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['movies']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

