# Pulling test data from Discord for ML project 2024

import requests
import json


def retrieve_messages(channelid):
    headers = {
        'authorization': 'your discord auth here'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
    messages = json.loads(r.text)
    with open('mod2.json', 'w') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

retrieve_messages(728714605156892744)