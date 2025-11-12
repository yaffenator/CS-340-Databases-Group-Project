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

'''Directors Routes'''

def add_director(firstName, lastName, middleName):
    query = "INSERT INTO Directors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values = (firstName, lastName, middleName)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
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

def add_actor(firstName, lastName, middleName):
    query = "INSERT INTO Actors (firstName, lastName, middleName) VALUES (%s, %s, %s);"
    values = (firstName, lastName, middleName)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
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
    query = "INSERT INTO Audiences (firstName, lastName, middleName, email) VALUES (%s, %s, %s, %s);"
    values = (firstName, lastName, middleName, email)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def delete_audience(idAudience):
    query = "DELETE FROM Audiences WHERE idAudience = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (idAudience,))
    mysql.connection.commit()

def update_audience(firstName, lastName, middleName, email, idAudience):
    query = "UPDATE Audiences SET firstName = %s, lastName = %s, middleName = %s, email = %s WHERE idAudience = %s;"
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
    cur.execute('SELECT * FROM Audiences;')
    results = cur.fetchall()
    return render_template('audiences.html', audiences = results) 

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
    query = 'SELECT * FROM Audiences WHERE idAudience = %s;'
    cur.execute(query, (idAudience,))
    audience = cur.fetchone()
    return render_template('update_audience.html', audience=audience)


@app.route("/audiences/delete/<int:idAudience>", methods = ['POST'])
def delete_audience_route(idAudience):
    delete_audience(idAudience)
    return redirect(url_for('audiences_page'))


'''Audience Review Routes'''

def add_audience_review(idmovie, idaudience, review, stars):
    query = "INSERT INTO AudienceReviews (idMovie, idAudience, review, stars) VALUES (%s, %s, %s, %s);"
    values = (idmovie, idaudience, review, stars)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

def delete_audience_review(idAudienceReview):
    query = "DELETE FROM AudienceReviews WHERE idAudienceReview = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (idAudienceReview,))
    mysql.connection.commit()

def update_audience_review(review, stars, idAudienceReview):
    query = "UPDATE AudienceReviews SET review = %s, stars = %s WHERE idAudienceReview = %s;"
    values = (review, stars, idAudienceReview)
    cur = mysql.connection.cursor()
    cur.execute(query, values)
    mysql.connection.commit()

@app.route("/audience_reviews", methods=['GET', 'POST'])
def audience_reviews_page():
    if request.method == 'POST':
        movie = request.form['movie']
        audience = request.form['audience']
        stars = int(request.form['stars'])
        review = request.form['review']
        add_audience_review(movie, audience, review, stars)
    
    query = 'SELECT * FROM AudienceReviews;'
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
    query = 'SELECT * FROM AudienceReviews WHERE idAudienceReview = %s;'
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