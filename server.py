from flask import Flask, render_template, request
from datetime import datetime
from nutrients import Nutrition_Information

app = Flask(__name__)

def create_nutrition_obj(query):
    my_nutrition = Nutrition_Information(query)
    return my_nutrition

@app.route("/")
def home():
    return render_template("caffeine.html")

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

