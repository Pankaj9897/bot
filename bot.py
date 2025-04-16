from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()  

API_KEY = os.getenv('API_KEY') 


app = Flask(__name__)


@app.route('/', methods=['POST'])
def convert_currency():
    data = request.get_json()

    if data is None:
        print(" Koi JSON data nahi mila request se.")
        return jsonify({"fulfillmentText": "Bhai, JSON data hi nahi mila!"})

    print("JSON mila:", data)  

    unit_currency = data['queryResult']['parameters']['unit-currency']
    source_currency = unit_currency[0]['currency']
    amount = unit_currency[0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    
    print("Source:", source_currency)
    print( Amount:", amount)
    print("target:", target_currency)

    # Call CurrencyAPI
    url = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={source_currency}&currencies={target_currency}"
    response = requests.get(url)
    exchange_data = response.json()

    try:
        rate = exchange_data['data'][target_currency]['value']
        converted_amount = rate * amount
        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} = {converted_amount:.2f} {target_currency}"
        })
    except Exception as e:
        print("Error in conversion:", e)
        return jsonify({
            "fulfillmentText": "Kuch galat ho gaya bhai. Please check currency codes or API response."
        })

if __name__ == '__main__':
    app.run(debug=True)



