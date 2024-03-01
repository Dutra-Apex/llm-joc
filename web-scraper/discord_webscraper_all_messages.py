import json
import requests
import time
import csv
import argparse

def csv_to_dict(file_path):

    data_dict = {}
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        i = 1
        for row in csvreader:
            if len(row) == 2:
                key, value = row
                data_dict[key] = value
            else:
                print(f"Row #{i} does not have 2 columns and will be ignored")
            i += 1

    return data_dict


def retrieve_messages(channels_csv, authorization, limit):

    channels = csv_to_dict(channels_csv)
    headers = {
        'authorization' : authorization
    }

    for channel_name in channels.keys():
        channel_id = channels[channel_name]
        print(f"Scraping from channel {channel_name}")
        last_message_id = None
        while True:
            query_parameters = f'limit={limit}'
            if last_message_id is not None:
                query_parameters += f'&before={last_message_id}'
            r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?{query_parameters}', headers=headers)
            # TODO: Check if authorization key went through, report to user if it fails
            json_obj = json.loads(r.text)
            
            if len(json_obj) == 0:
                break

            for value in json_obj:  
                with open(f'{channel_name}.json', 'a', encoding='utf-8') as file:
                    json.dump(value,file, ensure_ascii=False, indent=4)
                    file.write(",\n")
                last_message_id = value['id']
            
            #time.sleep(2)


def main():

    parser = argparse.ArgumentParser(description="Discord Webscraper")
    parser.add_argument("--channel_list_path", type=str, help="To run the scraper on a list of channels, save the list as a csv file and input its path")
    parser.add_argument("--authorization", type=str, help="Your Discord authorization token")
    parser.add_argument("--limit", type=int, help="How many messages to get", default=50)
    args = parser.parse_args()

    retrieve_messages(args.channel_list_path, args.authorization, args.limit)

    # Commandline sample call
    # python discord_webscraper_responses.py --channel_list_path="path/to/your/list.csv" --authorization="your_token" --limit=100 
    

if __name__ == "__main__":
    main()
