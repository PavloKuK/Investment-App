import customer as customer_db
import json
import requests
import urllib.request
import csv
import pandas as pd
# from sklearn.datasets import load_iris
from itertools import islice

from sqlalchemy.orm import sessionmaker

from company_lookup import Lookup
from flask import Flask, render_template, url_for, request, redirect, jsonify


app = Flask(__name__)

app.config["SECRET_KEY"]='why_a_duck?'

key = "PUKOSP3TWUJWMXBG"

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
         url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + result["name"] + "&apikey=" + key
         r = requests.get(url)
         data = urllib.request.urlopen(url).read().decode()
      
         companyInfo = json.loads(data)
         with open('static/data/company_overview.json', 'w') as file:
            file.write(data)
            
         return render_template('lookupAfter.html', title= result["name"] + " overview", header=result["name"] + " overview", result=result, companyInfo=companyInfo)
      
      
      if result["purpose"] == "Divident Income":
         urlCsv = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + result["name"] + "&apikey=" + key + "&datatype=csv"
      
         frame = pd.read_csv(urlCsv)
      
         frame.to_csv('static/data/monthly_adjusted.csv')
      
         # print(frame.to_string())
         
         with open('static/data/monthly_adjusted.csv', 'r') as file:
            
            for line in islice(csv.reader(file), 1, 12):
               dividentIncome += float(line[8])
               
         print(dividentIncome)
         
         hundredShares = dividentIncome * 100
               
         return render_template('dividentIncomeHandler.html', title = "Dividents", header = "Divdents", result=result, dividentIncome=dividentIncome, hundredShares=hundredShares)
   
      \
   return render_template('lookup.html', title="Investment App", header="Investment App", form=form)

@app.route('/manuals', methods=['GET', 'POST'])
def manual():
   return render_template('manuals.html', title="User Manuals", header="User Manuals")
   

if __name__ == "__main__":
   app.run(debug=True) 
