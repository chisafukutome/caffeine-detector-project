import requests
import os

NUTRITIONIX_API = os.environ.get('NUTRITIONIX_API')
NUTRITIONIX_APP_ID = os.environ.get('NUTRITIONIX_APP_ID')
NUTRITIONIX_ENDPOINT = os.environ.get('NUTRITIONIX_ENDPOINT')

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API,
    "x-remote-user-id": "0",
    "Content-Type": "application/json"
}


class Nutrition_Information():
    def __init__(self, query):
        nutrition_params = {
            "query": query
        }

        response = requests.post(url=NUTRITIONIX_ENDPOINT, headers=headers, json=nutrition_params)
        response.raise_for_status()

        data = response.json()['foods'][0]
        food_name = data['food_name']
        serving_qty = data['serving_qty']
        serving_unit = data['serving_unit']
        nutrient_info = data['full_nutrients']

        for nutrient in nutrient_info:
            if nutrient['attr_id'] == 262:
                # caffeine amount in mg
                caffeine_amount = nutrient['value']

        self.food = food_name
        self.qty = serving_qty
        self.serving_unit = serving_unit
        self.caffeine_amt = caffeine_amount



