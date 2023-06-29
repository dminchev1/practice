import json
import boto3
from datetime import datetime, timedelta

city_mapping = {
        'Sofia': {'latitude': 42.70, 'longitude': 23.32},
        'Berlin': {'latitude': 52.52, 'longitude': 13.41},
        'London': {'latitude': 51.51, 'longitude': -0.13},
        'New York': {'latitude': 40.71, 'longitude': -74.01},
        'Paris': {'latitude': 48.85, 'longitude': 2.35}
    }

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    city = event['city']
    latitude = city_mapping[city]['latitude']
    longitude = city_mapping[city]['longitude']
    
    start_date = datetime.strptime(event['start_date'], '%d-%m-%Y')
    end_date = datetime.strptime(event['end_date'], '%d-%m-%Y')

    current_date = start_date
    while current_date <= end_date:  # working correctly
        message = {
            'city': city,
            'latitude': latitude,
            'longitude': longitude,
            'date': current_date.strftime('%Y-%m-%d')
        }
        sqs.send_message(
            QueueUrl='https://sqs.eu-west-2.amazonaws.com/431028257119/standardQ',
            MessageBody=json.dumps(message)
        )
        current_date += timedelta(days=1)
        print(current_date)

    return {
        'statusCode': 202,
        'body': json.dumps({'status': 'ok'})
    }