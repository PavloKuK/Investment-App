from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectMultipleField, SelectField, RadioField
from wtforms.validators import InputRequired, Length
import requests
import matplotlib.pyplot as plt
import numpy as np
#pip install matplotlib

# key = "PUKOSP3TWUJWMXBG"

# url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=" + name + "&apikey=" + key
# r = requests.get(url)
# graph_data = r.json()


#print(data)

companyNames = []

with open('venv/static/data/listing_status.csv', 'r') as file:
    for line in file:
        if line.strip():
            l = line.rstrip().split(",")
            list = []
            list.append(l[0])
            list.append(l[1])
            myTuple = tuple(list)
            companyNames.append(myTuple)
                   

class CreateGraph(FlaskForm):
    name = SelectField("Pick a company", choices=companyNames)
    submit = SubmitField("Submit")