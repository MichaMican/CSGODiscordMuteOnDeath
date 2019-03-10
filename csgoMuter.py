#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_cors import CORS
import json
from threading import Thread, Lock
from pynput import keyboard
import time
import datetime
import os


app = Flask(__name__)
CORS(app)

TIME_TILL_MUTE = 4

roundBlockTimer = datetime.datetime.now()
deaths = 0
gameRound = 0
isMuted = False
pause = False
mutingTrigger = False
muteBlock = False
player = ""
init = True

#This awesome variable is necessary because pynput is a peace of human garbage (Or maybe i implemented it wrong and i'm a peace of human garbage)
stupidBooleanOfFUCK = False


@app.route("/", methods=['POST'])
def write_data():
    data = request.get_json()
    analyse(data)
    return "OK", 200


@app.route("/")
def index():
    return "OK", 200


def analyse(data):
    global roundBlockTimer
    global deaths
    global gameRound
    global isMuted
    global stupidBooleanOfFUCK
    global mutingTrigger
    global player
    global init

    unMuteThisRound = False
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
            init = True
            roundBlockTimer = datetime.datetime.now() - datetime.timedelta(seconds=10)

    #checking if player is in match - if so - get player data of player
    try:
        currentDeaths = data["player"]["match_stats"]["deaths"]
        currentPlayer = data["player"]["name"]
        currentRound = data["map"]["round"]
        currentPhase = data["map"]["phase"]
        currentRoundPhase = data["round"]["phase"]
        currentActivity = data["player"]["activity"]
    except:
        print("Player is not in a match")
        deaths = 0
        currentDeaths = 0
        currentRound = 0
        currentPlayer = ""
        currentPhase = ""
        currentRoundPhase = ""
        currentActivity = ""
        gameRound = 0
        if isMuted:
            print("UNMUTE Registriert")
            isMuted = False
            unMute()
        init = True

    if currentRoundPhase == "freezetime" and init:
        player = currentPlayer
        init = False
        print("PLAYER SET TO: " + player)

    if currentRoundPhase == "freezetime" and not init:
        roundBlockTimer = datetime.datetime.now()
        deaths = currentDeaths
        gameRound = currentRound

    print("Player Name: " + currentPlayer)
    print("Saved Player Name: " + player)
    print("Deaths: " + str(currentDeaths))
    print("Round: " + str(currentRound))
    print("SavedDeaths: " + str(deaths))
    print("SavedRound: " + str(gameRound))
    print("Phase: " + currentPhase)
    print("Round Phase: " + currentRoundPhase)
    print("Activity: " + currentActivity)
    print("Unmute this Round: " + str(unMuteThisRound))
    print("MUTE STATE:" + str(isMuted))

    #This part unmutes the user
    if currentRound > gameRound:
        gameRound = currentRound
        deaths = currentDeaths
        roundBlockTimer = datetime.datetime.now()
        print("New Round")
        if isMuted and not pause:
            print("UNMUTE Registriert")
            unMuteThisRound = True
            isMuted = False
            unMute()
    

    #This part mutes the user
    if currentDeaths > deaths and not isMuted and not pause and currentPlayer == player and currentRoundPhase != "freezetime" and currentRoundPhase != "over":
        deaths = currentDeaths
        timeDifference = (datetime.datetime.now() - roundBlockTimer).total_seconds()
        if not unMuteThisRound and not currentRoundPhase == "over":
            if  timeDifference > 2:
                print("MUTE Registriert")
                isMuted = True
                mute()
            else:
                print("Mute was skipped with a timeDifference of" + str(timeDifference))
        else:
            print("Mute skipt due to resent unmute")



def on_press(key):
    global pause
    global deaths
    global gameRound
    global stupidBooleanOfFUCK
    global isMuted
    global mutingTrigger
    
    #Pause the programm (in case you take over the bot)
    if key == keyboard.Key.f6:
        pause = not pause
        print ("Pause ist " + str(pause))
        if pause:
            if isMuted:
                print("UNMUTE Registriert")
                isMuted = False
                unMute()
                
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
    global isMuted
    global muteBlock
    muteBlock = True
    print("Muteblock active")
    #This block is a workarround to threading, because my code with threads killed flask
    for sleep in range(TIME_TILL_MUTE * 100):
        if not isMuted:
            print("ESCAPE!")
            break
        else:
            time.sleep(0.01)
    muteBlock = False
    print("Muteblock deactivated")

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
    global muteBlock
    if not muteBlock:
        print("UNMUTED")
        keyboardOut = keyboard.Controller()
        keyboardOut.press('k')
        keyboardOut.press('l')
        keyboardOut.press('n')
        keyboardOut.release('k')
        keyboardOut.release('l')
        keyboardOut.release('n')

def debug():
    global isMuted
    while True:
        print(str(isMuted))        


keyListenerThread = Thread(target=startKeyListener, args=())
keyListenerThread.start()




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)