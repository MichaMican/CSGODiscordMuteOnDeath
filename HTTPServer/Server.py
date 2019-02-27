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

deaths = 0
gameRound = 0
isMuted = False
pause = False


#This awesome variable is necessary because pynput is a peace of human garbage (Or maybe i implemented it wrong and i'm a peace of human garbage)
stupidBooleanOfFUCK = False


@app.route("/read", methods=['GET'])
def read_data():
    data = ''
    with open(game_data, 'r') as f:
        data = f.read()
    return data


@app.route("/", methods=['POST'])
def write_data():
    data = request.get_json()
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
    global gameRound
    global isMuted
    global stupidBooleanOfFUCK
    
    currentDeaths = deaths
    currentRound = gameRound

    if stupidBooleanOfFUCK:
        stupidBooleanOfFUCK = False
        try:
            deaths = data["player"]["match_stats"]["deaths"]
            gameRound = data["map"]["round"]
            print("UPDATED")
        except:
            print("Player is not in a match :(")
            deaths = 0
            gameRound = 0

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
    if currentRound > gameRound:
        gameRound = currentRound
        if isMuted and not pause:
            isMuted = False
            unMute()
            print("UNMUTED!")


def on_press(key):
    global pause
    global deaths
    global gameRound
    global stupidBooleanOfFUCK
    global isMutedklnkln
    

    keyChar = ''
    try:
        keyChar = format(key.char)
    except AttributeError:
        foo = 0
    except:
        print("Es gab nen fehler beim Taste einlesen - Nichts worüber man sich sorgen machen sollte")
    
    if keyChar == 'i':
        pause = not pause
        print ("Pause ist " + str(pause))
        if pause:
            if isMuted:
                isMuted = False
                unMute()
        if not pause:
            stupidBooleanOfFUCK = True

        
    if keyChar == 'o':
        deaths = 0
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

    keyboardOut.press('k')
    keyboardOut.press('l')
    keyboardOut.press('n')
    keyboardOut.release('k')
    keyboardOut.release('l')
    keyboardOut.release('n')


thread = Thread(target=startKeyListener, args=())
thread.start()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
    #app.run(host='0.0.0.0', port=5000)