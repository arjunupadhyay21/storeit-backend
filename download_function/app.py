import json
import boto3
import os
import base64

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['STORAGE_BUCKET_NAME']

def download_handler(event, context):
    try:
        body = json.loads(event['body'])
        file_key = body.get('file_key')

        if not file_key:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({"message": "Missing 'file_key'"})
            }

        response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
        file_data = response['Body'].read()
        base64_content = base64.b64encode(file_data).decode()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": f"File '{file_key}' downloaded",
                "content": base64_content
            }),
        }
    except Exception as e:
        print(f"Error downloading file: {e}")
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"message": "Error downloading file", "error": str(e)}),
        }