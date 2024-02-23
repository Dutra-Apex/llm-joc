# Filter messages and assign values based on relevance

import json

# load data from json file
with open('mod1.json') as file:
    messages = json.load(file)

# add or reference keywords to assign postiive values
mod1_keywords_positive = {
    'function': 1, 'error': 2, 'bug': 2, 'code': 3, 'programming': 2,
    'python': 2, 'javascript': 2, 'turtle': 2, 'debug': 2, 'solution': 3, 'pycharm': 2, 'vscode': 2, 
    'terminal': 2, 'syntax': 2, 'indentation': 2, 'whitespace': 2, 'newline': 2, 'tab': 2, 'space': 2, 
    'penup': 2, 'pendown': 2, 'forward': 2, 'backward': 2, 'right': 2, 'left': 2, 'goto': 2, 'setpos': 2, 
    'string': 2, 'integer': 2, 'float': 2, 'boolean': 2, 'list': 2, 'tuple': 2, 'dictionary': 2, 'set': 2,
}

# assign a relevance score based on coding-related content
def assign_relevance_score(message):
    content = message['content'].lower()
    score = 0
    
    # increment score based on presence of keywords
    for keyword, value in mod1_keywords_positive.items():
        if keyword in content:
            score += value

    # additional scoring criteria
    # can be expanded with regex checks for code snippets, etc.
    if '```' in content:  # check for code blocks
        score += 5
    if '@help' in content: # check for bot help requests
        score += 3

    # assign score to message (or return it)
    message['relevance_score'] = score
    return message

# apply scoring to each message
scored_messages = [assign_relevance_score(msg) for msg in messages]

# filter out messages with a score below specified threshold
threshold = 4
relevant_messages = [msg for msg in scored_messages if msg['relevance_score'] >= threshold]

# save scored and filtered messages as needed
with open('scored_filtered_messages2.json', 'w') as outfile:
    json.dump(relevant_messages, outfile, indent=4)

print(f"Filtered {len(relevant_messages)} messages with a score of {threshold} or higher.")
