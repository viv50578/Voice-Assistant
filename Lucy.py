import subprocess
from tkinter import*
from tkinter import messagebox
# import wolframalpha
import pyttsx3
import json
import speech_recognition as sr
import datetime
# import wikipedia
import webbrowser
import os
import pyjokes
import time
# import shutil
from twilio.rest import Client
from textui import *
import requests
#from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import threading

# Create the root (base) window where all widgets go
root = Tk()

# Create a Text widget
output = Text(root, background="white")
output.pack()

output.tag_config('user', foreground='blue')
output.tag_config('assistant', foreground='red')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    output.insert(END, "Assistant: " + str(audio) + "\n", 'assistant')  # Write to the Text widget

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning!")

    elif hour>= 12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    assistantname ="Lucy"
    speak(f"I am your Assistant {assistantname}")

def username():
    speak("What should I call you?")
    uname = takeCommand()
    speak(f"Welcome,{uname}")
    # output.insert(END, "Welcome " + uname + "\n")
    # output.insert(END, "These are some of the applications that I can open\n")
    speak("These are some of the applications that I can open")
    output.insert(END, "Wikipedia\n")    
    output.insert(END, "Youtube\n")
    output.insert(END, "2048 Video game\n")
    output.insert(END, "Google\n")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output.insert(END, "Listening...\n", 'assistant')
        audio = r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        output.insert(END, "Recognizing...\n", 'assistant')
        query = r.recognize_google(audio, language ='en-in')
        output.insert(END, "User: " + query + "\n", 'user')
    except Exception as e:
        output.insert(END, str(e) + "\n", 'assistant')
        output.insert(END, "Unable to Recognize your voice.\n", 'assistant')
        return "None"
    return query

def main_loop():
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    username()
    
    while True:
        query = takeCommand().lower()
        if query:
            if 'open wikipedia' in query or 'wikipedia kholo' in query or 'wikipedia' in query:
                speak('Here you go to Wikipedia\n')
                webbrowser.open("wikipedia.com")

            elif 'open youtube' in query or 'youtube kholo' in query:
                speak("Here you go to Youtube\n")
                webbrowser.open("youtube.com")

            elif 'open google' in query or 'google kholo' in query or 'google' in query:
                speak("Here you go to Google\n")
                webbrowser.open("google.com")

            elif 'open 2048' in query or 'start video game' in query:
                speak("Opening 2048\n")    
                speak("In this game your final motive is to get 2048 on a single tile, this can be done by moving the rows and columns using arrow keys")
                exec(open("2048.py").read() )

            elif 'what is the time' in query or 'time' in query or 'time kya hai' in query:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                speak(f"The time is {strTime}")

            elif 'How are you Lucy' in query:
                speak("I am fine, Thank you")
                speak("How are you, Sir")

            elif 'fine' in query or "great" in query or "awesome" in query:
                speak("It's good to know that you are fine")

            elif "change my name to" in query:
                query = query.replace("change my name to", "")
                uname = query

            elif "change name" in query:
                speak("What would you like to call me, Sir ")
                assistantname = takeCommand()
                speak("Thanks for naming me")

            elif "what's your name" in query or "tumhara naam kya hai" in query:
                output.insert(END, "My friends call me " + assistantname + "\n")
                
            elif "who made you" in query or "who created you" in query:
                speak("I was created by Parth Chaudhary, Dhairya Thakkar and Vivek Iyer")
                
            elif 'tell me a joke' in query:
                joke = pyjokes.get_joke()
                output.insert(END, joke + "\n")
                speak(joke)
            
            elif "why you came to world" in query:
                speak("I came into existance because of a Mini Project assigned to Dhairya,Vivek and Parth")

            elif "who are you" in query:
                speak("I am your virtual assistant Lucy.")

            elif "don't listen" in query or "stop listening" in query:
                speak("For how many seconds do you want to stop me from listening to commands")
                a = int(takeCommand())
                time.sleep(a)
                output.insert(END, str(a) + "\n")

            elif "write a note" in query:
                speak("What should i write, sir?")
                note = takeCommand()
                file = open('notes.txt', 'w')
                file.write(note)
            
            elif "show note" in query:
                speak("Showing Notes")
                file = open("notes.txt", "r")
                output.insert(END, file.read() + "\n")
                speak(file.read(6))

            elif "lucy" in query:
                wishMe()
                speak("Lucy your Voice Assisstant at your service")
                speak(assistantname)
                
            elif "good morning" == query or "good afternoon" == query:
                output.insert(END, "A warm " + query + "\n")
                speak("A warm " + query)
                output.insert(END, "How are you ?\n")
                speak("How are you ?")
                day = takeCommand()
                if "i am good" in day or " i am great" in day:
                    output.insert(END, "Glad to hear that!\n")
                    speak("Glad to hear that!")

            elif "tell me the current news" in query:
                url = 'https://www.bbc.com/news'
                response = requests.get(url)

                soup = BeautifulSoup(response.text, 'html.parser')
                headlines = soup.find('body').find_all('h3')
                unwanted = ['BBC World News TV', 'BBC World Service Radio',
                            'News daily newsletter', 'Mobile app', 'Get in touch']
                
                headlines_list = list(dict.fromkeys(headlines))
                final_list = headlines_list[:5]

                for x in final_list:
                    if x.text.strip() not in unwanted:
                        output.insert(END, x.text.strip() + "\n")
                        speak(x.text.strip())

            elif "good evening" == query:
                speak(f"A very {query}") #Add uname
                speak("How was your day?")
                day = takeCommand()
                if "good" in day or "great" in day or "it was good" in day or "it was great" in day:
                    speak("I am glad to know that it went well!")

            elif "how are you" in query:
                speak("I'm great, glad you asked me ")

            elif 'exit' in query or 'bye' in query:
                speak("Thanks for giving me your time")
                exit()

            elif 'tata' in query:
                speak('Apke waqt ke liye dhanyawad')
                exit()        

            else:
                speak("I am unable to recognize your voice, please speak again")

# Run the main loop in a separate thread
threading.Thread(target=main_loop).start()

# Run the event loop (needed for all Tkinter-based applications)
root.mainloop()
