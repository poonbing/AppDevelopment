from wtforms import StringField, TextAreaField, IntegerField, SubmitField, RadioField
from wtforms.validators import Optional, Length, DataRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
import shelve


def retrieve_db(shelve_name, key):
    with shelve.open(shelve_name) as db:
        output = db[key]
    return output

class CreateAccessories(FlaskForm):

    name = StringField(label=('Name of Accessory:'), validators=[DataRequired()])
    brand = StringField(label=('Brand of Accessory:'), validators=[DataRequired(), Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    price = IntegerField(label=('Price of Accessory($):'), validators=[DataRequired(), NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField(label=('Description of Accessory:'), validators=[DataRequired(), Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    picture = StringField(label=('Path of Picture of Accessory:'), validators=[DataRequired()])
    offer = IntegerField(label=('Offer(%):'), validators=[DataRequired(), NumberRange(min=0, max=100, message='Offer must be between %(min)d and %(max)d')])
    submit = SubmitField(label=('Submit'))



class CreateTutorial(FlaskForm):
    name = StringField(label=('Name of Video:'), validators=[DataRequired()])
    difficulty = RadioField(label=('Difficulty Lvl:'), choices=['Beginner', 'Intermediate', 'Advanced'], validators=[DataRequired()])
    type = RadioField(label=('Type of Video:'), choices=['Trick', 'Sleight of Hand', 'Flourishes', 'Non-cards'], validators=[DataRequired()])
    video = StringField(label=('Path of video of Tutorial:'), validators=[DataRequired()])
    thumbnail = StringField(label=('Thumbnail Path:'), validators=[DataRequired()])
