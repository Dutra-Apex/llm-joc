# Pulling test data from Discord for ML project 2024

import requests
import json

def retrieve_messages(channelid):
    headers = {
        'authorization': 'your discord auth here'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
    messages = json.loads(r.text)
    with open('mod1.json', 'w') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

channel_id = 000000000000
retrieve_messages(channel_id)
