import json
import urllib.request
from decimal import Decimal

def lambda_handler(event, context):
    # Extract the city name from the query parameters
    city = event['queryStringParameters']['city']
    # check https://aws-lambda-for-python-developers.readthedocs.io/en/latest/02_event_and_context/

    # Get the weather information for the city
    response_body, response_code = get_weather(city)

    # Create a response object
    response = {
        'statusCode': response_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response_body)
    }

    return response

def get_weather(city):
    api_key = '6733567cb84f82143cc6651eea3e88fe'
    # OpenWeatherMap API endpoint
    api_endpoint = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    # Make an API request to retrieve the weather information
    with urllib.request.urlopen(api_endpoint) as response:
        data = json.loads(response.read())

    # Check if the API request was successful
    if data.get('cod') == 200:
        weather_info = {
            'description': data['weather'][0]['description'],
            'temperature': Decimal(str(data['main']['temp'])),  # Convert to Decimal
            'humidity': data['main']['humidity']
        }
        return weather_info, data.get('cod')
    else:
        return None