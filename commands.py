import os
import wikipedia
import webbrowser
from Command import Command

commands = []

def google(charlie):
    run = True
    charlie.speak("What do you want to search for?")
    while run:
        text = charlie.get_audio("your answer...").lower()
        if text == "":
            charlie.speak('I did not understand your answer, please try again.')
            continue
        
        run = False
        charlie.log("Opening Google Chrome...")
        tabUrl = "http://google.com/search?q="
        webbrowser.open(tabUrl+text,new=2)
        charlie.speak("Google opened successfuly, you can look into your browser")

def wiki(charlie):
    run = True
    charlie.speak("What do you want to search for?")
    while run:
        text = charlie.get_audio("your answer...").lower()
        if text == "":
            charlie.speak('I did not understand your answer, please try again.')
            continue
        
        run = False
        charlie.log("Looking for Wikipedia...")
        try:
            charlie.speak("I found the following results:")
            charlie.speak(wikipedia.search(text))
        except:
            charlie.speak("I could not find any information about that")
            


commands.append(Command("close", lambda charlie: charlie.on_end()))
commands.append(Command("google", google))
commands.append(Command("wikipedia", wiki))