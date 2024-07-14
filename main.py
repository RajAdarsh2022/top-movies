from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from database import db, Movie
from wt_form import UpdateForm, MovieForm
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-movies-collection.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

# CREATE DB
db.init_app(app)

# CREATE TABLE
with app.app_context():
    db.create_all()



@app.route("/")
def home():
    with app.app_context():
        all_movies = list(db.session.execute(db.select(Movie)).scalars())
    
    return render_template("index.html", all_movies=all_movies)

@app.route("/add", methods=['GET', 'POST'])
def add_movie_data():
    movie_form = MovieForm()
    if movie_form.validate_on_submit():

        url = f"https://api.themoviedb.org/3/search/movie"
        print(movie_form.movie_title.data)
        params = {
            "query": movie_form.movie_title.data
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('TMDB_AUTH')}"
        }
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        movies_list = response_data["results"]
        for movie in movies_list:
            print(movie["original_title"])
        return render_template('select.html', movies_list=movies_list)

        
    return render_template("add.html", movie_form=movie_form)


@app.route("/movie/<int:movie_id>")
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_AUTH')}"
    }
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    response_data = response.json()  

    new_movie = Movie(
        title=response_data["original_title"],
        description=response_data["overview"],
        year=response_data["release_date"].split("-")[0],
        img_url=f"https://image.tmdb.org/t/p/w500{response_data['poster_path']}",
    )
    db.session.add(new_movie)
    db.session.commit()
    return "Success! Hope so"



@app.route("/edit", methods=['GET', 'POST'])
def edit_movie_data():
    movie_id = int(request.args.get('movie_id'))

    # with app.app_context():
    #     movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar()
    movie = db.get_or_404(Movie, movie_id)

    update_form = UpdateForm()
    if update_form.validate_on_submit():
        movie.rating = float(update_form.new_rating.data)
        movie.review = update_form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', update_form=update_form, movie=movie)


@app.route("/delete")
def delete_movie_data():
    movie_id = request.args.get('movie_id')
    movie = db.get_or_404(Movie, movie_id)

    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run()
