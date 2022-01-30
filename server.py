from getpass import getuser
import json
from flask import Flask, request, jsonify, render_template
from flask_mongoengine import MongoEngine
from matplotlib.container import BarContainer
from barcode import *
from datetime import datetime
from nutrients import Nutrition_Information

app = Flask(__name__)

###########Data Base Stuff#############

app.config['MONGODB_SETTINGS'] = {
    'db': 'caffeine_calculator_db',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    firstName = db.StringField()
    lastName = db.StringField()

###############ROUTES##################

#Home page
@app.route("/")
def home():
    return render_template("caffeine.html")

#Scan page
@app.route('/scanCode', methods=['POST'])
def post_record():
    img_data = json.loads(request.data)
    ScanAndSearchBarcode(img_data)
    return "hi"

@app.route('/scanCode', methods=['GET'])
def scanImg():
    return render_template("scanCode.html")

#Receipt page
def create_nutrition_obj(query):
    my_nutrition = Nutrition_Information(query)
    return my_nutrition

@app.route("/receipt", methods=['POST'])
def receipt():
    query = str(request.form['search_by_text'])
    today = datetime.now().strftime("%Y/%m/%d")
    my_nutrition = create_nutrition_obj(query)
    formatted_caffeine = round(my_nutrition.caffeine_amt, 2)
    amt_you_can_drink = round(400 - my_nutrition.caffeine_amt, 2)
    return render_template("receipt.html", today=today, food=my_nutrition.food, serving_quantity=my_nutrition.qty,
                           serving_unit=my_nutrition.serving_unit, caffeine_amount=formatted_caffeine,
                           amt_you_can_drink=amt_you_can_drink)


if __name__ == "__main__":
    app.run(debug=True)