import json
import requests
import time

def retrieve_messages(authorization):
    channels = [[728714730268786739,'guidelines-read-me-first'],
                [869529443260043315,'introduction'],
                [728714241242169409,'general'],
                [1159576386936246302,'student-sharing'],
                [930484782121500743,'weekly-schedule'],
                [1130981583998947489,'0-getting-started'],
                [728714605156892744,'1-7-basics-bootcamp'],
                [929122370835341342,'2-adv-prob-solv-data-structures'],
                [997577422838976632,'weekly-wins-training'],
                [997238397695438938,'weekly-wins-exp'],
                [929122504579092540,'explorer-onboarding'],
                [929122266741080144,'explorer-general'],
                [1181398371961942158,'explorer-data-science'],
                [1181398848887869490,'explorer-dev-ops'],
                [997218244886790184,'web-dev-front-end'],
                [997210990947082360,'web-dev-mobile'],
                [997211860896059422,'web-dev-backend-api'],
                [1007496003366170624,'web-dev-qa-testing'],
                [1155287726111858728,'web-dev-redwood'],
                [1124656910533140520,'game-projects'],
                [1090454149935661077,'custom-projects'],
                [1155287547493236787,'java-jam'],
                [1167517669206003794,'jira-q-and-a'],
                [1108557412744573020,'team-orff'],
                [1159577041046343933,'team-data-science'],
                [1167160324781256805,'team-support-local'],
                [1174040539507736646,'team-student-portal'],
                [1180206747848294432, 'team-ritp'],
                [1169278849436111021,'devops'],
                [1174752566408646687,'aws'],
                [1192518165066960969,'git'],
                [929122405148925982,'the-job-hunt']
                ]
    headers = {
        'authorization' : authorization
    }
    limit = 100
    for channel in channels:
        print(channel[0])
        last_message_id = None
        while True:
            query_parameters = f'limit={limit}'
            if last_message_id is not None:
                query_parameters += f'&before={last_message_id}'
            r = requests.get(f'https://discord.com/api/v9/channels/{channel[0]}/messages?{query_parameters}', headers=headers)
            json_obj = json.loads(r.text)
            
            if len(json_obj) == 0:
                break

            for value in json_obj:
                if(any('referenced_message' in d for d in value) and (value['referenced_message'] is not None)):
                    load_obj = {'content':value['content'],'referenced_message':value['referenced_message']['content']}
                    with open(f'{channel[1]}.json', 'a', encoding='utf-8') as file:
                        json.dump(load_obj,file, ensure_ascii=False, indent=4)
                        file.write(",\n")
                last_message_id = value['id']
            
            time.sleep(2)

auth = ''

retrieve_messages(auth)