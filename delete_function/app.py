import json
import boto3
import os
import base64

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['STORAGE_BUCKET_NAME']

def delete_handler(event, context):
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

        s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": f"File '{file_key}' deleted from '{BUCKET_NAME}'!"
            }),
        }
    except Exception as e:
        print(f"Error deleting file: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"message": "Error deleting file", "error": str(e)}),
        }