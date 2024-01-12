import json
import requests
import time

def retrieve_messages(channel_id, authorization, filename):

    headers = {
        'authorization' : authorization
    }
    limit = 100
    last_message_id = None
    while True:
        query_parameters = f'limit={limit}'
        if last_message_id is not None:
            query_parameters += f'&before={last_message_id}'
        r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?{query_parameters}', headers=headers)
        json_obj = json.loads(r.text)
        
        if len(json_obj) == 0:
            break

        for value in json_obj:
            if(any('referenced_message' in d for d in value) and (value['referenced_message'] is not None)):
                load_obj = {'content':value['content'],'referenced_message':value['referenced_message']['content']}
                with open(filename, 'a', encoding='utf-8') as file:
                    json.dump(load_obj,file, ensure_ascii=False, indent=4)
                    file.write(",\n")
            last_message_id = value['id']
        
        time.sleep(2) #In case there is a limiter on fetches

auth = '<authorization>'
channel_id = '<channel id>'
filename = 'discord_messages.json'

retrieve_messages(channel_id, auth, filename)