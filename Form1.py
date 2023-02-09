from wtforms import StringField, TextAreaField, IntegerField, SubmitField, RadioField, FileField
from wtforms.validators import Optional, Length, DataRequired, NumberRange, ValidationError
import shelve
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


def retrieve_db(shelve_name, key):
    with shelve.open(shelve_name) as db:
        output = db[key]
    return output


class CreateDeckForm(FlaskForm):
    name = StringField('Name of Deck:', [DataRequired()])
    brand = StringField('Brand of Deck:', validators=[DataRequired(), Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    type = RadioField('Type of Deck:', choices=['Luxury', 'Classic', 'Cardistry'], validators=[DataRequired()])
    price = IntegerField('Price of Deck($):', validators=[DataRequired(), NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField('Description of Deck:', validators=[DataRequired(), Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    file = FileField("Image:", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Type Not Allowed!')])
    offer = IntegerField('Offer(%):', validators=[DataRequired(), NumberRange(min=0, max=100, message='Offer must be between %(min)d and %(max)d')])
    submit = SubmitField('Submit')


class UpdateDeckForm(FlaskForm):
    name = StringField('Name of Deck:')
    brand = StringField('Brand of Deck:', validators=[Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    type = RadioField('Type of Deck:', choices=['Luxury', 'Classic', 'Cardistry'])
    price = IntegerField('Price of Deck($):', validators=[NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField('Description of Deck:', validators=[Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    file = FileField("Image:", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Type Not Allowed!')])
    offer = IntegerField('Offer(%):', validators=[NumberRange(min=0, max=100, message='Offer must be between %(min)d and %(max)d')])
    submit = SubmitField('Submit')


class CreateAccessories(FlaskForm):
    name = StringField('Name of Accessory:', [DataRequired()])
    brand = StringField('Brand of Accessory:', [DataRequired(), Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    price = IntegerField('Price of Accessory($):', [DataRequired(), NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField('Description of Accessory:', [DataRequired(), Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    file = FileField("Image:", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Type Not Allowed!')])
    offer = IntegerField('Offer(%):', [DataRequired(), NumberRange(min=0, max=100, message='Offer must be between %(min)d and %(max)d')])
    submit = SubmitField('Submit')


class UpdateAccessories(FlaskForm):
    name = StringField('Name of Accessory:')
    brand = StringField('Brand of Accessory:', [Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    price = IntegerField('Price of Accessory($):', [NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField('Description of Accessory:', [Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    file = FileField("Image:", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], message='File Type Not Allowed!')])
    offer = IntegerField('Offer(%):', [NumberRange(min=0, max=100, message='Offer must be between %(min)d and %(max)d')])
    submit = SubmitField('Submit')


class CreateTutorial(FlaskForm):
    name = StringField('Name of Video:', [DataRequired()])
    difficulty = RadioField('Difficulty Lvl:', choices=['Beginner', 'Intermediate', 'Advanced'], validators=[DataRequired()])
    type = RadioField('Type of Video:', choices=['Trick', 'Sleight of Hand', 'Flourishes', 'Non-cards'], validators=[DataRequired()])
    video = StringField('Path of video of Tutorial:', [DataRequired()])
    thumbnail = StringField('Thumbnail Path:', [DataRequired()])


class UpdateTutorial(FlaskForm):
    name = StringField('Name of Video:')
    difficulty = RadioField('Difficulty Lvl:', choices=['Beginner', 'Intermediate', 'Advanced'])
    type = RadioField('Type of Video:', choices=['Trick', 'Sleight of Hand', 'Flourishes', 'Non-cards'])
    video = StringField('Path of video of Tutorial:')
    thumbnail = StringField('Thumbnail Path:')
