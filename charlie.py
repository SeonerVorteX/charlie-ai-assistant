import os
import sys
import pyttsx3
import speech_recognition as sr
from CommandManager import CommandManager
from functions import *
sys.excepthook = sys.__excepthook__

class Charlie:
    def __init__(self):
        self.configs = load_json("helpers/configurations.json")
        self.intents = load_json("helpers/intents.json")
        self.commands = CommandManager()
        self.get_audio_exception_count = 0
        self.ready = False
        self.datas = {}

    def log(self, text):
        print(f"[CHARLIE] {text}")

    def set_voice_settings(self, rate=125, volume=1.0):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        if(text == ""):
            return
        if not(self.ready):
            self.ready = True
        
        self.log(text)
        self.engine.say(text)
        self.engine.runAndWait()
    
    def get_audio(self, text="your commands...", log=True):
        if log:
            self.log(f"Listening to {text}")
        with sr.Microphone() as source:
            audio = self.r.listen(source)
            said = ""

            try:
                said = self.r.recognize_google(audio)
                self.log(f"You: {said}")
            except Exception as e:
                said = ""
                self.get_audio_exception_count += 1
                if str(e):
                    self.log("Exception: " + str(e))
            return said
    
    def on_start(self):
        self.ready = True
        text = array_random(self.configs["system"]["start_messages"])
        self.speak(text)
    
    def on_end(self):
        self.kill()
        sys.exit()
    
    def on_command(self, command):
        cmd = self.commands.get(command)
        
        if cmd:
            cmd.callback(self)
    
    def sleep(self):
        self.ready = False
        text = array_random(self.configs["system"]["sleep_messages"])
        self.speak(text)
    
    def call(self):
        self.ready = True
        self.get_audio_exception_count = 0
        text = array_random(self.configs["system"]["call_messages"])
        self.speak(text)
    
    def did_not_undestand(self):
        self.speak(array_random(self.configs["system"]["did_not_understand_messages"]))
    
    def upload_datas(self):
        for data_file in os.listdir(os.getcwd() + "\datas"):
            if data_file.endswith(".json"):
                data = load_json(f"datas/{data_file}")
                self.datas[data_file.split(".")[0]] = data

    def kill(self):
        self.engine.stop()