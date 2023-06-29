import json
import urllib.request
import boto3
import csv
from decimal import Decimal
from datetime import datetime


def lambda_handler(event, context):  # if else with request end
    '''
    Handler of all events activated by triggers.
    '''
    try:
        # Get weather data or logged dynamo data history
        # Extract the city name from the query parameters
        city = event['queryStringParameters']['city']
        # Get the weather information for the city
        x = None
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
        
    except:
        # Write data from s3 to dynamodb based on s3 event trigger
        if event['Records'][0]['eventSource'] == 'aws:s3':
            trigger_s3(event)
        else:
            print('Error with s3 trigger process')
            
    return response

def get_weather_hist(city):
    '''
    Get all dynamodb log data.
    '''
    # Get all requests log per city from dynamodb (WeatherRequests)
    dynamodb = boto3.resource('dynamodb')
    table_name = 'WeatherRequests'
    table = dynamodb.Table(table_name)

    response = table.query(
        IndexName='city-index',  # global secondary index
        KeyConditionExpression="city = :city",
        ExpressionAttributeValues={":city": city},
        ScanIndexForward=False,  # Get descending order (recent first) 

    )

    items = response['Items']

    return items

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_weather(city):
    '''
    Request to weather API data.
    '''
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
    '''
    Write data to dynamodb (WeatherRequests)
    for each user request.
    '''
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
    
def trigger_s3(event):
    '''
    Read and write data from s3 upload to dynamodb (storeEmployee)
    '''
    # Get the S3 bucket name and object key from the event
    bucket_name = "city-temp"
    object_key = event['Records'][0]['s3']['object']['key']  # uploaded s3 file
    
    # Read the contents of the CSV file
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    csv_data = response['Body'].read().decode('utf-8')
    
    # Parse the CSV data and populate DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table_name = "storeEmployee"
    table = dynamodb.Table(table_name)
    
    csv_reader = csv.reader(csv_data.splitlines(), delimiter=',')
    for row in csv_reader:
        index = int(row[0])
        employee_name = str(row[1])
        employee_position = str(row[2])
        phone = int(row[3])
        
        # Store the data in DynamoDB
        item = {
            'id': index,
            'employeeName': employee_name,
            'employeePosition': employee_position,
            'phone': phone
        }
        table.put_item(Item=item)
    
    # Log a message to CloudWatch
    log_message = f"Successfully read and stored information about {object_key} to DB"
    print(json.dumps({"message": log_message}))
    
    return None