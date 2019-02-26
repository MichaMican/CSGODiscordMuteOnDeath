#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_cors import CORS
import json
from threading import Thread, Lock


app = Flask(__name__)
CORS(app)

game_data = "./IO/game_data.json"

idx = 0
deaths = 0

@app.route("/read", methods=['GET'])
def read_data():
    data = ''
    with open(game_data, 'r') as f:
        data = f.read()
    return data


@app.route("/", methods=['POST'])
def write_data():
    global idx
    idx += 1
    data = request.get_json()
    data["id"] = str(idx)
    analyse(data)
    #with open(game_data, 'w') as f:
        #f.write(json.dumps(data))
    return "OK", 200


@app.route("/")
def index():
    #return render_template("index.html")
    return "OK", 200


def analyse(data):
    global deaths
    if deaths > data["player"][0]["match_stats"][0]["deaths"]:
        deaths = data["player"][0]["match_stats"][0]["deaths"]
        print("MUTED!")



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
    #app.run(host='0.0.0.0', port=5000)
