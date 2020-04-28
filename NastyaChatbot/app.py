# app.py

from flask import Flask, render_template, request  # import flask

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return render_template('home.html')


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)


def chat(userText):
    pass


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
