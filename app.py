from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route('/api/hello', methods=['GET'])
def hello():

    # get the visitor's name and real IP address
    visitor_name = request.args.get('visitor_name', 'Visitor')
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Retrieve the location of the visitor's ip using ipapi.co 
    try:
        location = requests.get(f'https://ipapi.co/{visitor_ip}/json/', timeout=5).json()
        city = location.get('city', 'Unknown')
    except requests.exceptions.RequestException:
        city = 'Unknown'

    if city == 'Unknown':
        return jsonify({
            'visitor_ip': visitor_ip,
            'location': city,
            'greeting': f"Hello, {visitor_name}! We couldn't determine your location."
        }), 200

    # Use weatherapi.com to retrieve the weather information
    weather_api_key = '4de1d8d100e74282ada131115240307'
    try:
        weather_response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}', timeout=5)
        weather_response.raise_for_status()
        weather = weather_response.json()
        temperature = weather['current']['temp_c']
    except requests.exceptions.RequestException:
        temperature = 'unknown'

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'

    response = {
        'visitor_ip': visitor_ip,
        'location': city,
        'greeting': greeting
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run()