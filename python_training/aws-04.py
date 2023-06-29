import json
import boto3

def lambda_handler(event, context):
    # Extract the message from the query parameters
    message = event['queryStringParameters']['message']
    
    # Create an SNS client
    sns_client = boto3.client('sns')
    
    # Create an SNS topic
    topic_response = sns_client.create_topic(Name='MyTopic')
    topic_arn = 'arn:aws:sns:eu-west-2:431028257119:notify'
    
    # Create an email subscription for the topic
    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email-json',
        Endpoint='your-email@example.com'
    )
    
    # Publish the message to the topic and capture the response
    publish_response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    
    # Create a response object
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Message sent to SNS topic',
            'SNSResponse': publish_response
        })
    }
    
    return response
