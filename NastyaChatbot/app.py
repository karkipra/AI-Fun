from flask import Flask, render_template, request  # import flask
from random import randint
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re

# Constant for randomness
RANDOMNESS = 5

# Parse the auth and host from env:
bonsai = "https://jcky5zh1gq:3qkm3gjy40@cherry-213410966.us-east-1.bonsaisearch.net:443"
auth = re.search('https://(.*)@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# optional port
match = re.search('(:\d+)', host)
if match:
    p = match.group(0)
    host = host.replace(p, '')
    port = int(p.split(':')[1])
else:
    port = 443

# Connect to cluster over SSL using auth for best security:
es_header = [{
    'host': host,
    'port': port,
    'use_ssl': True,
    'http_auth': (auth[0], auth[1])
}]

# Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header)

# Verify that Python can talk to Bonsai (optional):
if not es.ping():
    print("Connection Error!")

# train_data instance and setting up with ES
train_data = pd.read_csv('data/train_data_2.csv')
train_data.dropna(subset=['text', 'response'], inplace=True)
texts_dict = train_data.to_dict(orient='records')

# Why is this not working??
bulk(es, texts_dict, index='chatbot-events', doc_type='clue', raise_on_error=True)


# create an app instance
app = Flask(__name__)


@app.route("/")  # at the end point /
def home():
    return render_template('home.html')


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return chat(user_text)

"""
chat - receives user_text and does a search for matching terms
params - user_text (String)
"""

def chat(user_text):
    # return user_text

    # Get response from ES
    response = es.search(index='chatbot-events', doc_type='clue', body={"query": {
        "match": {
            "text": user_text
        }
    }})

    # Use randomness function and get hit on response
    try:
        i = randint(0, RANDOMNESS)
        return response['hits']['hits'][i]['_source']['response']
    except:
        return "LOST FOR WORDS"


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
