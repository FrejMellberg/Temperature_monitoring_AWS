import json
import urllib3
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tableName')

def lambda_handler(event, context):
    print("Starting function")

    http = urllib3.PoolManager()
    r = http.request('GET', 'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/98230/period/latest-hour/data.json')
    
    if r.status == 200:
        json_data = json.loads(r.data.decode('utf-8'))
        
        station_name = str(json_data["station"]["name"])
        value_data = json_data["value"][0]["value"]
        value_date = json_data["value"][0]["date"]
            
        # Prepare data for DynamoDB input
        data_to_put = {
            'device_id': station_name,
            'temperatur': value_data,
            'time': value_date
        }
        
        # Put data into DynamoDB
       
        response = table.put_item(Item=data_to_put)
        
        return data_to_put
    else:
        print("Error fetching temperature:", r.status)
        return {
            "statusCode": r.status,
            "body": "Error fetching SMHI Data"
        }