from contextlib import redirect_stdout
from dataclasses import replace
import json
from flask import Flask, request, jsonify, render_template, redirect
from barcode import *
from datetime import datetime
from markupsafe import escape
from nutrients import Nutrition_Information

app = Flask(__name__)

###########HELPER FUNCTION#############
def get_nutrition_and_redirect(foodName):
    today = datetime.now().strftime("%Y/%m/%d")
    my_nutrition = create_nutrition_obj(foodName)
    formatted_caffeine = round(my_nutrition.caffeine_amt, 2)
    amt_you_can_drink = round(400 - my_nutrition.caffeine_amt, 2)
    return render_template("receipt.html", today=today, food=my_nutrition.food, qty=my_nutrition.qty,
                           serving_unit=my_nutrition.serving_unit, caffeine_amt=formatted_caffeine,
                           amt_you_can_drink=amt_you_can_drink)

###############ROUTES##################

#Home page
@app.route("/")
def home():
    return render_template("caffeine.html")

productNameGlobal = ""

#Scan page
@app.route('/scanCode', methods=['POST'])
def post_record():
    img_data = json.loads(request.data)
    productName = ScanAndSearchBarcode(img_data)
    if (productName == "Barcode not found"):
        res = {
            "status": "Barcode not found",
            "productName": productName
        }
        return json.dumps(res)
    elif (productName == "Product not found"):
        res = {
            "status": "Product not found",
            "productName": productName
        }
        return json.dumps(res)
    elif (not productName):
        res = {
            "status": "Failed to read barcode",
            "productName": productName
        }
        return json.dumps(res)
    else:
        res = {
            "status": "Barcode found, processing...",
            "productName": productName
        }
        productNameGlobal = productName;
        return json.dumps(res)

@app.route('/scanCode', methods=['GET'])
def scanImg():
    return render_template("scanCode.html")

#Receipt page
def create_nutrition_obj(query):
    my_nutrition = Nutrition_Information(query)
    return my_nutrition

@app.route('/receipt', methods=['GET'])
def getReceipt():
    return render_template("receipt.html")

@app.route('/receipt/<productName>', methods=['GET'])
def getReceiptWithName(productName):
    foodName = str({escape(productName)})
    foodName = foodName.replace("%20", " ")
    foodName = foodName.replace("%3C", "")
    foodName = foodName.replace("{Markup('&lt;", "")
    foodName = foodName.replace("&gt;')}", "")
    print("FOOD NAME: ", foodName)

    return get_nutrition_and_redirect(foodName)

@app.route("/receipt", methods=['post'])
def receiptFromSearchPost():
    query = (request.form['search_by_text'])
    print("TYPE: ", type(query))
    print("QUERY: ", query)

    return get_nutrition_and_redirect(query)

if __name__ == "__main__":
    app.run(debug=True, PORT=8000)