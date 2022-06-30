import subprocess
from tkinter import*
from tkinter import messagebox
import wolframalpha
import pyttsx3
import json
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import time
import shutil
from twilio.rest import Client
from textui import *
import requests
#from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning  !")

	elif hour>= 12 and hour<18:
		speak("Good Afternoon  !")

	else:
		speak("Good Evening  !")

	assistantname ="Lucy"
	speak("I am your Assistant")
	speak(f"My name is {assistantname}")

	# speak("These are the applications that I can open")
	# print("Wikipedia""\n Youtube""\n2048 video game""\n Google")
	
	

def username():
	speak("What should I call you ?")
	uname = takeCommand()
	speak(f"Welcome,{uname}")

	
	print("Welcome ", uname)

	print("These are the applications that I can open")
	speak("These are the applications that I can open")
	print("Wikipedia")	
	print("Youtube")
	print("2048 Video game")
	print("Google")
	

def takeCommand():
	
	# r = sr.Recognizer()
	
	# with sr.Microphone() as source:
		
	# 	print("Listening...")
	# 	audio=r.adjust_for_ambient_noise(source)
	# 	r.pause_threshold = 1
	# 	audio = r.listen(source)

	# try:
	# 	print("Recognizing...")
	# 	query = r.recognize_google(audio, language ='en-in')
	# 	print(f"User said: {query}\n")

	# except Exception as e:
	# 	print(e)
	# 	print("Unable to Recognize your voice.")
	# 	return "None"
	query=input()
	print("Listening...\nRecognizing...")
	print(f"User said: {query}\n")
	return query

if __name__ == '__main__':
	clear = lambda: os.system('cls')
	
	# This Function will clean any
	# command before execution of this python file
	clear()
	wishMe()
	username()
	
	while True:
		
		query = takeCommand().lower()
		
		# All the commands said by user will be
		# stored here in 'query' and will be
		# converted to lower case for easily
		# recognition of command
		if 'open wikipedia' in query or 'wikipedia kholo' in query or 'wikipedia' in query:
			speak('Here you go to Wikipedia...')
			webbrowser.open("wikipedia.com")
			

		elif 'open youtube' in query or 'youtube kholo' in query:
			speak("Here you go to Youtube\n")
			webbrowser.open("youtube.com")

		elif 'open google' in query or 'google kholo' in query or 'google' in query:
			speak("Here you go to Google\n")
			webbrowser.open("google.com")

		elif 'open 2048' in query or 'start video game' in query:
			speak("opening 2048\n")	
			speak("In this game your final motive is to get 2048 on a single tile, this can be done by moving the rows and columns")
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
			# speak("My friends call me")
			# speak(assistantname)
			print("My friends call me", assistantname)
			
		elif "who made you" in query or "who created you" in query:
			speak("I was created by Parth Chaudhary, Dhairya Thakkar and Vivek Iyer")
			
		elif 'tell me a joke' in query:
			joke = pyjokes.get_joke()
			print(joke)
			speak(joke)
         
		# elif "calculate" in query:
			
		# 	app_id = "Wolframalpha api id"
		# 	client = wolframalpha.Client(app_id)
		# 	indx = query.lower().split().index('calculate')
		# 	query = query.split()[indx + 1:]
		# 	res = client.query(' '.join(query))
		# 	answer = next(res.results).text
		# 	print("The answer is " + answer)
		# 	speak("The answer is " + answer)

		elif "why you came to world" in query:
			speak("I came into existance because of a Mini Project assigned to Dhairya,Vivek and Parth")

# make function if name is changed.
		elif "who are you" in query:
			speak("I am your virtual assistant Lucy.")

        
		elif "don't listen" in query or "stop listening" in query:
			speak("For how many seconds do you want to stop Lucy from listening commands")
			a = int(takeCommand())
			time.sleep(a)
			print(a)

	
# make txt file, where notes will be made
		elif "write a note" in query:
			speak("What should i write, sir")
			note = takeCommand()
			file = open('notes.txt', 'w')
			file.write(note)
		
		elif "show note" in query:
			speak("Showing Notes")
			file = open("notes.txt", "r")
			print(file.read())
			speak(file.read(6))

					
		# NPPR9-FWDCX-D2C8J-H872K-2YT43
		elif "lucy" in query:
			
			wishMe()
			speak("Lucy your Voice Assisstant at your service")
			speak(assistantname)
			
# add other greetings

		elif "good morning" == query or "good afternoon" == query:
			print("A warm " +query)
			speak("A warm " +query)
			print("How are you ?")
			speak("How are you ?")
			day = takeCommand()
			if "i am good" in day or " i am great" in day:
				print("Glad to hear that!")
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
					print(x.text.strip())
					speak(x.text.strip())


		elif "good evening" == query:
			speak(f"A very {query}") #Add uname
			speak("How was your day?")
			day = takeCommand()
			if "good" in day or "great" in day or "it was good" in day or "it was great" in day:
				speak("I am glad to know that it went well!")
				

		elif "how are you" in query:
			speak("I'm great, glad you asked me ")

			
		# elif "what is" in query or "who is" in query:
			
		# 	# Use the same API key
		# 	# that we have generated earlier
		# 	client = wolframalpha.Client("API_ID")
		# 	res = client.query(query)
			
		# 	try:
		# 		print(next(res.results).text)
		# 		speak(next(res.results).text)
		# 	except StopIteration:
		# 		print ("No results")
		elif 'exit' in query or 'bye' in query:
			speak("Thanks for giving me your time")


		elif 'tata' in query:
			speak('Apke waqt ke lie dhanyawad')
			exit()		

		else:
			speak("i am unable to recognize your voice, please speak again")