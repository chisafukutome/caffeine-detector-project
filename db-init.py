from getpass import getuser
import json
from flask import Flask, request, jsonify, render_template
from flask_mongoengine import MongoEngine

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


@app.route('/', methods=['GET'])
def query_records():
    return render_template("receipt_testing.html")

@app.route('/', methods=['POST'])
def post_record():
    record = json.loads(request.data)
    print(record)
    return record


if __name__ == "__main__":
    app.run(debug=True)