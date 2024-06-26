import subprocess
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage  # For image support
import pyttsx3
import json
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyjokes
import time
from twilio.rest import Client
from textui import *
import requests
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image, ImageTk  # For image resizing
import random
import pygame

# Create the root (base) window where all widgets go
root = Tk()
root.configure(bg="black")  # Set the background color of the root window to black

root.title('Lucy')

# Set the fixed window size
root.geometry("600x600")  # Width x Height
root.resizable(False, False)  # Disable resizing

# Create a Text widget
chat_frame = Frame(root, background="black")
chat_frame.pack(fill=BOTH, expand=True, pady=(0, 70))  # Leave space at the bottom for the mic button

# Configure the scrollbar
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=RIGHT, fill=Y)

output = Text(chat_frame, background="black", yscrollcommand=scrollbar.set, wrap=WORD)
output.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=output.yview)

output.tag_config('user', foreground='black', background='aqua')
output.tag_config('assistant', foreground='black', background='lightgreen')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

assistantname = "Lucy"  # Define assistantname as a global variable

def create_bubble(text, tag):
    text = f"{tag.capitalize()}: {text}"
    bubble = Frame(output, background=output.tag_cget(tag, 'background'), padx=5, pady=5)
    label = Label(bubble, text=text, wraplength=400, background=output.tag_cget(tag, 'background'), justify=LEFT if tag == 'assistant' else RIGHT, foreground=output.tag_cget(tag, 'foreground'))
    label.pack(fill=BOTH, expand=True)

    if tag == 'user':
        bubble.pack(anchor='e', padx=10, pady=5)  # Pack user bubble on the right
    else:
        bubble.pack(anchor='w', padx=10, pady=5)

    output.window_create(END, window=bubble)
    output.insert(END, "\n\n")  # Add space after each bubble
    output.see(END)  # Scroll to the end of the text widget

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    create_bubble(str(audio), 'assistant')

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak(f"I am your Assistant {assistantname}")

def username():
    speak("What should I call you?")
    uname = takeCommand()
    speak(f"Welcome {uname}")
    speak("These are some of the applications that I can open:")
    create_bubble("Wikipedia\nYoutube\n2048 Video game\nGoogle", 'assistant')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        create_bubble("Listening...", 'assistant')
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        create_bubble("Recognizing...", 'assistant')
        query = r.recognize_google(audio, language='en-in')
        create_bubble(query, 'user')  # Tag the user query as 'user'
    except Exception as e:
        create_bubble(str(e), 'assistant')
        # create_bubble("Unable to Recognize your voice.", 'assistant')
        return "None"
    return query

def process_query(query):
    global assistantname  # Access the global variable
    if query:
        query = query.lower()
        if 'open wikipedia' in query or 'wikipedia kholo' in query or 'wikipedia' in query:
            speak('Here you go to Wikipedia')
            webbrowser.open("wikipedia.com")

        elif 'open youtube' in query or 'youtube kholo' in query:
            speak("Here you go to Youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query or 'google kholo' in query or 'google' in query:
            speak("Here you go to Google")
            webbrowser.open("google.com")

        elif 'open 2048' in query or 'start video game' in query or '2048 kholo' in query:
            speak("Opening 2048")
            speak("In this game your final motive is to get 2048 on a single tile, this can be done by moving the rows and columns using arrow keys")
            exec(open("2048.py").read())

        elif 'open' in query:
            # Extracting the domain name after 'open'
            domain = query.split('open')[-1].strip()
            speak(f"Here you go to {domain}.com")
            webbrowser.open(f"https://{domain}.com")

        elif 'what is the time' in query or 'time' in query or 'samay kya hai' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            speak(f"The time is {strTime}")

        elif 'how are you' in query or 'aap kaise ho' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")
            command = takeCommand()
            if "i am good" in command or "i am great" in command or "i am fine" in command or "good" in command or "great" in command or "fine" in command:
                speak("Glad to hear that!")

        # elif 'fine' in query or "great" in query or "awesome" in query:
        #     speak("It's good to know that you are fine")

        elif 'do you know hindi' in query or 'tumhe hindi aati hai' in query or 'aapko hindi aati hai' in query:
            speak("Thoda Thoda")

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            uname = query

        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            assistantname = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in query or "what is your name" in query or "tumhara naam kya hai" in query:
            create_bubble("My friends call me " + assistantname, 'assistant')

        elif "who made you" in query or "who created you" in query or "tumhe kisne banaya" in query:
            speak("I was created by Parth Chaudhary, Dhairya Thakkar and Vivek Iyer")

        elif 'tell me a joke' in query or 'joke sunao' in query or 'tell me something' in query:
            joke = pyjokes.get_joke()
            # create_bubble(joke, 'assistant')
            speak(joke)

        elif "why you came to this world" in query or "tum is duniya me kyu aaye" in query:
            speak("I came into existence because of a Mini Project assigned to Dhairya, Vivek, and Parth")

        elif "who are you" in query or "tum kaun ho" in query:
            speak("I am your virtual assistant Lucy.")

        # elif "don't listen" in query or "stop listening" in query:
        #     speak("For how many seconds do you want to stop me from listening to commands")
        #     a = int(takeCommand())
        #     time.sleep(a)
        #     create_bubble(str(a), 'assistant')

        elif "write a note" in query:
            speak("What should I write, sir?")
            note = takeCommand()
            file = open('notes.txt', 'w')
            file.write(note)

        elif "show the note" in query:
            speak("Showing the note")
            file = open("notes.txt", "r")
            create_bubble(file.read(), 'assistant')
            speak(file.read(6))

        # elif "lucy" in query:
        #     wishMe()
        #     speak("Lucy your Voice Assistant at your service")
        #     speak(assistantname)

        elif "good morning" == query or "good afternoon" == query:
            speak("A warm " + query)
            speak("How are you?")
            day = takeCommand()
            if "i am good" in day or "i am great" in day or "i am fine" in day or "good" in day or "great" in day or "fine" in day:
                speak("Glad to hear that!")

        elif "tell me the current news" in query or 'news' in query:
            url = 'https://www.livemint.com/news'
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                headlines = soup.find('body').find_all('h2')
                unwanted = ['BBC World News TV', 'BBC World Service Radio',
                            'News daily newsletter', 'Mobile app', 'Get in touch']

                headlines_list = list(dict.fromkeys([h.text.strip() for h in headlines if h.text.strip() not in unwanted]))
                final_list = headlines_list[:5]

                for headline in final_list:
                    # create_bubble(headline, 'assistant')
                    speak(headline)
            else:
                speak("I couldn't fetch the news at the moment.")

        elif "good evening" == query:
            speak(f"A very {query}")  # Add uname
            speak("How was your day?")
            day = takeCommand()
            if "good" in day or "great" in day or "fine" in day or "it was good" in day or "it was great" in day or "it was fine" in day:
                speak("I am glad to know that it went well!")

        elif "how are you" in query or 'aap kaise ho' in query:
            speak("I'm great, glad you asked me")

        elif 'exit' in query or 'bye' in query:
            speak("Thanks for giving me your time")
            exit()

        elif 'tata' in query:
            speak('Apke waqt ke liye dhanyawad')
            exit()

        else:
            speak("I am unable to recognize your voice, please speak again")

def on_mic_click():
    threading.Thread(target=lambda: process_query(takeCommand())).start()

# Load and resize microphone image
mic_image = Image.open("mic.png")
mic_image = mic_image.resize((47, 47), Image.LANCZOS)
mic_photo = ImageTk.PhotoImage(mic_image)

# Create microphone button with a white border
mic_button = Button(root, image=mic_photo, command=on_mic_click, bg="black", activebackground="black", borderwidth=10, highlightbackground="white", highlightcolor="white", highlightthickness=2)
mic_button.place(relx=0.5, rely=1, anchor=S)

# Initial welcome messages and setup
def initial_setup():
    wishMe()
    username()

threading.Thread(target=initial_setup).start()

# Run the event loop (needed for all Tkinter-based applications)
root.mainloop()
