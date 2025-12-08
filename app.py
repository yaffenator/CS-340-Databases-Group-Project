# -- Citation for the following function: Ayowade Owojori
# -- Date: 11/11/2025
# -- Copied from /OR Adapted from /OR Based on
# -- (Explain degree of originality)
# -- Source URL: https://claude.ai/
# -- if AI tools were used: Given our update and delete functionality for audiences and the audience html
# -- we prompted Claude AI to fix our update and delete functionality. We also used it to fix an error occuring when we passed 
# -- '%d' to insert the number of the stars in the database.
# -- (Explain use of tools and include summary of prompts)
# -- Drop the procedure if it already exists

from flask import Flask, json, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_owojora'
app.config['MYSQL_PASSWORD'] = '5551'
app.config['MYSQL_DB'] = 'cs340_owojora'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def landing_page():
    return render_template('index.html')

def add_movie(title, year, genre, description, directors, actors, rating):
    query1 = "INSERT INTO Movies (title, releaseYear, idGenre, description, averageRating) VALUES (%s, %s, %s, %s, %s);"
    values1 = (title, year, genre, description, rating)
    cur1 = mysql.connection.cursor()
    cur1.execute(query1, values1)

    movie_id = cur1.lastrowid

    for director_id_str in directors:
        director_id = int(director_id_str) 
        query2 = "INSERT INTO Movies_has_Directors (idMovie, idDirector) VALUES (%s, %s)"
        insert_ids = (movie_id, director_id)
        cur1.execute(query2, insert_ids)

    for actor_id_str in actors:
        actor_id = int(actor_id_str)
        query3 = "INSERT INTO Movies_has_Actors (idMovie, idActor) VALUES (%s, %s)"
        insert_ids = (movie_id, actor_id)
        cur1.execute(query3, insert_ids)

    mysql.connection.commit()

@app.route("/reset", methods = ['POST'])
def reset_db_route():
    reset_db()
    return redirect(url_for('landing_page'))

def reset_db():
    query = "CALL sp_reset_moviedb();"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

def delete_movie(idMovie):
    query = "DELETE FROM Movies WHERE idMovie = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (idMovie,))
    mysql.connection.commit()

def update_movie(title, releaseYear, description, averageRating, idMovie):
    query = "UPDATE Movies SET title = %s, releaseYear = %s, description = %s, averageRating = %s WHERE idMovie = %s;"
    values = (title, releaseYear, description, averageRating, idMovie)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/movies", methods = ['GET', 'POST'])
def movies_page():
    # Movies query
    query1 = 'SELECT * FROM Movies;'
    cur1 = mysql.connection.cursor()
    cur1.execute(query1)
    results1 = cur1.fetchall()

    # Genres category JOIN query
    query2 = 'SELECT category FROM Genres JOIN Movies on Genres.idGenre = Movies.idGenre GROUP BY Movies.idGenre;'
    cur2 = mysql.connection.cursor()
    cur2.execute(query2)
    results2 = cur2.fetchall()

    # Directors firstName & lastName JOIN query
    query3 = 'SELECT Directors.idDirector, Directors.firstName, Directors.lastName FROM Directors JOIN Movies_has_Directors ON Directors.idDirector = Movies_has_Directors.idDirector JOIN Movies ON Movies_has_Directors.idMovie = Movies.idMovie;'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    # Movies_has_Directors query (for backend id association)
    query4 = 'SELECT * FROM Movies_has_Directors;'
    cur4 = mysql.connection.cursor()
    cur4.execute(query4)
    results4 = cur4.fetchall()

    # Actors firstName & lastName JOIN query
    query5 = 'SELECT Actors.idActor, Actors.firstName, Actors.lastName FROM Actors JOIN Movies_has_Actors ON Actors.idActor = Movies_has_Actors.idActor JOIN Movies ON Movies_has_Actors.idMovie = Movies.idMovie;'
    cur5 = mysql.connection.cursor()
    cur5.execute(query5)
    results5 = cur5.fetchall()

    # Movies_has_Actors query (for backend id association)
    query6 = 'SELECT * FROM Movies_has_Actors;'
    cur6 = mysql.connection.cursor()
    cur6.execute(query6)
    results6 = cur6.fetchall()

    # Genres query
    query7 = 'SELECT * FROM Genres;'
    cur7 = mysql.connection.cursor()
    cur7.execute(query7)
    results7 = cur7.fetchall()
    genres_lookup = {genre['idGenre']: genre['category'] for genre in results7}

    # Directors query
    query8 = """
    SELECT 
        idDirector, 
        CONCAT_WS(' ', firstName, lastName) AS fullName 
    FROM Directors
    ORDER BY lastName, firstName;
    """
    cur8 = mysql.connection.cursor()
    cur8.execute(query8)
    result8 = cur8.fetchall()

    query9 = """
    SELECT 
        idActor, 
        CONCAT_WS(' ', firstName, lastName) AS fullName 
    FROM Actors
    ORDER BY lastName, firstName;
    """
    cur9 = mysql.connection.cursor()
    cur9.execute(query9)
    result9 = cur9.fetchall()

    if request.method == 'POST':
        title = request.form['title_input']
        year = int(request.form['year_input'])
        genre = int(request.form['genre_selected'])
        description = request.form['description_input']
        directors = request.form.getlist('directors_selected')
        actors = request.form.getlist('actors_selected')
        rating = float(request.form['rating_input'])
        add_movie(title, year, genre, description, directors, actors, rating)
        return redirect(url_for('movies_page'))

    return render_template('movies.html', movies = results1, directors = results3, directors_intersection_data = results4, actors = results5, actors_intersection_data = results6, genres = results7, director_names = result8, actor_names = result9, genres_lookup = genres_lookup)

@app.route("/movies/update/<int:idMovie>", methods = ['GET', 'POST'])
def update_movie_page(idMovie):
    if request.method == 'POST':
        title = request.form['title']
        releaseYear = request.form['releaseYear']
        description = request.form['description']
        averageRating = float(request.form['averageRating'])
        update_movie(title, releaseYear, description, averageRating, idMovie)
        return redirect(url_for('movies_page'))
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM Movies WHERE idMovie = %s;'
    cur.execute(query, (idMovie,))
    movie = cur.fetchone()
    return render_template('update_movie.html', movie=movie)


@app.route("/movies/delete/<int:idMovie>", methods = ['POST'])
def delete_movie_route(idMovie):
    delete_movie(idMovie)
    return redirect(url_for('movies_page'))

'''Genres Route'''

@app.route("/genres")
def genres_page():
    # Genres query
    query = 'SELECT * FROM Genres;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('genres.html', genres = results)

def add_director(firstName, lastName, middleName, movies_directed):
    query1 = "INSERT INTO Directors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values1 = (firstName, lastName, middleName)
    cur1 = mysql.connection.cursor()
    cur1.execute(query1, values1)

    director_id = cur1.lastrowid

    for movie_title in movies_directed:
        # idMovie query
        query2 = "SELECT idMovie FROM Movies WHERE title = %s;"
        cur2 = mysql.connection.cursor()
        cur2.execute(query2, (movie_title,))
        movie_id_result = cur2.fetchone()

        # check that movie_id_result actually exists
        if movie_id_result is None:
            # Handle error (rollback or log error)
            app.logger.error(f"Movie title '{movie_title}' not found. Cannot insert into intersection table.")
            mysql.connection.rollback()
            return

        movie_id = movie_id_result['idMovie']

        query4 = "INSERT INTO Movies_has_Directors (idMovie, idDirector) VALUES (%s, %s)"
        insert_ids = (movie_id, director_id)
        cur4 = mysql.connection.cursor()
        cur4.execute(query4, insert_ids)

    mysql.connection.commit()

def delete_director(idDirector):
    query = "DELETE FROM Directors WHERE idDirector = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (idDirector,))
    mysql.connection.commit()

def update_director(firstName, lastName, middleName, idDirector):
    query = "UPDATE Directors SET firstName = %s, lastName = %s, middleName = %s WHERE idDirector = %s;"
    values = (firstName, lastName, middleName, idDirector)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/directors", methods = ['GET', 'POST'])
def directors_page():
    # Directors query
    query1 = 'SELECT * FROM Directors;'
    cur1 = mysql.connection.cursor()
    cur1.execute(query1)
    results1 = cur1.fetchall()

    # Movies title JOIN query
    query2 = 'SELECT Movies.idMovie, Movies.title FROM Movies JOIN Movies_has_Directors ON Movies.idMovie = Movies_has_Directors.idMovie JOIN Directors ON Movies_has_Directors.idDirector = Directors.idDirector GROUP BY Movies.idMovie'
    cur2 = mysql.connection.cursor()
    cur2.execute(query2)
    results2 = cur2.fetchall()

    # Movies_has_Directors query (for backend id association)
    query3 = 'SELECT * FROM Movies_has_Directors'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    # Movies query (for adding a new director)
    query4 = 'SELECT * FROM Movies'
    cur4 = mysql.connection.cursor()
    cur4.execute(query4)
    results4 = cur4.fetchall()

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        if request.form['middleName'] != '':
            middleName = request.form['middleName']
        else:
            middleName = 'None'
        movies_directed = request.form.getlist('movies_directed')
        add_director(firstName, lastName, middleName, movies_directed)
        return redirect(url_for('directors_page'))

    return render_template("directors.html", directors = results1, movie_titles = results2, intersection_data = results3, movies = results4)

@app.route("/directors/update/<int:idDirector>", methods = ['GET', 'POST'])
def update_director_page(idDirector):
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        update_director(firstName, lastName, middleName, idDirector)
        return redirect(url_for('directors_page'))   
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM Directors WHERE idDirector = %s;'
    cur.execute(query, (idDirector,))
    director = cur.fetchone()
    return render_template('update_director.html', director=director)


@app.route("/directors/delete/<int:idDirector>", methods = ['POST'])
def delete_director_route(idDirector):
    delete_director(idDirector)
    return redirect(url_for('directors_page'))

'''Actors Routes'''

def add_actor(firstName, lastName, middleName, movie_appearances):
    query = "INSERT INTO Actors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values = (firstName, lastName, middleName)
    cur1 = mysql.connection.cursor()
    cur1.execute(query, values)

    actor_id = cur1.lastrowid

    for movie_title in movie_appearances:
        # idMovie query
        query2 = "SELECT idMovie FROM Movies WHERE title = %s;"
        cur2 = mysql.connection.cursor()
        cur2.execute(query2, (movie_title,))
        movie_id_result = cur2.fetchone()

        # check that movie_id_result actually exists
        if movie_id_result is None:
            # Handle error (rollback or log error)
            app.logger.error(f"Movie title '{movie_title}' not found. Cannot insert into intersection table.")
            mysql.connection.rollback()
            return

        movie_id = movie_id_result['idMovie']

        query4 = "INSERT INTO Movies_has_Actors (idMovie, idActor) VALUES (%s, %s)"
        insert_ids = (movie_id, actor_id)
        cur4 = mysql.connection.cursor()
        cur4.execute(query4, insert_ids)

    mysql.connection.commit()

def delete_actor(idActor):
    query = "DELETE FROM Actors WHERE idActor = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (idActor,))
    mysql.connection.commit()

def update_actor(firstName, lastName, middleName, idActor):
    query = "UPDATE Actors SET firstName = %s, lastName = %s, middleName = %s WHERE idActor = %s;"
    values = (firstName, lastName, middleName, idActor)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/actors", methods = ['GET', 'POST'])
def actors_page():
    # Actors query
    query1 = 'SELECT * FROM Actors;'
    cur1 = mysql.connection.cursor()
    cur1.execute(query1)
    results1 = cur1.fetchall()

    # Movies title JOIN query
    query2 = 'SELECT Movies.idMovie, Movies.title FROM Movies JOIN Movies_has_Actors ON Movies.idMovie = Movies_has_Actors.idMovie JOIN Actors ON Movies_has_Actors.idActor = Actors.idActor GROUP BY Movies.idMovie'
    cur2 = mysql.connection.cursor()
    cur2.execute(query2)
    results2 = cur2.fetchall()

    # Movies_has_Actors query (for backend id association)
    query3 = 'SELECT * FROM Movies_has_Actors'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    # Movies query (for adding a new actor)
    query4 = 'SELECT * FROM Movies'
    cur4 = mysql.connection.cursor()
    cur4.execute(query4)
    results4 = cur4.fetchall()

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        if request.form['middleName'] != '':
            middleName = request.form['middleName']
        else:
            middleName = 'None'
        movie_appearances = request.form.getlist('movie_appearances')
        add_actor(firstName, lastName, middleName, movie_appearances)
        return redirect(url_for('actors_page'))

    return render_template('actors.html', actors = results1, movie_titles = results2, intersection_data = results3, movies = results4) 

@app.route("/actors/update/<int:idActor>", methods = ['GET', 'POST'])
def update_actor_page(idActor):
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        update_actor(firstName, lastName, middleName, idActor)
        return redirect(url_for('actors_page'))   
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM Actors WHERE idActor = %s;'
    cur.execute(query, (idActor,))
    actor = cur.fetchone()
    return render_template('update_actor.html', actor=actor)


@app.route("/actors/delete/<int:idActor>", methods = ['POST'])
def delete_actor_route(idActor):
    delete_actor(idActor)
    return redirect(url_for('actors_page'))

'''Audiences Routes'''

def add_audience(firstName, lastName, middleName, email):
    query = "CALL sp_add_audience(%s, %s, %s, %s);"
    values = (firstName, lastName, middleName, email)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def delete_audience(idAudience):
    query = "CALL sp_delete_audience(%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (idAudience,))
    mysql.connection.commit()

def update_audience(firstName, lastName, middleName, email, idAudience):
    query = "CALL sp_update_audience(%s, %s, %s, %s, %s);"
    values = (firstName, lastName, middleName, email, idAudience)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/audiences", methods = ['GET', 'POST'])
def audiences_page():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        email = request.form['email']
        add_audience(firstName, lastName, middleName, email)
    cur = mysql.connection.cursor()
    cur.execute('CALL sp_get_all_audiences();')
    results = cur.fetchall()
    return render_template('audience.html', audiences = results) 

@app.route("/audiences/update/<int:idAudience>", methods = ['GET', 'POST'])
def update_audience_page(idAudience):
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        email = request.form['email']
        update_audience(firstName, lastName, middleName, email, idAudience)
        return redirect(url_for('audiences_page'))   
    cur = mysql.connection.cursor()
    query = 'CALL sp_get_audience_by_id(%s)'
    cur.execute(query, (idAudience,))
    audience = cur.fetchone()
    return render_template('update_audience.html', audience=audience)


@app.route("/audiences/delete/<int:idAudience>", methods = ['POST'])
def delete_audience_route(idAudience):
    delete_audience(idAudience)
    return redirect(url_for('audiences_page'))


'''Audience Review Routes'''

def add_audience_review(idmovie, idaudience, review, stars):
    query = "CALL sp_add_audience_review(%s, %s, %s, %s);"
    values = (idmovie, idaudience, review, stars)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def delete_audience_review(idAudienceReview):
    query = "CALL sp_delete_audience_review(%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (idAudienceReview,))
    mysql.connection.commit()

def update_audience_review(review, stars, idAudienceReview):
    query = "CALL sp_update_audience_review(%s, %s, %s);"
    values = (review, stars, idAudienceReview)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/audience_reviews", methods=['GET', 'POST'])
def audience_reviews_page():
    # Audience Reviews query
    query1 = 'SELECT * FROM AudienceReviews;'
    cur1 = mysql.connection.cursor()
    cur1.execute(query1)
    results1 = cur1.fetchall()

    # Movies title JOIN query
    query2 = 'SELECT title, Movies.idMovie FROM Movies JOIN AudienceReviews on Movies.idMovie = AudienceReviews.idMovie GROUP BY Movies.idMovie;'
    cur2 = mysql.connection.cursor()
    cur2.execute(query2)
    results2 = cur2.fetchall()

    # Audiences firstName & lastName JOIN query
    query3 = 'SELECT firstName, lastName, Audiences.idAudience FROM Audiences JOIN AudienceReviews on Audiences.idAudience = AudienceReviews.idAudience GROUP BY Audiences.idAudience;'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    if request.method == 'POST':
        movie = request.form['movie']
        audience = request.form['audience']
        stars = int(request.form['stars'])
        review = request.form['review']
        add_audience_review(movie, audience, review, stars)
    
    query = 'CALL sp_get_all_audience_reviews();'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()

    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM Movies;')
    results2 = cur2.fetchall()

    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM Audiences;')
    results3 = cur3.fetchall()

    return render_template('audience_reviews.html', audience_reviews = results, movies = results2, audiences = results3) 

@app.route("/audiences_reviews/update/<int:idAudienceReview>", methods = ['GET', 'POST'])
def update_audience_review_page(idAudienceReview):
    if request.method == 'POST':
        stars = int(request.form['stars'])
        review = request.form['review']
        update_audience_review(review, stars, idAudienceReview)
        return redirect(url_for('audience_reviews_page'))   
    cur = mysql.connection.cursor()
    query = 'CALL sp_get_audience_review_by_id(%s);'
    cur.execute(query, (idAudienceReview,))
    audience_review = cur.fetchone()
    return render_template('update_audience_review.html', audience_review=audience_review)

@app.route("/audiences_reviews/delete/<int:idAudienceReview>", methods = ['POST'])
def delete_audience_review_route(idAudienceReview):
    delete_audience_review(idAudienceReview)
    return redirect(url_for('audience_reviews_page'))

'''Movie Has Directors Intersection Table'''

@app.route("/movies_has_directors")
def movies_has_directors_page():
    query = 'SELECT * FROM Movies_has_Directors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('movies_has_directors.html', results = results) 

@app.route("/movies_has_actors")
def movies_has_actors_page():
    query = 'SELECT * FROM Movies_has_Actors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('movies_has_actors.html', results = results)

if __name__ == "__main__":
    app.run(debug=True, port=5100)
