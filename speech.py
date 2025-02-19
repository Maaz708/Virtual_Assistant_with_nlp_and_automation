import speech_recognition as sr
import logging
import time
from threading import Event
import queue

# Event flags for thread synchronization
should_listen = Event()
should_listen.set()  # Start in listening mode
processing_event = Event()

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.setup_recognizer()
        self.setup_logging()
        self.input_file = "input.txt"
        self.audio_queue = queue.Queue()
        self.last_sample = time.time()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('speech_recognition.log')
            ]
        )

    def setup_recognizer(self):
        # Optimized settings for better recognition
        self.recognizer.energy_threshold = 3000  # Lowered for better sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.6  # Reduced for faster response
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.4  # Reduced for faster detection

    def continuous_listen(self):
        microphone = sr.Microphone()
        with microphone as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready to listen!")

        while True:
            if not should_listen.is_set():
                time.sleep(0.1)
                continue
                
            try:
                with microphone as source:
                    print("Listening...") if time.time() - self.last_sample > 1 else None
                    self.last_sample = time.time()
                    
                    audio = self.recognizer.listen(
                        source,
                        timeout=None,  # Remove timeout for continuous listening
                        phrase_time_limit=5  # Limit phrase length
                    )
                    
                    self.audio_queue.put(audio)
                    self.process_audio()
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logging.error(f"Error in continuous listening: {e}")
                time.sleep(0.5)
                continue

    def process_audio(self):
        while not self.audio_queue.empty():
            audio = self.audio_queue.get()
            try:
                if should_listen.is_set():  # Check again before processing
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        text = text.lower().strip()
                        print(f"Recognized: {text}")
                        
                        # Set processing flag before saving
                        processing_event.set()
                        should_listen.clear()  # Stop listening while processing
                        
                        self.save_to_file(text)
                        
                        # Reset listening after processing
                        should_listen.set()  # Allow listening again
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                logging.error(f"Could not request results; {e}")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error processing audio: {e}")

    def save_to_file(self, text):
        try:
            with open(self.input_file, "w", encoding='utf-8') as file:
                file.write(text)
            logging.info(f"Saved to file: {text}")
        except Exception as e:
            logging.error(f"Error saving to file: {e}")

    def listen_for_file_name(self):
        """Listen for the file name input from the user."""
        should_listen.set()  # Ensure listening is enabled
        while True:
            if self.audio_queue.qsize() > 0:
                audio = self.audio_queue.get()
                try:
                    file_name = self.recognizer.recognize_google(audio)
                    print(f"File name recognized: {file_name}")  # Debugging statement
                    should_listen.set()  # Reset listening state
                    return file_name  # Return the recognized file name
                except sr.UnknownValueError:
                    print("Could not understand audio, please try again.")
                except Exception as e:
                    print(f"Error recognizing file name: {e}")
                    return None  # Return None if recognition fails

def listen():
    """Main listening loop."""
    recognizer = SpeechRecognizer()
    recognizer.continuous_listen()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        listen()  # Start listening for commands
    except KeyboardInterrupt:
        logging.info("Speech recognition stopped by user")
    except Exception as e:
        logging.error(f"Critical error in speech recognition: {e}")
        time.sleep(2)  # Wait before restarting