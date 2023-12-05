# Make sure to include the discord_webhook library in a layer for the function.
# The Lib should be placed in a path "python/lib/python3.11/site-packages/",
# ziped and then uploaded to AWS. 

from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime


now = datetime.now()
time_string = now.strftime('%Y-%m-%d %H:%M:%S')
message_string= ('NodeMCU_home Connected at: \n '+time_string)
webhook = DiscordWebhook(url='yourDiscordURL', content=message_string)

webhook.execute()

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": {"message": "NodeMCU_home Connected"}
    }
