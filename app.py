from flask import Flask
from flask import request, render_template
import ml_model

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index.html')
  
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