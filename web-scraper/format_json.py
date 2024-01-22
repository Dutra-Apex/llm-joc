import json
import argparse

def format_messages(json_data):
    formatted_messages = []

    for message in json_data:
        content = message.get("content", "")
        reference = message.get("referenced_message", "")

        formatted_content = "A: {}".format(content)
        formatted_reference = "Q: {}".format(reference)

        formatted_messages.append(formatted_content)
        formatted_messages.append(formatted_reference)

    return "\n".join(formatted_messages)

def json_to_txt(json_file_path, txt_file_path):
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    formatted_messages = format_messages(json_data)

    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(formatted_messages)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON messages to formatted TXT file")
    parser.add_argument("--json_path", help="Path to the input JSON file")
    parser.add_argument("--output_path", help="Path to the output TXT file")

    args = parser.parse_args()
    json_path = args.json_path
    output_path = args.output_path

    json_to_txt(json_path, output_path)
