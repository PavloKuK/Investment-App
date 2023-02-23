import customer as customer_db
import json
import requests
import urllib.request

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
         
   
      url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + result["name"] + "&apikey=" + key
      r = requests.get(url)
      data = urllib.request.urlopen(url).read().decode()
      
      companyInfo = json.loads(data)
      
      url1 = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol" + result["name"] + "&apikey=" + key
      r1 = requests.get(url1)
      data1 = urllib.request.urlopen(url1).read().decode()
      
      companyInfo1 = json.loads(data1)
      
      with open('static/data/company_overview.json', 'w') as file:
         file.write(data)
      
      return render_template('lookupAfter.html', title= result["name"] + " overview", header=result["name"] + " overview", result=result, companyInfo=companyInfo, companyInfo1=companyInfo1)
   return render_template('lookup.html', title="Investment App", header="Investment App", form=form)

@app.route('/manuals', methods=['GET', 'POST'])
def manual():
   return render_template('manuals.html', title="User Manuals", header="User Manuals")
   

if __name__ == "__main__":
   app.run(debug=True) 