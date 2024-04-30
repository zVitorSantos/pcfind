from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

    @app.route('/search', methods=['OPTIONS', 'POST'])
    def search():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            return response
        elif request.method == 'POST':
            # Handle the POST request here
            data = request.get_json()
            link = data.get('link')
            
            # Make a GET request to the link
            response = requests.get(link)
            
            # Parse the HTML of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the component text
            component_element = soup.find('h1', class_='sc-58b2114e-6 brTtKt')
            component = component_element.text if component_element else None

            # Find the cash price
            cash_price_element = soup.find('h4', class_='sc-5492faee-2 ipHrwP finalPrice')
            cash_price = cash_price_element.text.replace('R$', '').replace('\u00a0', ' ') if cash_price_element else None

            # Find the installment price
            installment_price_element = soup.find('b', class_='regularPrice')
            installment_price = installment_price_element.text.replace('R$', '').replace('\u00a0', ' ') if installment_price_element else None

            # Return the extracted data as the response
            return jsonify({
                'component': component,
                'cash_price': cash_price,
                'installment_price': installment_price
            })

    return app

app = create_app()