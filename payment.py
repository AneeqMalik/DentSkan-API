from flask import Flask, render_template, request, jsonify
import requests
import random
import time
from urllib.parse import quote

def venue_paymentid_request():

    while True:
        # Generate random product name and price
        product_name = "Product" + str(random.randint(1, 1000))
        product_price = random.randint(100, 1000)
        server_endpoint = "https://venueconnect-payment-server.azurewebsites.net/generate-price"

        try:
            payload = {
                "price": product_price,
                "productName": product_name
            }

            response = requests.post(server_endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            
            data = response.json()
            price_id = data.get("priceId")
            if price_id:
                print('Price ID:', price_id)
            else:
                print('Price ID not found in the response')

        except requests.exceptions.RequestException as err:
            print("Failed to generate Price ID:", err)

        time.sleep(30)  # 600 seconds = 10 minutes


if __name__ == '__main__':
    venue_paymentid_request()
    app.run()