import customer as customer_db
import json
import requests
import urllib.request
import csv
import pandas as pd
# from sklearn.datasets import load_iris
from itertools import islice
import plotly
import plotly.graph_objs as go
import dataframe_image as dfi

from sqlalchemy.orm import sessionmaker

from company_lookup import Lookup
from flask import Flask, render_template, url_for, request, redirect, jsonify


app = Flask(__name__)

app.config["SECRET_KEY"]='why_a_duck?'

key0 = "PUKOSP3TWUJWMXBG"
key1 = "4ELFTP653JW7XT9Z"
key2 = "QQAF8NRUKEMZTX1T"

Email = ""
Password = ""

@app.route("/")
def myrediret():
   return redirect(url_for('simple_form'))

@app.route('/lookup', methods=['GET', 'POST'])
def simple_form():
   form = Lookup()
   
   if form.is_submitted():
      
      result = request.form
      
      dividentIncome = 0
      
      if result["purpose"] == "General Overview":
         url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + result["name"] + "&apikey=" + key0
         r = requests.get(url)
         data = urllib.request.urlopen(url).read().decode()
      
         companyInfo = json.loads(data)
         with open('static/data/company_overview.json', 'w') as file:
            file.write(data)
            
         return render_template('lookupAfter.html', title= result["name"] + " overview", header=result["name"] + " overview", result=result, companyInfo=companyInfo)
      
      
      if result["purpose"] == "Divident Income":
         urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + result["name"] + "&apikey=" + key1 + "&datatype=csv"
      
         frame = pd.read_csv(urlCsv)
      
         frame.to_csv('static/data/monthly_adjusted.csv')
      
         with open('static/data/monthly_adjusted.csv', 'r') as file:
            
            for line in islice(csv.reader(file), 1, 12):
               dividentIncome += float(line[8])
               
         print(dividentIncome)
         
         hundredShares = dividentIncome * 100
               
         return render_template('dividentIncomeHandler.html', title = "Dividents", header = "Divdents", result=result, dividentIncome=dividentIncome, hundredShares=hundredShares)
      
      if result["purpose"] == "Stock History":
         urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + result["name"] + "&apikey=" + key2 + "&datatype=csv"
      
         companyInfo = pd.read_csv(urlCsv)
      
         companyInfo.to_csv('static/data/monthly_adjusted.csv')

         # Create a trace
         data = [go.Scatter(
            x = companyInfo['timestamp'], 
            y = companyInfo['close'],
         )]
         layout = go.Layout(
            xaxis = dict(
               title='TimeStamps',
            ),
            yaxis = dict(
               title = 'Share Price',
            )
         )
         # Show entire stock rates for company
         fig = go.Figure(data=data, layout = layout)
         fig.write_image("static/photo/graph.png")
      
         # Show stock rates for last 12 Months
         graph_table = pd.read_csv(urlCsv, usecols=['timestamp', 'high', 'close'], nrows=12)
         data = [go.Scatter(
            x = graph_table['timestamp'], 
            y = graph_table['close'],
         )]
         layout = go.Layout(
            xaxis = dict(
               title='TimeStamps',
            ),
            yaxis = dict(
               title = 'Share Price',
            )
         )
         fig_monthly = go.Figure(data=data, layout = layout)
         fig_monthly.write_image("static/photo/graph_monthly.png")
         df_styled = graph_table.style.background_gradient()
         dfi.export(df_styled, "static/photo/monthly_rate_table.png")

         # Show stock rates for last 10 weeks
         urlCsvWeekly = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=' + result["name"] + "&apikey=" + key2 + "&datatype=csv"
         weekly_table = pd.read_csv(urlCsvWeekly, usecols=['timestamp', 'high', 'close'], nrows=10)
         data = [go.Scatter(
            x = weekly_table['timestamp'], 
            y = weekly_table['close'],
         )]
         layout = go.Layout(
            xaxis = dict(
               title='TimeStamps',
            ),
            yaxis = dict(
               title = 'Share Price',
            )
         )
         fig_weekly = go.Figure(data=data, layout = layout)
         fig_weekly.write_image("static/photo/graph_weekly.png")
         df_styled = weekly_table.style.background_gradient()
         dfi.export(df_styled, "static/photo/weekly_rate_table.png")
         
         # Show stock rates for last 15 days
         urlCsvDaily = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + result["name"] + "&apikey=" + key2 + "&datatype=csv"
         daily_table = pd.read_csv(urlCsvDaily, usecols=['timestamp', 'close'], nrows=15)
         data = [go.Scatter(
            x = daily_table['timestamp'], 
            y = daily_table['close'],
         )]
         layout = go.Layout(
            xaxis = dict(
               title='TimeStamps',
            ),
            yaxis = dict(
               title = 'Share Price',
            )
         )
         fig_daily = go.Figure(data=data, layout = layout)
         fig_daily.write_image("static/photo/graph_daily.png")
         df_styled = daily_table.style.background_gradient()
         dfi.export(df_styled, "static/photo/daily_rate_table.png")

         return render_template('rate_graphAfter.html', title= result["name"] + " Graph", header=result["name"] + " Stock Rates Graph Over Time", result=result, companyInfo=companyInfo)
   return render_template('lookup.html', title="Investment App", header="Investment App", form=form)

@app.route('/manuals', methods=['GET', 'POST'])
def manual():
   return render_template('manuals.html', title="User Manuals", header="User Manuals")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template('signup.html', title="Signup", header="Signup")

@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html', title="Login", header="Login")
   
if __name__ == "__main__":
   app.run(debug=True) 
