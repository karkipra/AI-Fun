from flask import Flask, render_template, request  # import flask
from random import randint
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re
import pickle

# Constant for randomness of bot results
RANDOMNESS = 5

# Global Elasticsearch object
ES = None

# Bonsai Url
BONSAI_URL = "https://5a4z2itkpp:bf5bs55wlx@azalea-318561537.us-east-1.bonsaisearch.net:443"

# Create an app instance
app = Flask(__name__)


# at the end point /
@app.route("/")
def home():
    return render_template('home.html')


# GET request from user
@app.route("/get")
def get_bot_response():
    """
    get_bot_response - parses the request from userInput and returns the chat method
    params - None
    returns - response (String)
    """
    user_text = request.args.get('msg')
    return chat(user_text)


def chat(user_text):
    """
    chat - receives user_text and does a search for matching terms
    params - user_text (String)
    returns - response (String)
    """
    # Get response from ES
    response = ES.search(index='chatbot-events', doc_type='clue', body={"query": {
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


def create_elasticsearch(bonsai):
    """
    create_elasticsearch - creates elasticsearch instance from the bonsai cluster
    params - bonsai (String)
    returns - es (Elasticsearch Object)
    """
    # Parse the auth and host from env:
    auth = re.search('https://(.*)@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    # optional ports
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
    return Elasticsearch(es_header)


def bulk_data(es):
    """
    bulk_data - retrieves training data from pickle and uses BULK to index the data
    params - es (Elasticsearch Instance)
    returns - None
    """
    # using Pickled Data for optimization
    with open('data/train_data.pickle', 'rb') as handle:
        texts_dict = pickle.load(handle)

    bulk(es, texts_dict, index='chatbot-events', doc_type='clue', raise_on_error=True)


if __name__ == "__main__":
    # Create elasticsearch instance
    ES = create_elasticsearch(BONSAI_URL)
    # Bulk the indices of the data
    bulk_data(ES)
    # runs the flask app
    app.run(debug=True)
