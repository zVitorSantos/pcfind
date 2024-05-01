from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from utils import get_data_from_kabum , get_data_from_pichau, get_data_from_amazon

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

            # Map hosts to functions
            host_to_function = {
                'www.kabum.com.br': get_data_from_kabum,
                'www.pichau.com.br': get_data_from_pichau,
                'www.amazon.com.br': get_data_from_amazon
            }

            # Check if the link is from a supported host
            for host, function in host_to_function.items():
                if host in link:
                    # Get the data from the link
                    data = function(link)

                    # Return the extracted data as the response
                    return jsonify(data)

            # If we get here, no supported host was found in the link
            return jsonify({'error': 'Site não suportado para coleta automática.'}), 400

    return app

app = create_app()