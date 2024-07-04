from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

@app.route('/api/hello',methods=['GET'])
def hello():
    try:
        # Get visitor's name and client's ip address
        visitor_name = request.args.get('visitor_name')
        client_ip = request.remote_addr

        # Retrieve location data using ipapi.co
        location_data = requests.get(f'https://ipapi.co/{client_ip}/json/').json()
        
        city = location_data.get('city', '')

        if not city or city == 'Unknown':
            return jsonify({
                'greeting': f"Hello, {visitor_name}! We couldn't determine your location.",
                'client_ip': client_ip,
                'location': 'Unknown'
            }), 200

        # Retrieve weather data using weatherapi.com
        weather_api_key = '4de1d8d100e74282ada131115240307'
        weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}', timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']

        greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees celsius in {city}'

        response = {
            'client_ip': client_ip,
            'location': city,
            'greeting': greeting
        }

        return jsonify(response), 200
    
    # Exceptions are caught for network issues
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from external API: {str(e)}"
        return jsonify({'error': error_message}), 503
    
    #Exceptions are caught for unexpected data format
    except KeyError as e:
        error_message = f"Unexpected data format from API: {str(e)}"
        return jsonify({'error': error_message}), 500
    
    # A fallback catch-all Exception
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run()


