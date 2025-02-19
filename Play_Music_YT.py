import pywhatkit as pw

def play_music_on_youtube(song_name):
    try:
        pw.playonyt(song_name)
    except Exception as e:
        print(f"Error playing music on YouTube: {e}")
