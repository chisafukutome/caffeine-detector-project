from getpass import getuser
import json
from flask import Flask, request, jsonify, render_template
from flask_mongoengine import MongoEngine
from matplotlib.container import BarContainer
from barcode import *

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'caffeine_calculator_db',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    #id = db.fields.intfield()
    firstName = db.StringField()
    lastName = db.StringField()
    #totalCaffeine = db.fields.intfield()


# @app.route('/', methods=['GET'])
# def query_records():
#     return render_template("index.html")

@app.route('/', methods=['POST'])
def post_record():
    img_data = json.loads(request.data)
    ScanAndSearchBarcode(img_data)
    return "hi"

@app.route('/', methods=['GET'])
def scanImg():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)