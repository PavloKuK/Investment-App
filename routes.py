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
import win32api
from objectFile import Company

import ctypes  # An included library with Python install.

from sqlalchemy.orm import sessionmaker

from company_lookup import Lookup, Login, SignUp, BankTransfer
from flask import Flask, render_template, url_for, request, redirect, jsonify, flash

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

Session = sessionmaker(bind=customer_db.engine)
session = Session()

app = Flask(__name__)

app.config["SECRET_KEY"] = 'why_a_duck?'

key0 = "PUKOSP3TWUJWMXBG"
key1 = "4ELFTP653JW7XT9Z"
key2 = "QQAF8NRUKEMZTX1T"
key3 = "EG17YJVUNT4E43P7"

Email = "email"
Password = "password"

company = Company("", "", "", "", "", "", "", "",
                  "", "", "", "", "", "", "", "", "")

# def show_popup():
#     messagebox.showinfo("Title", "Message")

# root = tk.Tk()
# root.withdraw()

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
 

# def popupmsg(msg, title):
#     root = tk.Tk()
#     root.title(title)
#     label = ttk.Label(root, text=msg)
#     label.pack(side="top", fill="x", pady=10)
#     B1 = tk.Button(root, text="Okay", command=root.destroy)
#     B1.pack()
#     root.attributes("-topmost", True) # This will make the window appear on top of all other windows
#     root.after_idle(root.attributes, '-topmost', False) # This will reset the attribute after the window appears
#     root.geometry(f"+{root.winfo_screenwidth() // 2}+{root.winfo_screenheight() // 2}") # This will make the window appear in the middle of the screen
#     root.mainloop()

@app.route("/")
def myrediret():
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
                # print(Password + Password)

                if result["email"] == newLogin.email and result["password"] == newLogin.password:
                    # print(Email + Password + Email)
                    # win32api.MessageBox(0, 'alert', 'alert')
                    
                    Mbox('Login', 'Login Successful', 0)
                  
                  #   root.after(0, show_popup)
                  #   root.mainloop()
                  
                  #   popupmsg("Hello", "Message")
                    
                    return redirect(url_for('simple_form'))

            except AttributeError:
                # win32api.MessageBox(0, 'alert', 'alert', 0x00001000)
                Mbox('Login', 'Login Successful', 0)
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
            user = session.query(customer_db.Account).first()
            newPassword = session.query(customer_db.Credentials).first()
            newBank = session.query(customer_db.Balance).first()

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
                Mbox('Profile', 'Profile changes saved successfuly', 0)

        except AttributeError:

            if result["password"] == result["confirmPassword"]:

                customer = customer_db.Account(
                    name=result["name"], email=result["email"], bank=result["bank"], address=result["address"], state=result["state"])
                credentials = customer_db.Credentials(
                    email=result["email"], password=result["password"])
                newBank = customer_db.Balance(bank=result["bank"], amount=0.0)
                session.add(customer)
                session.add(credentials)
                session.add(newBank)
                session.commit()
                session.flush()
                Mbox('Sinup', 'Signup Successful', 0)

                return redirect(url_for('simple_form'))

    return render_template('signup.html', title="Signup", header="Signup", form=form)


@app.route('/lookup', methods=['GET', 'POST'])
def simple_form():
    form = Lookup()

    if form.is_submitted():

        result = request.form

        dividentIncome = 0

        if result["purpose"] == "General Overview":
            url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + \
                result["name"] + "&apikey=" + key0
            urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + \
                result["name"] + "&apikey=" + key1 + "&datatype=csv"
            r = requests.get(url)
            data = urllib.request.urlopen(url).read().decode()

            frame = pd.read_csv(urlCsv)
            frame.to_csv('static/data/monthly_adjusted.csv')

            companyInfo = json.loads(data)
            with open('static/data/company_overview.json', 'w') as file:
                file.write(data)

            with open('static/data/monthly_adjusted.csv', 'r') as file:

                for line in islice(csv.reader(file), 1, 12):
                    dividentIncome += float(line[8])

            print(dividentIncome)

            hundredShares = dividentIncome * 100

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

            return render_template('lookupAfter.html', result=result, companyInfo=companyInfo, dividentIncome=dividentIncome, hundredShares=hundredShares,
                                   assetType=company.assetType,
                                   name=company.name,
                                   description=company.description,
                                   exchange=company.exchange,
                                   country=company.country,
                                   sector=company.sector,
                                   industry=company.industry,
                                   address=company.address,
                                   marketCapitalization=company.marketCapitalization,
                                   dividentYield=company.dividentYield,
                                   peratio=company.peratio,
                                   eps=company.eps,
                                   beta=company.beta,
                                   weekHigh=company.weekHigh,
                                   weekLow=company.weekLow,
                                   fiftyDayMovingAverage=company.fiftyDayMovingAverage,
                                   twoHundredDayMovingAverage=company.twoHundredDayMovingAverage)

        # if result["purpose"] == "Divident Income":
        #    urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + result["name"] + "&apikey=" + key1 + "&datatype=csv"

        #    frame = pd.read_csv(urlCsv)

        #    frame.to_csv('static/data/monthly_adjusted.csv')

        #    with open('static/data/monthly_adjusted.csv', 'r') as file:

        #       for line in islice(csv.reader(file), 1, 12):
        #          dividentIncome += float(line[8])

        #    print(dividentIncome)

        #    hundredShares = dividentIncome * 100

        #    return render_template('dividentIncomeHandler.html', title = "Dividents", header = "Divdents", result=result, dividentIncome=dividentIncome, hundredShares=hundredShares)

        if result["purpose"] == "Stock History":
            urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + \
                result["name"] + "&apikey=" + key1 + "&datatype=csv"

            companyInfo = pd.read_csv(urlCsv)

            companyInfo.to_csv('static/data/monthly_adjusted.csv')

            # Create a trace
            data = [go.Scatter(
                x=companyInfo['timestamp'],
                y=companyInfo['close'],
            )]
            layout = go.Layout(
                xaxis=dict(
                    title='TimeStamps',
                ),
                yaxis=dict(
                    title='Share Price',
                )
            )
            # Show entire stock rates for company
            fig = go.Figure(data=data, layout=layout)
            fig.write_image("static/photo/graph.png")

            # Show stock rates for last 12 Months
            graph_table = pd.read_csv(
                urlCsv, usecols=['timestamp', 'high', 'close'], nrows=12)
            data = [go.Scatter(
                x=graph_table['timestamp'],
                y=graph_table['close'],
            )]
            layout = go.Layout(
                xaxis=dict(
                    title='TimeStamps',
                ),
                yaxis=dict(
                    title='Share Price',
                )
            )
            fig_monthly = go.Figure(data=data, layout=layout)
            fig_monthly.write_image("static/photo/graph_monthly.png")
            df_styled = graph_table.style.background_gradient()
            dfi.export(df_styled, "static/photo/monthly_rate_table.png")

            # Show stock rates for last 10 weeks
            urlCsvWeekly = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=' + \
                result["name"] + "&apikey=" + key2 + "&datatype=csv"
            weekly_table = pd.read_csv(urlCsvWeekly, usecols=[
                                       'timestamp', 'high', 'close'], nrows=10)
            data = [go.Scatter(
                x=weekly_table['timestamp'],
                y=weekly_table['close'],
            )]
            layout = go.Layout(
                xaxis=dict(
                    title='TimeStamps',
                ),
                yaxis=dict(
                    title='Share Price',
                )
            )
            fig_weekly = go.Figure(data=data, layout=layout)
            fig_weekly.write_image("static/photo/graph_weekly.png")
            df_styled = weekly_table.style.background_gradient()
            dfi.export(df_styled, "static/photo/weekly_rate_table.png")

            # Show stock rates for last 15 days
            urlCsvDaily = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + \
                result["name"] + "&apikey=" + key3 + "&datatype=csv"
            daily_table = pd.read_csv(urlCsvDaily, usecols=[
                                      'timestamp', 'close'], nrows=15)
            data = [go.Scatter(
                x=daily_table['timestamp'],
                y=daily_table['close'],
            )]
            layout = go.Layout(
                xaxis=dict(
                    title='TimeStamps',
                ),
                yaxis=dict(
                    title='Share Price',
                )
            )
            fig_daily = go.Figure(data=data, layout=layout)
            fig_daily.write_image("static/photo/graph_daily.png")
            df_styled = daily_table.style.background_gradient()
            dfi.export(df_styled, "static/photo/daily_rate_table.png")

            return render_template('rate_graphAfter.html', title=result["name"] + " Graph", header=result["name"] + " Stock Rates Graph Over Time", result=result, companyInfo=companyInfo)
    return render_template('lookup.html', title="Investment App", header="Investment App", form=form)


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


@app.route('/manuals', methods=['GET', 'POST'])
def manual():
    return render_template('manuals.html', title="User Manuals", header="User Manuals")


if __name__ == "__main__":
    app.run(debug=True)
