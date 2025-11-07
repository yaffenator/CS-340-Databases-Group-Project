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
def main_movies_page():
    query = 'SELECT * FROM Movies;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('index.html', movies = results)

@app.route("/genres")
def genres_page():
    query = 'SELECT * FROM Genres;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('genres.html', genres = results)

@app.route("/directors")
def directors_page():
    query = 'SELECT * FROM Directors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('directors.html', directors = results)

@app.route("/actors")
def actors_page():
    query = 'SELECT * FROM Actors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('actors.html', actors = results) 

@app.route("/audiences")
def audiences_page():
    query = 'SELECT * FROM Audiences;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('audiences.html', audiences = results) 

@app.route("/audience_reviews")
def audience_reviews_page():
    query = 'SELECT * FROM AudienceReviews;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('audience_reviews.html', audience_reviews = results) 

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
    app.run(debug=True)