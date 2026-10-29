# list_function/app.py
import boto3
import os
import json

s3 = boto3.client("s3")
BUCKET = os.environ["STORAGE_BUCKET_NAME"]

def list_handler(event, context):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET)
        keys = []
        total_size = 0
        total_files = 0
        
        if "Contents" in response:
            for obj in response["Contents"]:
                keys.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat()
                })
                total_size += obj["Size"]
                total_files += 1
        
        # Calculate storage cost in Indian Rupees
        storage_gb = total_size / (1024 ** 3)
        monthly_cost_usd = storage_gb * 0.023  # $0.023/GB-month
        monthly_cost_inr = monthly_cost_usd * 86.5  # Convert to INR
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "files": keys,
                "storage_metrics": {
                    "total_size": total_size,
                    "total_files": total_files,
                    "storage_gb": round(storage_gb, 4),
                    "monthly_cost": round(monthly_cost_inr, 2)
                }
            })
        }
    except Exception as e:
        # ... (keep existing error handling)
        print("Error listing files in bucket:", e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": "Error listing files",
                "error": str(e)
            })
        }
