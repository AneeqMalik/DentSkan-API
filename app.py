from flask import Flask, render_template, request, jsonify
import requests
import random
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_request', methods=['POST'])
def send_request():
    # Get the image path from the form data
    image_path = request.form['image_path']

    # Call the function to send the API request
    response = send_api_request(image_path, api_url)

    return render_template('index.html', response=response)

# Specify an array of image file paths
image_paths = ['static/image1.jpg', 'static/image2.png', 'static/image3.jpg']

# Specify the API endpoint URL
api_url = 'https://dentskan.azurewebsites.net/dentSkan/v1/cropper_image'

venue_url = 'https://venueconnect.azurewebsites.net/api/getvenues'


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

        time.sleep(20)  # 600 seconds = 10 minutes

# Function to send the API request
def send_api_request(image_file_path, api_url):
    # Create the form data payload
    files = {'image': ('image', open(image_file_path, 'rb'))}

    try:
        # Send the POST request with the form data
        response = requests.post(api_url, files=files)

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            print("API request successful!")
            print("Response:", response.json())
            return response.json()
        else:
            # Request failed
            print("API request failed. Status code:", response.status_code)
            print("Response:", response.text)
            return {'error': 'API request failed'}

    except requests.exceptions.RequestException as e:
        print("Error sending API request:", str(e))
        return {'error': 'Error sending API request'}


# Main loop to send requests every 2 minutes
def auto_api_request_loop():
    while True:
        # Choose a random image path from the array
        image_path = random.choice(image_paths)

        # Call the function to send the API request
        dentSkan_response = send_api_request(image_path, api_url)


        response =  requests.get(venue_url)

        # Log the response to the browser console
        print('Venue Connect API Response:', response.json())

        # Wait for 2 minutes before sending the next request
        time.sleep(600)  # 600 seconds = 10 minutes

# Run the Flask app and start the auto API request loop
if __name__ == '__main__':
    auto_api_request_loop()
    app.run()
