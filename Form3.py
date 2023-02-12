from wtforms import Form, StringField, TelField, TextAreaField, SelectField, validators, EmailField


class CreateAddressForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder":'John'})
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder":'Doe'})
    town = SelectField('', choices=[('Central', 'Central'), ('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')], default='North')
    zipcode = StringField('', [validators.Length(min=1, max=6), validators.DataRequired()], render_kw={"placeholder":'569830'})
    address = StringField('', [validators.Length(min=1, max=200), validators.DataRequired()], render_kw={"placeholder":'NYP Block L'})
    phone_number = TelField('', [validators.Length(min=1, max=9), validators.DataRequired()], render_kw={"placeholder":'9424 1424'})
    office_number = TelField('', [validators.Length(min=1, max=9), validators.Optional()], render_kw={"placeholder":'6579 5678'})
    email_address = EmailField('', [validators.Length(min=1, max=100), validators.DataRequired()], render_kw={"placeholder":'your_name@gmail.com'})
    remarks = TextAreaField('', [validators.Length(min=1, max=150), validators.Optional()])

