import customer as customer_db
import json
import requests
import urllib.request
import csv
from itertools import islice
import os
# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.graph_objs as go
# import plotly.express as px
import dataframe_image as dfi
from sqlalchemy.orm import sessionmaker
import win32api
from objectFile import Company

from company_lookup import Lookup, Login, SignUp, BankTransfer, BuyShares
# from graph_lookup import CreateGraph
from flask import Flask, render_template, url_for, request, redirect, jsonify, session, flash

Session = sessionmaker(bind = customer_db.engine)
session = Session()

app = Flask(__name__)

app.config["SECRET_KEY"]='why_a_duck?'

key0 = "PUKOSP3TWUJWMXBG"
key1 = "4ELFTP653JW7XT9Z"
key2 = "QQAF8NRUKEMZTX1T"
key3 = "EG17YJVUNT4E43P7"

Email = "email"
Password = "password"

company = Company("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")

@app.route("/")
def myredirect():
   # company_form = Lookup()
   # graph_form = CreateGraph()
   # return render_template('lookup.html', company_form=company_form)
   return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   
   form = Login()
   
   if form.is_submitted():
      print("Message")
      if form.submit.data:
         result = request.form
        
         # print(result["email"])
         # print(result["password"])
        
         try:
            newLogin = session.query(customer_db.Credentials).first()
            print(Password + Password)
           
            if result["email"] == newLogin.email and result["password"] == newLogin.password:
               # print(Email + Password + Email)
               # win32api.MessageBox(0, 'alert', 'alert')
               return redirect(url_for('simple_form'))
           
         except AttributeError:
            # win32api.MessageBox(0, 'alert', 'alert', 0x00001000)
            print("6516565154165151611111111111111111")
            print(AttributeError)
           
      if form.signup.data:
         # print("16151515+1")
         return redirect(url_for('signup'))
      
   return render_template('login.html', title="Login", header="Login", form=form) 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   form = SignUp()
   
   if form.is_submitted():
      
      result = request.form
      
      try:
         print("It got here")
         user = session.query(customer_db.Account).first()
         newPassword = session.query(customer_db.Credentials).first()
         newBank = session.query(customer_db.Balance).first()
         newHoldings = session.query(customer_db.Holdings).first()
         
         if result["password"] == result["confirmPassword"]:
            user.name = result["name"]
            user.email = result["email"]
            user.bank = result["bank"]
            user.address = result["address"]
            user.state = result["state"]
            
            newPassword.email = result["email"]
            newPassword.password = result["password"]
            
            newBank.bank = result["bank"]
         
            session.commit()
         
      except:
         print("Attribute Error")
         if result["password"] == result["confirmPassword"]:
             
            customer = customer_db.Account(name = result["name"], email = result["email"], bank = result["bank"], address = result["address"], state = result["state"])
            credentials = customer_db.Credentials(email = result["email"], password = result["password"])
            newBank = customer_db.Balance(bank = result["bank"], amount = 0.0)
            newHoldings = customer_db.Holdings(name = "", value = 0.0, gain = 0.0)
            session.add(customer)
            session.add(credentials)
            session.add(newBank)
            session.add(newHoldings)
            session.commit()
            session.flush()
            
            return redirect(url_for('simple_form'))
            
   return render_template('signup.html', title="Signup", header="Signup", form=form)

@app.route('/lookup', methods=['GET', 'POST'])
def simple_form():
   # company_form = Lookup()
   form = Lookup()
   # form = company_form
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
            
         for key, value in companyInfo.items():
            
            if key == "AssetType":
               company.assetType = value
               
            elif key == "Name":
               company.name = value
               
            elif key == "Description":
               company.description = value
               
            elif key == "Exchange":
               company.exchange = value
               
            elif key == "Country":
               company.country = value
            
            elif key == "Sector":
               company.sector = value
               
            elif key == "Industry":
               company.industry = value
               
            elif key == "Address":
               company.address = value
               
            elif key == "MarketCapitalization":
               company.marketCapitalization = value
               
            elif key == "DividendYield":
               company.dividentYield = value
               
            elif key == "PERatio":
               company.peratio = value
               
            elif key == "EPS":
               company.eps = value
               
            elif key == "Beta":
               company.beta = value
               
            elif key == "52WeekHigh":
               company.weekHigh = value
               
            elif key == "52WeekLow":
               company.weekLow = value
               
            elif key == "50DayMovingAverage":
               company.fiftyDayMovingAverage = value
               
            elif key == "200DayMovingAverage":
               company.twoHundredDayMovingAverage = value
            
         
         return render_template('lookupAfter.html', result = result, companyInfo = companyInfo,
         assetType = company.assetType,
         name = company.name,
         description = company.description,
         exchange = company.exchange,
         country = company.country,
         sector = company.sector,
         industry = company.industry,
         address = company.address,
         marketCapitalization = company.marketCapitalization,
         dividentYield = company.dividentYield,
         peratio = company.peratio,
         eps = company.eps,
         beta = company.beta,
         weekHigh = company.weekHigh,
         weekLow = company.weekLow,
         fiftyDayMovingAverage = company.fiftyDayMovingAverage,
         twoHundredDayMovingAverage = company.twoHundredDayMovingAverage)
      
      
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
         url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + result["name"] + "&apikey=" + key0
         r = requests.get(url)
         data = urllib.request.urlopen(url).read().decode()
      
         companyInfo = json.loads(data)
         with open('static/data/company_overview.json', 'w') as file:
            file.write(data)

         for key, value in companyInfo.items():
            
            if key == "Name":
               company.name = value

         urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + result["name"] + "&apikey=" + key2 + "&datatype=csv"
      
         companyInfo = pd.read_csv(urlCsv)
      
         companyInfo.to_csv('static/data/monthly_adjusted.csv')
         monthlyData = pd.read_csv('static/data/monthly_adjusted.csv')
         
         # Create a trace
         data = [go.Scatter(
            x = monthlyData['timestamp'], 
            y = monthlyData['close'],
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
         graph_table = pd.read_csv('static/data/monthly_adjusted.csv', usecols=['timestamp', 'high', 'close'], nrows=12)
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
         urlCsvWeekly = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=' + result["name"] + "&apikey=" + key1 + "&datatype=csv"
         weekly_info = pd.read_csv('static/data/weekly_adjusted.csv')
         weekly_info.to_csv('static/data/weekly_adjusted.csv')
         weekly_table = pd.read_csv('static/data/weekly_adjusted.csv', usecols=['timestamp', 'high', 'close'], nrows=10)
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

         return render_template('rate_graphAfter.html', title= company.name + " Graph", header= company.name + " Stock Rates Graph Over Time", result=result, companyInfo=companyInfo, name = company.name)

   return render_template('lookup.html', title="Investment App", header="Investment App", form=form)

@app.route('/manuals', methods=['GET', 'POST'])
def manual():
   return render_template('manuals.html', title="User Manuals", header="User Manuals")

@app.route('/bank-transfer', methods=['GET', 'POST'])
def bankTransfer():
   form = BankTransfer()
   
   if form.is_submitted():
      
      result = request.form
      
      money = result["amount"]
   
      
      try:
         money = float(money)
         
         balance = session.query(customer_db.Balance).first()
         
         balance.amount = balance.amount + money
         
         session.commit()
         
         print(balance.amount)
         
         print("Money is a number")
        
      except ValueError:
         print(ValueError)
         print("You have to enter a number")
            
      
      print(money)
   
   return render_template('bank-transfer.html', title = "Bank", header = "Bank", form=form)


@app.route("/favicon.ico")
def favicon():
    return render_template('close.html', title="User Manuals", header="User Manuals")

if __name__ == "__main__":
   app.run(debug=True) 
