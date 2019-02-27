#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_cors import CORS
import json
from threading import Thread, Lock
from pynput import keyboard
import time
import os


app = Flask(__name__)
CORS(app)

TIME_TILL_MUTE = 5

deaths = 0
gameRound = 0
isMuted = False
pause = False
mutingTrigger = False
muteBlock = False

#This awesome variable is necessary because pynput is a peace of human garbage (Or maybe i implemented it wrong and i'm a peace of human garbage)
stupidBooleanOfFUCK = False


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
    global mutingTrigger
    
    currentDeaths = deaths
    currentRound = gameRound

    #Update after unpause
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

    #checking if player is in match - if so - get player data of player
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
        print("MUTE Registriert")
        isMuted = True
        mutingTrigger = True
        

    #This part unmutes the user
    if currentRound > gameRound:
        gameRound = currentRound
        if isMuted and not pause:
            print("UNMUTE Registriert")
            isMuted = False
            mutingTrigger = True


def on_press(key):
    global pause
    global deaths
    global gameRound
    global stupidBooleanOfFUCK
    global isMuted
    global mutingTrigger
    
    #Pause the programm (in case you take over the bot)
    if key == keyboard.Key.f5:
        pause = not pause
        print ("Pause ist " + str(pause))
        if pause:
            if isMuted:
                print("UNMUTE Registriert")
                isMuted = False
                mutingTrigger = True
                
        if not pause:
            stupidBooleanOfFUCK = True

    #Reset the programm (in case something went horribly wrong)
    if key == keyboard.Key.page_down:
        deaths = 0
        gameRound = 0
        print ("RESET")
        

def on_release(key):
    # Stop programm
    if key == keyboard.Key.page_up:
        os._exit(1)
        return False

def startKeyListener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def mute():
    global TIME_TILL_MUTE
    global mutingTrigger
    global muteBlock
    while 1:
        if mutingTrigger and isMuted:
            mutingTrigger = False
            muteBlock = True
            time.sleep(TIME_TILL_MUTE)
            muteBlock = False
            if isMuted:
                print("MUTED")
                keyboardOut = keyboard.Controller()
                keyboardOut.press('k')
                keyboardOut.press('l')
                keyboardOut.press('n')
                keyboardOut.release('k')
                keyboardOut.release('l')
                keyboardOut.release('n')
    


def unMute():
    global TIME_TILL_MUTE
    global mutingTrigger
    global muteBlock
    while 1:
        if mutingTrigger and muteBlock:
            mutingTrigger = False
        elif mutingTrigger and not isMuted:
            mutingTrigger = False
            print("UNMUTED")
            keyboardOut = keyboard.Controller()
            keyboardOut.press('k')
            keyboardOut.press('l')
            keyboardOut.press('n')
            keyboardOut.release('k')
            keyboardOut.release('l')
            keyboardOut.release('n')
        


keyListenerThread = Thread(target=startKeyListener, args=())
muteThread = Thread(target=mute, args=())
unMuteThread = Thread(target=unMute, args=())


keyListenerThread.start()
muteThread.start()
unMuteThread.start()



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
    #app.run(host='0.0.0.0', port=5000)