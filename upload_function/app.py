import json
import boto3
import os
import base64

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['STORAGE_BUCKET_NAME']

def upload_handler(event, context):
    try:
        body = json.loads(event['body'])
        file_key = body.get('file_key', 'default.txt')
        file_content = body.get('file_content', '')
        file_bytes = base64.b64decode(file_content)

        s3.put_object(Bucket=BUCKET_NAME, Key=file_key, Body=file_bytes)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": f"File '{file_key}' uploaded successfully to '{BUCKET_NAME}'"
            }),
        }
    except Exception as e:
        print(f"Error uploading file: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"message": "Error uploading file", "error": str(e)}),
        }