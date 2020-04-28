from flask import Flask, render_template, request  # import flask
from random import randint
    # import pandas as pd
    # from elasticsearch import Elasticsearch
    # from elasticsearch.helpers import bulk

# Constant for randomness
RANDOMNESS = 5

    # es = Elasticsearch()

# train_data instance and setting up with ES
    # train_data = pd.read_csv('data/train_data_2.csv')
    # train_data.dropna(subset=['text', 'response'], inplace=True)
    # texts_dict = train_data.to_dict(orient='records')
    # bulk(es, texts_dict, index='textbot', doc_type='clue', raise_on_error=True)

# create an app instance
app = Flask(__name__)


@app.route("/")  # at the end point /
def hello():  # call method hello
    # return "<h1>Hello World</h1>"
    return render_template('home.html')


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(user_text)
    # return chat(user_text)


    # def chat(user_text):
    #
    #     # Get response from ES
    #     response = es.search(index='textbot', doc_type='clue', body={"query": {
    #         "match": {
    #             "text": user_text
    #         }
    #     }})
    #
    #     # Use randomness function and get hit on response
    #     try:
    #         i = randint(0, RANDOMNESS)
    #         return response['hits']['hits'][i]['_source']['response']
    #     except:
    #         return "LOST FOR WORDS"


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
