from Automation.Automation_Brain import Auto_main_brain,clear_file
#from NetHyTechSTT.listen import listen
from Speech_Recognition.speech import listen
from TextToSpeech.Fast_DF_TTS import speak
import threading
from Data.DLG_Data import online_dlg,offline_dlg
import random
from Automation.Battery import battery_Alert
from Time_Operations.brain import input_manage,input_manage_Alam
from Brain.brain import Main_Brain
from Features.create_file import create_file
from Vision.Vbrain import *
#from Vision.MVbrain import *
from Weather_Check.check_weather import get_weather_by_address
from Whatsapp_automation.wa import send_msg_wa
from TextToImage.gen_image import generate_image
from Features.mike_health import mike_health
from Features.speaker_health import speaker_health_test
from Features.br_persentage import check_br_persentage
from Features.set_br import set_brightness_windows
from Features.set_get_volume import *
from Features.check_running_app import *
from Features.find_my_ip import find_my_ip

numbers = ["1:","2:","3:","4:","5:","6:","7:","8:","9:"]
spl_numbers = ["11:","12:"]

ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)


def check_inputs():
    output_text = ""
    while True:
        with open("input.txt","r") as file:
            input_text = file.read().lower() 
        if input_text != output_text:
            output_text = input_text
            if output_text.startswith("tell me"):
                output_text = output_text.replace(" p.m.","PM")
                output_text = output_text.replace(" a.m.","AM")
                if "11:" in output_text or "12:" in output_text:
                    input_manage(output_text)
                    clear_file()
                else:
                    for number in numbers:
                        if number in output_text:
                           output_text = output_text.replace(number,f"0{number}")
                           input_manage(output_text)
                           clear_file()
                           
            elif output_text.startswith("set alarm"):
                output_text = output_text.replace(" p.m.","PM")
                output_text = output_text.replace(" a.m.","AM")
                if "11:" in output_text or "12:" in output_text:
                    input_manage_Alam(output_text)
                    clear_file()
                else:
                    for number in numbers:
                        if number in output_text:
                           output_text = output_text.replace(number,f"0{number}")
                           input_manage_Alam(output_text)
                           clear_file()

            elif "jarvis" in output_text:
                f = open('log.txt','a')
                f.write('\n'+'You : '+ output_text)
                response = Main_Brain(output_text)
                f.write('\n'+'jarvis : '+ response)
                speak(response)

            elif output_text.startswith("create"):
                if "file" in output_text:
                    create_file(output_text)

            elif "what is this" in output_text or "what can you see" in output_text:
                        image_path = "captured_image.png"
                        if capture_image_and_save(image_path):
                            encoded_image = encode_image_to_base64(image_path)
                            answer = vision_brain(encoded_image)
                            speak(answer)

            elif "what is in front of mobile camera" in output_text or "what can you see use mobile camera" in output_text:
                        image_path = "captured_image.png"
                        if capture_image_and_save(image_path):
                            encoded_image = encode_image_to_base64(image_path)
                            answer = vision_brain(encoded_image)
                            speak(answer)

            elif "check weather" in output_text:
                text = output_text.replace("check weather in","")
                ans = get_weather_by_address(text)
                speak(ans)

            elif "send message on whatsapp" in output_text:
                send_msg_wa()

            elif "generate image" in output_text:
                 text = output_text.replace("generate image","")
                 text = text.strip()
                 generate_image(text)
                 speak("image generated successfully")
            elif "find my ip" in output_text:
                 ip_address = find_my_ip()
                 speak(f"Your IP address is {ip_address}")

            elif "check mike" in output_text or "check mike health" in output_text or "check microphone" in output_text:
                 mike_health()

            elif "check speaker health" in output_text or "check speaker" in output_text:
                 speaker_health_test()

            elif "check brightness percentage" in output_text:
                 check_br_persentage()

            elif "set brightness percentage" in output_text:
                try:
                    set = output_text.replace("set brightness percentage to", "").strip()
                    set_brightness_windows(int(set))
                except ValueError:
                    speak("Please provide a valid brightness percentage.")

            elif "check volume level" in output_text:
                get_volume_windows()
                 
            elif "set volume level " in output_text:
                 set = output_text.replace("set volume level","")
                 set = set.replace("%","")
                 set_volume_windows(int(set))

            elif "check running application" in output_text:
                 check_running_app()
            else:
                Auto_main_brain(output_text)
                
                

def Jarvis():
    clear_file()
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=check_inputs)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    Jarvis()
