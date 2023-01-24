from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, BooleanField
from wtforms.fields import EmailField, DateField


class CreateUserForm(Form):

    membership = BooleanField('Receive notification on promotion')
    email = EmailField('Email', [ validators.DataRequired()])



class CreateCustomerForm(Form):

    date_set = DateField('Date Set for release', format='%Y-%m-%d')
    remarks = TextAreaField('Remarks', [validators.DataRequired()])


class CreateNewProductForm(Form):

    name = TextAreaField('Name:', [validators.DataRequired()])
    brand = TextAreaField('Brand:', [validators.DataRequired()])
    price = TextAreaField('Price:', [validators.DataRequired()])
