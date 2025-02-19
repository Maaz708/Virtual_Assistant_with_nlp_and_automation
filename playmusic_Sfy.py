import webbrowser
import pyautogui as ui
import time
from TextToSpeech.Fast_DF_TTS import speak

def play_music_on_spotify(song_name):
    try:
        # Open Spotify web player
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com/")
        time.sleep(6)  # Wait for page to load
        
        # Search for the song
        ui.hotkey("ctrl", "shift", "l")
        time.sleep(1)
        ui.write(song_name)
        time.sleep(3)
        
        # Click on the first result
        try:
            ui.leftClick(805, 515)
            speak(f"Playing {song_name} on Spotify")
            return True
        except:
            speak("Couldn't click the play button")
            return False
            
    except Exception as e:
        print(f"Error playing music: {e}")
        speak("Sorry, I couldn't play the song on Spotify")
        return False

def play_random_spotify():
    try:
        # Open Spotify web player
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com/")
        time.sleep(6)
        
        # Click on "Made for You" section
        ui.leftClick(100, 250)  # Adjust these coordinates based on your screen
        time.sleep(2)
        
        # Click play on the first playlist
        ui.leftClick(400, 400)  # Adjust these coordinates based on your screen
        speak("Playing random music from your recommendations")
        return True
        
    except Exception as e:
        print(f"Error playing random music: {e}")
        speak("Sorry, I couldn't play random music")
        return False

def pause_spotify():
    try:
        ui.hotkey('space')
        speak("Music paused")
        return True
    except:
        speak("Couldn't pause the music")
        return False

def resume_spotify():
    try:
        ui.hotkey('space')
        speak("Resuming music")
        return True
    except:
        speak("Couldn't resume the music")
        return False
