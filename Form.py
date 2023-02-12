from wtforms import Form, StringField, TelField, TextAreaField, RadioField, SelectField, validators, EmailField


class CreatePaymentForm(Form):
    card_name = StringField('', [validators.Length(min=1, max=100), validators.DataRequired()])
    card_number = StringField('', [validators.Length(min=1, max=24), validators.DataRequired()])
    security_code = StringField('', [validators.Length(min=1, max=3), validators.DataRequired()], render_kw={"placeholder":'123'})
    expiry_month = SelectField('Card Expiration Date - Month', [validators.DataRequired()], choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')], default='')
    expiry_year = SelectField('Card Expiration Date - YEAR', [validators.DataRequired()], choices=[('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], default='')
    payment_type = RadioField('', choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Paypal', 'Paypal')], default='Credit Card')
    delivery_type = RadioField('', choices=[('Standard', 'Standard'), ('Premium', 'Premium')], default='Standard')
    promo_code = StringField('', [validators.Length(min=1, max=150), validators.Optional()])

