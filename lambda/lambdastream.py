import json
import boto3
from decimal import Decimal

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Config
TABLE_NAME = "Your Table Name"
BUCKET = "Your Bucket Name"
FILE_KEY = "all_cities_weather.json"

table = dynamodb.Table(TABLE_NAME)

# Decimal converter
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):

    try:

        # 1. Read ALL latest city data from DynamoDB
        response = table.scan()

        items = response.get('Items', [])

        print(f"Fetched {len(items)} cities")

        # 2. Upload complete latest dataset to S3
        s3.put_object(
            Bucket=BUCKET,
            Key=FILE_KEY,
            Body=json.dumps(items, indent=2, default=decimal_default),
            ContentType="application/json"
        )

        print("S3 updated successfully")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "S3 updated",
                "records": len(items)
            })
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }