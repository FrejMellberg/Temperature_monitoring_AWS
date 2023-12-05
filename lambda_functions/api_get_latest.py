import boto3
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'TableName'  # Replace with your table name

def lambda_handler(event, context):
    # Get the DynamoDB table
    table = dynamodb.Table(table_name)
    
    try:
        # Query the table to get the most recently added item
        response = table.query(
            KeyConditionExpression=Key('device_id').eq('DeviceName'),  # Define your sort key condition
            ScanIndexForward=False,  # Sort in descending order (most recent first)
            Limit=1  # Limit to retrieve only one item
            
        )
        
        # Extract the item if it exists
        if 'Items' in response and len(response['Items']) > 0:
            most_recent_item = response['Items'][0]
            # Do something with the most recent item
            return most_recent_item
        else:
            return "No items found"
    except Exception as e:
        return f"Error: {e}"
