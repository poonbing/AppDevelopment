from wtforms import StringField, TextAreaField, IntegerField, SubmitField, RadioField
from wtforms.validators import Optional, Length, DataRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
import shelve


def retrieve_db(shelve_name, key):
    with shelve.open(shelve_name) as db:
        output = db[key]
    return output


class UpdateDeckForm(FlaskForm):
    name = StringField(label=('Name of Deck:'))
    brand = StringField(label=('Brand of Deck:'), validators=[Length(min=1, max=50, message='Brand length must be between %(min)d and %(max)d characters')])
    type = RadioField(label=('Type of Deck:'), choices=['Luxury', 'Classic', 'Cardistry'])
    price = IntegerField(label=('Price of Deck($):'), validators=[NumberRange(min=1, max=100, message='You are only allowed to set the Price between%(min)d and %(max)d ')])
    description = TextAreaField(label=('Description of Deck:'), validators=[Length(min=1, max=300, message='Description length must be between %(min)d and %(max)d characters')])
    picture = StringField(label=('Path of Picture of Deck:'))
    offer = IntegerField(label=('Offer(%):'))
    submit = SubmitField(label=('Submit'))


    def validate_name(self, name):
        db = retrieve_db('products', 'decks')
        plist = list(db.values())
        for i in plist:
            if name.data in i.values():
                raise ValidationError("Entry already exist in database, try another.")
