from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main_movies_page():
    return render_template('index.html')

@app.route("/genres")
def genres_page():
    return render_template('genres.html')  

@app.route("/directors")
def directors_page():
    return render_template('directors.html')

@app.route("/actors")
def actors_page():
    return render_template('actors.html') 

@app.route("/audiences")
def audiences_page():
    return render_template('audiences.html') 

@app.route("/audience_reviews")
def audience_reviews_page():
    return render_template('audience_reviews.html') 

@app.route("/movies_has_directors")
def movies_has_directors_page():
    return render_template('movies_has_directors.html') 

@app.route("/movies_has_actors")
def movies_has_actors_page():
    return render_template('movies_has_actors.html') 

if __name__ == "__main__":
    app.run(debug=True)