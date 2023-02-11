from wtforms import Form, StringField, SelectField, validators, TextAreaField, FloatField, DateField, RadioField, TimeField, DecimalField
from wtforms.fields import EmailField, PasswordField, IntegerField, FileField
from wtforms.validators import ValidationError
import datetime


class signUp(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])
    contact = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    gender = SelectField('Gender', [validators.DataRequired(message='This is a required field.')], choices=['', 'Male', 'Female'], default='')
    dob = DateField('Date of Birth', [validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=20, message='Passwords must be between 8 to 20 characters'), validators.DataRequired(), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password, must contain a mix of lowercase, uppercase, number and special character')])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.EqualTo('password', message='Passwords must match'), validators.DataRequired(message='This is a required field.')])

class Login(Form):
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    password = PasswordField('Password', [validators.Length(min=1, max=50), validators.DataRequired()])

class ForgetPassword(Form):
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])

class update(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    contact = StringField('Contact Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    gender = SelectField('Gender', [validators.DataRequired(message='This is a required field.')], choices=['', 'Male', 'Female'], default='')
    dob = DateField('Date of Birth', [validators.InputRequired()])
