import os
import csv
import json
from sklearn.feature_extraction.text import TfidfVectorizer

src = r""
dest = r""

list_files = os.listdir(src)
list_messages = []

for file in list_files:
    if file[-5:] == ".json":
        filepath = os.path.join(src, file)
        with open(filepath, 'r', encoding='utf-8') as file_json:
            curr_json = json.load(file_json)
        content_list = [message["content"] for message in curr_json]
        list_messages.append(' '.join(content_list))
        print(f"Loaded data from {file}")

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(list_messages)
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.toarray()[0]
word_tfidf_scores = list(zip(feature_names, tfidf_scores))
word_tfidf_scores.sort(key=lambda x: x[1], reverse=True)

csv_data = "Word, Tf-idf score \n"
for word, score in word_tfidf_scores:
    csv_data += f"{word}, {score}\n"


with open(dest, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_reader = csv.reader(csv_data.splitlines())
    for row in csv_reader:
        csv_writer.writerow(row)
