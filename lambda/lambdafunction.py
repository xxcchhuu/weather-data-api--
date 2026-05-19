import json
import urllib.request
import boto3
from datetime import datetime
from decimal import Decimal

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_data')

API_KEY = "Your Api Key"

cities = [
    "Kochi", "Mumbai", "Chennai", "Bangalore",
    "Hyderabad", "Pune", "Kolkata", "Ahmedabad",
    "Jaipur", "Lucknow", "Kanpur", "Nagpur",
    "Indore", "Bhopal", "Patna", "Surat",
    "Visakhapatnam", "Coimbatore", "Mysore",
    "Trivandrum", "Thrissur", "Kozhikode",
    "Goa", "Noida", "Gurgaon", "Amritsar",
    "Ludhiana", "Varanasi", "Agra", "Madurai",
    "Salem", "Erode", "Tiruppur", "Vellore"
]

def lambda_handler(event, context):

    results = []

    for city in cities:

        try:

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            response = urllib.request.urlopen(url)

            data = json.loads(response.read())

            item = {
                "city": city,
                "timestamp": datetime.utcnow().isoformat(),
                "temperature": Decimal(str(data["main"]["temp"])),
                "humidity": Decimal(str(data["main"]["humidity"]))
            }

            # overwrite latest city weather
            table.put_item(Item=item)

            results.append({
                "city": city,
                "status": "uploaded"
            })

            print(f"Uploaded: {city}")

        except Exception as e:

            print(f"Error for {city}: {str(e)}")

            results.append({
                "city": city,
                "status": "failed",
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }