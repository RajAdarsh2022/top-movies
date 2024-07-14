from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UpdateForm(FlaskForm):
    new_rating = StringField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    new_review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class MovieForm(FlaskForm):
    movie_title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")