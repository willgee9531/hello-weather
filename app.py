from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    
    # Try to get the real IP address from the request headers
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Use ipapi.co to get the location based on the IP
    try:
        location_data = requests.get(f'https://ipapi.co/{client_ip}/json/', timeout=5).json()
        city = location_data.get('city', 'Unknown')
    except requests.exceptions.RequestException:
        city = 'Unknown'

    if city == 'Unknown':
        return jsonify({
            'client_ip': client_ip,
            'location': city,
            'greeting': f"Hello, {visitor_name}! We couldn't determine your location."
        }), 200

    # Use weatherapi.com to get the weather information
    weather_api_key = '4de1d8d100e74282ada131115240307'
    try:
        weather_response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}', timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']
    except requests.exceptions.RequestException:
        temperature = 'unknown'

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'

    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': greeting
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run()