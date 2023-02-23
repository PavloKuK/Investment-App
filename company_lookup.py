from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectMultipleField, SelectField, RadioField
from wtforms.validators import InputRequired, Length

companyNames = []

with open('static/data/listing_status.csv', 'r') as file:
    for line in file:
        if line.strip():
            l = line.rstrip().split(",")
            list = []
            list.append(l[0])
            list.append(l[1])
            myTuple = tuple(list)
            companyNames.append(myTuple)
                   

class Lookup(FlaskForm):
    name = SelectField("Pick a company", choices=companyNames)
    purpose = RadioField(u'Pick what information you want displayed',
                         choices=[('General Overview', 'General Overview'),
                                  ('Divident Income', 'Divident Income'),
                                  ('Stock History For The Past 12 Month', 'Stock History For The Past 12 Month')],
                         validators=[InputRequired(message="You Have To Pick An Option")])
    submit = SubmitField("Submit")
    

