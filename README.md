# CSGOMuteOnDeath
##### This Project uses the CS:GO Game State Integration to mute the player 4 seconds after he dies
CS:GO Game State Integration:
https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration

**Important! This programm was tested only in Matchmakeing and Wingman - The game needs to have a freezetime so the programm can initialize**

## How to Install (Quickstart):
1. Copy the .cfg file into the cfg folder of your CSGO installation (SteamLibrary\steamapps\common\Counter-Strike Global Offensive\csgo\cfg)
2. Set microphone in your communication program (e.g. Discord or TeamSpeak) toggle to K+L+N
3. Start csgoMuter.exe
4. Start game

## How to Install (for manual execution):
1. Install Python 3 (https://www.python.org/downloads/)  
(->Install pip (If not already installed with Python))
2. Install flask, flask_cors, pynput with pip (Open cmd and type `pip <package>`)
3. Copy the .cfg file into the cfg folder of your CSGO installation (SteamLibrary\steamapps\common\Counter-Strike Global Offensive\csgo\cfg)
4. Set microphone in your communication program (e.g. Discord or TeamSpeak) toggle to K+L+N
5. Open cmd and navigate to the folder of the repository
6. Type ``python csGoMuter.py`` or use the start.bat file
7. Start game

## How to Use:
**F6** - Pause the program  
**Page up** - closes the program  
**Page down** - Reset (incase something goes horribly wrong)
