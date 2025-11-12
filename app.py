from flask import Flask, json, render_template
from flask_mysqldb import MySQL
from flask import request
import os

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

@app.route("/directors")
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

    return render_template('directors.html', directors = results1, movie_titles = results2, intersection_data = results3)

@app.route("/actors")
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

    return render_template('actors.html', actors = results1, movie_titles = results2, intersection_data = results3) 

@app.route("/audience")
def audiences_page():
    # Audiences query
    query1 = 'SELECT * FROM Audiences;'
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template('audience.html', audiences = results) 

@app.route("/audience_reviews")
def audience_reviews_page():
    # Audience Reviews query
    query1 = 'SELECT * FROM AudienceReviews;'
    cur1 = mysql.connection.cursor()
    cur1.execute(query1)
    results1 = cur1.fetchall()

    # Movies title JOIN query
    query2 = 'SELECT title FROM Movies JOIN AudienceReviews on Movies.idMovie = AudienceReviews.idMovie GROUP BY Movies.idMovie;'
    cur2 = mysql.connection.cursor()
    cur2.execute(query2)
    results2 = cur2.fetchall()

    # Audiences firstName & lastName JOIN query
    query3 = 'SELECT firstName, lastName FROM Audiences JOIN AudienceReviews on Audiences.idAudience = AudienceReviews.idAudience GROUP BY Audiences.idAudience;'
    cur3 = mysql.connection.cursor()
    cur3.execute(query3)
    results3 = cur3.fetchall()

    return render_template('audience_reviews.html', audience_reviews = results1, movie_titles = results2, audience_names = results3) 

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
    app.run(port = 5164, debug=True)