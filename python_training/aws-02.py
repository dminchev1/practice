import json
import urllib.request
import boto3
from decimal import Decimal
from datetime import datetime


def lambda_handler(event, context):  # if else with request end
    # # Extract the city name from the query parameters
    city = event['queryStringParameters']['city']

    # Get the weather information for the city
    x = []
    if event['resource'] == "/cityTempreture":  # working
        # Get the weather information for the city
        response_body, response_code = get_weather(city)
        # Save the weather response
        save_response(city, response_body['temperature'])  # working
        x = response_body
    elif event['resource'] == "/cityTempreture/history":  # working
        x = get_weather_hist(city)
    
    else:
        x = 'Raise error'
    
    
    # Create a response object
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(x, default=decimal_default)  # json serialization
    }
    
    return response

#### write get weather requests history form dynamodb
def get_weather_hist(city):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'WeatherRequests'
    table = dynamodb.Table(table_name)

    response = table.query(
        IndexName='city-index',  # global secondary index
        KeyConditionExpression="city = :city",
        ExpressionAttributeValues={":city": city},
        ScanIndexForward=False,  # Get the records in descending order (most recent first)
        Limit=10  # Retrieve a maximum of 10 records
    )

    items = response['Items']

    return items

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

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


def save_response(city, temperature):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'WeatherRequests'

    table = dynamodb.Table(table_name)

    # Generate a timestamp for the current time
    timestamp = str(datetime.now())

    # Create an item to be inserted into the DynamoDB table
    item = {
        'timestamp': timestamp,
        'city': city,
        'temperature': temperature
    }

    # Insert the item into the DynamoDB table
    table.put_item(Item=item)