#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_cors import CORS
import json
from threading import Thread, Lock
from pynput import keyboard
import os


app = Flask(__name__)
CORS(app)

game_data = "./IO/game_data.json"

idx = 0
deaths = 0
gameRound = 0
isMuted = False
pause = False

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
    with open(game_data, 'w') as f:
        f.write(json.dumps(data))
    return "OK", 200


@app.route("/")
def index():
    #return render_template("index.html")
    return "OK", 200


def analyse(data):
    global deaths
    global gameRound
    global isMuted
    
    currentDeaths = deaths
    currentRound = gameRound
    try:
        currentDeaths = data["player"]["match_stats"]["deaths"]
        currentRound = data["map"]["round"]
    except:
        print("Player is not in a match")
        deaths = 0
        currentDeaths = 0
        currentRound = 0
        gameRound = 0

    #This part mutes the user
    if currentDeaths > deaths and not isMuted and not pause:
        deaths = currentDeaths
        isMuted = True
        mute()
        print("MUTED!")

    #This part unmutes the user
    if currentRound > gameRound and isMuted and not pause:
        isMuted = False
        gameRound = currentRound
        unMute()
        print("UNMUTED!")


def on_press(key):
    global pause
    global deaths
    global currentDeaths
    global currentRound
    global gameRound

    keyChar = ''
    try:
        keyChar = format(key.char)
    except AttributeError:
        foo = 0
    except:
        print("Es gab nen fehler beim Taste einlesen - Nichts worüber man sich sorgen machen sollte")
    
    if keyChar == 'i':
        pause = not pause
        print ("Pause ist "+str(pause))
    if keyChar == 'o':
        deaths = 0
        currentDeaths = 0
        currentRound = 0
        gameRound = 0
        print ("RESET")


def on_release(key):
    if key == keyboard.Key.page_down:
        # Stop listener
        os._exit(1)
        return False

def startKeyListener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def mute():
    keyboardOut = keyboard.Controller()

    keyboardOut.press('k')
    keyboardOut.press('l')
    keyboardOut.press('n')
    keyboardOut.release('k')
    keyboardOut.release('l')
    keyboardOut.release('n')


def unMute():
    keyboardOut = keyboard.Controller()

    keyboardOut.press('p')
    keyboardOut.press('n')
    keyboardOut.press('m')
    keyboardOut.release('p')
    keyboardOut.release('n')
    keyboardOut.release('m')


if __name__ == '__main__':
    thread = Thread(target=startKeyListener, args=())
    thread.start()
    app.run(host='127.0.0.1', port=3000, debug=True)
    #app.run(host='0.0.0.0', port=5000)