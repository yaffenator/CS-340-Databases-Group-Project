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

@app.route("/movies")
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
    query3 = 'SELECT Directors.firstName, Directors.lastName FROM Directors JOIN Movies_has_Directors ON Directors.idDirector = Movies_has_Directors.idDirector JOIN Movies ON Movies_has_Directors.idMovie = Movies.idMovie;'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    # Movies_has_Directors query (for backend id association)
    query4 = 'SELECT * FROM Movies_has_Directors;'
    cur4 = mysql.connection.cursor()
    cur4.execute(query4)
    results4 = cur4.fetchall()

    # Actors firstName & lastName JOIN query
    query5 = 'SELECT Actors.firstName, Actors.lastName FROM Actors JOIN Movies_has_Actors ON Actors.idActor = Movies_has_Actors.idActor JOIN Movies ON Movies_has_Actors.idMovie = Movies.idMovie;'
    cur5 = mysql.connection.cursor()
    cur5.execute(query5)
    results5 = cur5.fetchall()

    # Movies_has_Actors query (for backend id association)
    query6 = 'SELECT * FROM Movies_has_Actors;'
    cur6 = mysql.connection.cursor()
    cur6.execute(query6)
    results6 = cur6.fetchall()

    return render_template('movies.html', movies = results1, categories = results2, directors = results3, directors_intersection_data = results4, actors = results5, actors_intersection_data = results6)

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

    return render_template('directors.html', directors = results1, movie_titles = results2, intersection_data = results3, movies = results4)
    
def add_actor(firstName, lastName, middleName, movie_appearances):
    app.logger.info("TESTING AGAIN")
    app.logger.info(movie_appearances)
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

def add_audience(firstName, lastName, middleName, email):
    query = "INSERT INTO Audiences (firstName, lastName, middleName, email) VALUES (%s, %s, %s, %s);"
    values = (firstName, lastName, middleName, email)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def update_audience(firstName, lastName, middleName, email, idAudience):
    query = "UPDATE Audiences SET firstName = %s, lastName = %s, middleName = %s, email = %s) WHERE idAudience = %d;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

def delete_audience(idAudience):
    query = "DELETE FROM Audiences WHERE idAudience = %d;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()

@app.route("/audiences", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def audiences_page():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        email = request.form['email']
        add_audience(firstName, lastName, middleName, email)
    elif request.method == 'PUT':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        middleName = request.form['middleName']
        email = request.form['email']
        idAudience = request.form['idAudience']
        update_audience(firstName, lastName, middleName, email, idAudience)
    elif request.method == 'DELETE':
        idAudience = request.form['idAudience']
        delete_audience(idAudience)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Audiences;')
    results = cur.fetchall()
    return render_template('audience.html', audiences = results) 

def add_audience_review(review, stars):
    query = "INSERT INTO Audiences (review, stars) VALUES (%s, %d);"
    values = (review, stars)
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
        stars = int(request.form['stars'])
        review = request.form['review']
        add_audience_review(review, stars)
    
    return render_template('audience_reviews.html', audience_reviews = results1, movies = results2, audiences = results3) 

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
