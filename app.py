from flask import Flask
from flask import request, render_template, url_for
import ml_model

app = Flask(__name__)

@app.route('/mlinput')
def student():
   return render_template('mlinput.html')

@app.route('/dashboard3')
def dashboard3():
   return render_template('dashboard3.html')

@app.route('/dashboard2')
def dashboard2():
   return render_template('dashboard2.html')

@app.route('/dashboard1')
def dashboard1():
   return render_template('dashboard1.html')

@app.route('/')
def home():
   return render_template('home.html')
  
@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      list_price = request.form.get("listprice")
      # getting input with name = lname in HTML form 
      bedroom = request.form.get("bedrooms")
      washroom = request.form.get("washrooms")
      additional = request.form.get("additional")
      kitchens = request.form.get("kitchens")
      style = request.form.get("style")
      housetype = request.form.get("type")
      fam = request.form.get("family")
      contractdate = request.form.get("cdate")
      #solddate = request.form.get("sdate")
      garage = request.form.get("garage")
      soldprice, difference = ml_model.predict(list_price,bedroom,washroom,additional,kitchens,style,housetype,fam,contractdate,garage)
          
      return render_template("results.html", soldprice=soldprice,difference=difference)
  
if __name__ == '__main__':
   app.run(debug = True)