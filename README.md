# SEEnema
_______________________________________________________________________________________________________________________

**Homepage:**

http://127.0.0.1:8000/
Prototype designed, leveraging API's to handle UI.
Incomplete. As of now, just leverages the list api and displays the list of movies.
________________________________________________________________________________________________________________________

**Public APIs:**

1. **Query All Movies:**

GET http://127.0.0.1:8000/api/v1/movies/ 
OR
GET http://127.0.0.1:8000/apis/movies/

2. **Sort movies by Upvotes/Downvotes:**

GET http://127.0.0.1:8000/api/v1/movies/?ordering=downvotes
OR
GET http://127.0.0.1:8000/apis/movies/?ordering=-upvotes

3. **Sort by release date:**

GET http://127.0.0.1:8000/api/v1/movies/?ordering=-release_date 
OR
GET http://127.0.0.1:8000/apis/movies/?ordering=release_date
________________________________________________________________________________________________________________________

**Auth APIs:**

1. **Registration API:**

POST  http://127.0.0.1:8000/apis/user/registration/

Form Data = {'username': 'username', 'email': 'email@email.com', 'password': 'password'}

2. **Login API:**

POST  http://127.0.0.1:8000/apis/user/login/

Form Data = {'username': 'username', 'password': 'password'}
________________________________________________________________________________________________________________________

**Authenticated APIs:**

1. **Add Movie API:**

POST http://127.0.0.1:8000/api/v1/movies/

Form Data= {"name":"the holiday 2","release_date":"2021-11-01","upvotes":20,"downvotes":5
,"review":"good one","genre":1}

2. **Add review to the Movie API:**

PATCH http://127.0.0.1:8000/api/v1/movies/<movie_id>/

Form Data = {review: "add your review"}

3. **Upvote movie API:**

Patch http://127.0.0.1:8000/api/v1/movies/<movie_id>/

Form Data = {upvotes: <any_integer>}

4. **Downvote movie API:**

Patch http://127.0.0.1:8000/api/v1/movies/<movie_id>/

Form Data = {downvotes: <any_integer>}

5. **Get recommendations API:**

GET http://127.0.0.1:8000/api/v1/movies/?genre__id=<userprofiles_genre_id>

6. **Set favourite genre API:**

PATCH http://127.0.0.1:8000/apis/update/user-profile/<user_profile_id/

Form Data = {'favourite_genre': <genre_id>}
________________________________________________________________________________________________________________________

**Tests:**

python manage.py tests

Implemented few simple testcases using rest_framework.test.APITestCase
________________________________________________________________________________________________________________________
