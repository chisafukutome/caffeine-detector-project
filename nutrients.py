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

nutrition_params = {
    "query": "8 oz tea"
}
response = requests.post(url=NUTRITIONIX_ENDPOINT, headers=headers, json=nutrition_params)
response.raise_for_status()
data = response.json()['foods'][0]['full_nutrients']

for nutrient in data:
    if nutrient['attr_id'] == 262:
        #caffeine amount in mg
        caffeine_amount = nutrient['value']
        print(caffeine_amount)