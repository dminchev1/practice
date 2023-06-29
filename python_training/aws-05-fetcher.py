import json
import boto3
from botocore.vendored import requests
import urllib3
from decimal import Decimal
import uuid

http = urllib3.PoolManager()
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

weather_collect = dynamodb.Table('storeMaxTemp')

def lambda_handler(event, context):
    message = event['Records'][0]['body']
    message_body = json.loads(message)
    
    latitude = message_body['latitude']
    longitude = message_body['longitude']
    date = message_body['date']
    city = message_body['city']
    
    # Make HTTP request to the Weather API
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&daily=temperature_2m_max&timezone=auto"
    response = http.request('GET',
                        url,
                        headers = {'Content-Type': 'application/json'},
                        retries = False)
    data = json.loads(response.data.decode('utf-8'))
    
    max_temperature = data['daily']['temperature_2m_max'][0]
    
    random_id = str(uuid.uuid4())
    
    # Log the result in the DynamoDB table
    weather_collect.put_item(  # working
        Item={
            'uuid': random_id,
            'date': date,
            'city': city,
            'max_temperature': Decimal(str(max_temperature))
        }
    )
    
    # Send a message to the SNS topic
    sns.publish(
        TopicArn='arn:aws:sns:eu-west-2:431028257119:notify',
        Message=f"The max temperature in {city} on {date} was {max_temperature} degrees Celsius"
    )

    print(event)  # FIFO is printing consecutive but only first 2 messages!
    return None