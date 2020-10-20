# Udacity FullStack Nanodegree Final Project


This repository contains the code base to my solution for [Udacity's Full Stack Nanodegree final project](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044). It is a private API that contains data on actors and movies for casting directors, executive producers, and casting assistants. The API is developed using the python framework Flask, the authentication service AUth0 with a Postgres SQL database

### Directions

#### For Local Development

1. Clone this repository on to your machine and make sure in terminal you ``cd`` into the project directory.

2. Then start a virtual environment. If you don't have the means to do so on your local machine type in this command.

**MacOS and Linux**
```
python3 -m pip install --user virtualenv
```

**Windows**
```
py -m pip install --user virtualenv
```

Now, that you have the virtual environment package installed on your computer. In the project directory, start a virtual environment by typing this command    ``` virtualenv env```

Then to iniate the environment type this command ```source env/bin/activate```.

3. Then install the projects dependencies by typing this command ``` pip install -r requirements.txt```

4. This API utilizes the Postgres SQL database package provided by Heroku, and that is already set up and populated with data.

5. The next step is to start the flask server and you do so by typing this command ```export FLASK_APP=app.py && flask run --reload```.

6. Normally, that would be the final step and you could access the API endpoints using either Postman or curl. However, this API has an authentication layer that needs to be accesssed before being able to access the API points. You'll notice that I've stored JWT Tokens for each role for this API executive producer, casting director, casting associate. I've detailed their permission levels ino the API Endpoint section of this documentation. 

To access each one of these enpoints you'll need to apply these tokens to the headers of each request. 

#### Running tests

1. Since you've set up a testing database in the instructions for local set up you can run unit tests by typing this command ```python test_app.py```.

## API Reference

* **Local Base URL** ```http://127.0.0.1:5000``` 
* **Production Base URL** ```https://stormy-mountain-88605.herokuapp.com```


* **Authentication** I"ve provided three jwt tokens with different levels of access in the ```.env``` file. Feel free to test their levels of access by adding them to the headers of your request.

```executive_token``` has full access to all API endpoints
```director_token``` has access to GET /actors & /movies, DELETE /actors, PATCH /actors & /movies
```associate_token``` has access to GET /actors & /mvoies

### API Endpoint Details

**GET /movies**
* Test ```curl http://127.0.0.1:5000/movies```
* Response:
    ```
    {
    "movies": [
        {
            "actors": [
                {
                    "age": "89",
                    "gender": "male",
                    "id": 2,
                    "movie_id": 2,
                    "name": "Sean Connery"
                }
            ],
            "id": 2,
            "release": "1962",
            "title": "Dr. No"
        },
        {
            "actors": [
                {
                    "age": "74",
                    "gender": "male",
                    "id": 3,
                    "movie_id": 3,
                    "name": "Bing Crosby"
                }
            ],
            "id": 3,
            "release": "1944",
            "title": "Going My Way"
        },
        {
            "actors": [
                {
                    "age": "79",
                    "gender": "male",
                    "id": 4,
                    "movie_id": 4,
                    "name": "Al Pacino"
                }
            ],
            "id": 4,
            "release": "1972",
            "title": "The Godfather"
        },
        {
            "actors": [
                {
                    "age": "80",
                    "gender": "male",
                    "id": 1,
                    "movie_id": 1,
                    "name": "Bill Murray"
                }
            ],
            "id": 1,
            "release": "2003",
            "title": "The Life Aquatic with Steve Zissou"
        }
    ],
    "success": true
    }
    ```

**GET /actors**
* Test ```curl http://127.0.0.1:5000/actors```
* Response:
    ```
    {
    "actors": [
        {
            "age": "89",
            "gender": "male",
            "id": 2,
            "movie_id": 2,
            "name": "Sean Connery"
        },
        {
            "age": "74",
            "gender": "male",
            "id": 3,
            "movie_id": 3,
            "name": "Bing Crosby"
        },
        {
            "age": "79",
            "gender": "male",
            "id": 4,
            "movie_id": 4,
            "name": "Al Pacino"
        },
        {
            "age": "80",
            "gender": "male",
            "id": 1,
            "movie_id": 1,
            "name": "Bill Murray"
        }
    ],
    "success": true
    }
    ```    
    
    **DELETE /actors/<actor_id>**
    * Test ```curl http://127.0.0.1:5000/actors/2 -X DELETE```
    * Response:
        ```
        {
            "deleted": 2, 
            "success": true
        }
        ```
    
    **POST /actors**
    * Test ```curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d { "name": "Marlin Barndo", "age": "80", "gender": "male", "movie_id": 4 }```
    * Response:
        ```
        {
            'success': True,
            'created': 7,
            'new_actor': {
                'name': 'Marlin Brando',
                'age': '80',
                'gender':'male',
                'movie_id': 4
            }
        }
        ```
    **PATCH /actors/<actor_id>**
    * Test ```curl http://127.0.0.1:5000/actors/2 -X PATCH -H "Content-Type: application/json" -d { "age": "81" }```
    * Response:
        ```
        {
            "id": 2, 
            "success": true
        }
        ```
    
        **DELETE /actors/<actor_id>**
    * Test ```curl http://127.0.0.1:5000/actors/2 -X DELETE```
    * Response:
        ```
        {
            "deleted": 2, 
            "success": true
        }
        ```
    
    **POST /movies**
    * Test ```curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d { "name": "Home Alone", "release": "1990" }```
    * Response:
        ```
        {
            'success': True,
            'created': 7,
            'new_movie': {
                'title': 'Home Alone',
                'release': '1990'
                'actors': []
            }
        }
        ```
    **PATCH /movies/<actor_id>**
    * Test ```curl http://127.0.0.1:5000/movies/7 -X PATCH -H "Content-Type: application/json" -d { "release": "2020" }```
    * Response:
        ```
        {
            "id": 2, 
            "success": true
        }
        ```

 ## Contribution
 If anyone is interested in developing this application feel free by making a pull request and starting their own git branch. All contributors are welcomed!
