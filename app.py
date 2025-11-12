from flask import Flask, json, render_template, request
from flask_mysqldb import MySQL
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

def add_director(firstName, lastName, middleName):
    query = "INSERT INTO Directors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values = (firstName, lastName, middleName)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/directors", methods = ['GET', 'POST'])
def directors_page():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        if request.form['middleName'] != '':
            middleName = request.form['middleName']
        else:
            middleName = 'None'
        add_director(firstName, lastName, middleName)
    query = 'SELECT * FROM Directors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('directors.html', directors = results)

def add_actor(firstName, lastName, middleName):
    query = "INSERT INTO Actors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values = (firstName, lastName, middleName)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/actors", methods = ['GET', 'POST'])
def actors_page():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        if request.form['middleName'] != '':
            middleName = request.form['middleName']
        else:
            middleName = 'None'
        add_actor(firstName, lastName, middleName)
    query = 'SELECT * FROM Actors;'
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template('actors.html', actors = results) 

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
    return render_template('audiences.html', audiences = results) 

def add_audience_review(review, stars):
    query = "INSERT INTO Audiences (review, stars) VALUES (%s, %d);"
    values = (review, stars)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/audience_reviews", methods=['GET', 'POST'])
def audience_reviews_page():
    if request.method == 'POST':
        stars = int(request.form['stars'])
        review = request.form['review']
        add_audience_review(review, stars)
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
    app.run(debug=True, port=5100)