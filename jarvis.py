from ui import start_ui
import threading
import sys
from internet_check import is_Online
from Alert import Alert
from Data.DLG_Data import online_dlg,offline_dlg
import random
from co_brain import Jarvis
from TextToSpeech.Fast_DF_TTS import speak
from Automation.Battery  import check_plug
from Time_Operations.throw_alert import check_schedule,check_Alam
from os import getcwd

Alam_path = f"{getcwd()}\\Alam_data.txt"
file_path = f'{getcwd()}\\schedule.txt'

ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)


def main():
    if is_Online():
        try:
            # Initialize all threads
            t1 = threading.Thread(target=speak, args=(ran_online_dlg,), name="SpeechThread")
            t3 = threading.Thread(target=check_plug, name="BatteryThread")
            t4 = threading.Thread(target=check_schedule, args=(file_path,), name="ScheduleThread")
            t5 = threading.Thread(target=Jarvis, name="JarvisThread")
            t6 = threading.Thread(target=check_Alam, args=(Alam_path,), name="AlarmThread")

            # Start all threads
            threads = [t1, t3, t4, t5, t6]
            for t in threads:
                t.daemon = True  # Make threads daemon so they exit when main program exits
                print(f"Starting thread: {t.name}")
                t.start()

            # Optional: Wait for speech to complete before continuing
            t1.join()

            # Let other threads run independently
            # Only join non-daemon threads if you need to wait for them
            # for t in [t3, t4, t5, t6]:
            #     t.join()

        except Exception as e:
            print(f"Error in main thread: {e}")
    else:
        Alert(ran_offline_dlg)

if __name__ == "__main__":
    try:
        app, ui = start_ui()
        # Run the main Jarvis function in a separate thread
        main_thread = threading.Thread(target=main, daemon=True, name="MainThread")
        main_thread.start()
        # Start the UI event loop
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {e}")