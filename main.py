from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from database import db, Movie
from wt_form import UpdateForm
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

# with app.app_context():
#     new_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():
    with app.app_context():
        all_movies = list(db.session.execute(db.select(Movie)).scalars())
    for movie in all_movies:
        print(f"Movie ID: {movie.id}, Title: {movie.title}, Rating: {movie.rating}, Review: {movie.review}")  

    return render_template("index.html", all_movies=all_movies)

    #Angela's method
    # result = db.session.execute(db.select(Movie))
    # all_movies = list(result.scalars())
    # return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=['GET', 'POST'])
def edit_movie_data():
    movie_id = int(request.args.get('movie_id'))

    # with app.app_context():
    #     movie = db.session.execute(db.select(Movie).filter_by(id=movie_id)).scalar()
    movie = db.get_or_404(Movie, movie_id)

    update_form = UpdateForm()
    if update_form.validate_on_submit():
        print('Updating post route')
        print(update_form.new_rating.data)
        print(update_form.new_review.data)
        movie.rating = float(update_form.new_rating.data)
        movie.review = update_form.new_review.data
        try:
            db.session.flush()  # Explicitly flush the session
            db.session.commit()
            print('Database commit successful')
        except Exception as e:
            print('Database commit failed:', e)
        return redirect(url_for('home'))

    return render_template('edit.html', update_form=update_form, movie=movie)





if __name__ == '__main__':
    app.run()
