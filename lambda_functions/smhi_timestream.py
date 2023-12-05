import boto3
import json
import urllib3

timestreamwrite = boto3.client('timestream-write')

def lambda_handler(event, context):
    # Assuming the event contains JSON data you want to put into Timestream
    http = urllib3.PoolManager()
    # SMHI API URL
    r = http.request('GET', 'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/98230/period/latest-hour/data.json')
    
    if r.status == 200:
        json_data = json.loads(r.data.decode('utf-8'))  
        records = [
            {
                'Dimensions': [
                    {'Name': 'device_id', 
                    'Value': json_data["station"]["name"]}
                    # Add more dimensions if necessary
                ],
                'MeasureName': 'outdoor_temperature',
                'MeasureValue': str(json_data["value"][0]["value"]),  # Replace 'your_json_key' with your actual key
                'MeasureValueType': 'DOUBLE',  # Change the type as per your data
                'Time': str((json_data["value"][0]["date"])+3600000)  # a not very elegant way to change the time zone
            }
            # You can add more records if needed
        ]
    
    # Write records to Timestream table
    response = timestreamwrite.write_records(
        DatabaseName='YourDatabaseName',
        TableName='YourTableName',
        Records=records
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully inserted into Timestream'),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
