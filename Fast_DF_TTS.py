import requests # pip install requests
from playsound import playsound # pip install playsound==1.2.2
import os
from typing import Union # pip install typing
import sys
import time
import threading
from TTS.api import TTS  # Add this import at the top

def generate_audio(message: str,voice : str = "Matthew"):
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={message}"

    headers = {'User-Agent':'Mozilla/5.0(Maciontosh;intel Mac OS X 10_15_7)AppleWebKit/537.36(KHTML,like Gecoko)Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
    
def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.050)  # Adjust the sleep duration for the animation speed
    print()

def play_audio(file_path: str):
    """Play audio in a separate thread to avoid blocking."""
    playsound(file_path)

def Co_speak(message: str, voice: str = "Matthew", extension: str = ".mp3") -> Union[None, str]:
    try:
        folder = os.path.join(os.getcwd(), "audio_files")
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print(f"Failed to create directory: {e}")
                folder = os.getcwd()  # Fallback to current directory
            
        result_content = generate_audio(message, voice)
        if result_content is None:
            print("Failed to generate audio content")
            return "Failed to generate audio"
            
        file_path = os.path.join(folder, f"speech{extension}")
        
        # Remove old file if it exists
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
            
        # Write new audio file
        with open(file_path, "wb") as file:
            file.write(result_content)
        
        # Add a small delay
        time.sleep(0.1)
        
        # Play the audio in a separate thread
        audio_thread = threading.Thread(target=play_audio, args=(file_path,))
        audio_thread.start()
        
        # Clean up
        try:
            audio_thread.join()  # Wait for the audio to finish playing
            os.remove(file_path)
        except:
            pass
            
        return None
        
    except Exception as e:
        print(f"Error in Co_speak: {str(e)}")
        return str(e)

def speak(text):
    """Main speaking function that uses Co_speak for TTS"""
    try:
        if isinstance(text, bool):  # Handle boolean responses
            return
        if not text or text.strip() == "":  # Handle empty responses
            return
        print(f"Assistant: {text}")  # Print response to terminal
        Co_speak(str(text))  # Convert to string to handle any type
    except Exception as e:
        print(f"Error in speak function: {e}")


#c