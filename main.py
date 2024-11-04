print("Loading tailsAssist...")
import speech_recognition as sr
import pygame
from gtts import gTTS
import threading
import time
import datetime
import json
import requests

pygame.init()
pygame.mixer.init()
version="0.1"
awake=False
active=False
tv=False
tvname="TV"
tvtype="TV"
tvip="TV"
headers = {
	'User-Agent': '(tails1154-assist, https://github.com/tails1154/tailsassist)',
	'Accept': 'application/json'
	}
print("Loaded modules!")
print("Loading integrations")
f = open("integrations.json", "r")
integrations=json.loads(f.read())
if integrations["tvname"]:
	print("Found TV in integrations.json")
	print("Loading TV...")
	tvname=integrations["tvname"]
	tvip=integrations["tvip"]
	tvtype=integrations["tvtype"]
	if tvtype == "roku":
		print("Loaded roku tv")
		tv=True
	else:
		print("tvtype not supported yet. Want to add support? make a pull request on github!")
		tv=False
else:
	tv=False
print("Starting...")
r = sr.Recognizer()






def sleeptimer():
	global active
	global awake
	print(active)
	print(awake)







def ttsplay(text):
	from gtts import gTTS
	tts = gTTS(text)
	tts.save('temp.mp3')
	pygame.mixer.music.unload()
	pygame.mixer.music.load("temp.mp3", "mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		1 + 1









def input():
	print("Wait for input")
	with sr.Microphone() as source:
    		print("Say something!")
    		audio = r.listen(source)
	try:
		return r.recognize_google(audio)
	except sr.UnknownValueError:
		print("Google speech could not understand audio")
	except sr.RequestError as e:
		print("Google speech error; {0}".format(e))



def tvremote():
	try:
		global tvip
		text=input().lower()
		if text == "help":
			ttsplay("To press up on the remote, say 'up'")
			ttsplay("To press down on the remote, say 'down'")
			ttsplay("To press left on the remote, say 'left'")
			ttsplay("To press right on the remote, say 'right'")
			ttsplay("To press power on the remote, say 'power'")
			ttsplay("To press OK on the remote, say 'OK'")
			ttsplay("To press Home on the remote, say 'home'")
			ttsplay("To quit, say 'quit'")
		if text == "left":
			ttsplay("Left")
			requests.post("http://" + tvip + ":8060/keypress/Left")
			tvremote()
		elif text == "right":
			ttsplay("Right")
			requests.post("http://" + tvip + ":8060/keypress/Right")
			tvremote()
		elif text == "up":
			ttsplay("Up")
			requests.post("http://" + tvip + ":8060/keypress/Up")
			tvremote()
		elif text == "down":
			ttsplay("Down")
			requests.post("http://" + tvip + ":8060/keypress/Down")
			tvremote()
		elif text == "power":
			ttsplay("Power")
			requests.post("http://" + tvip + ":8060/keypress/Power")
			tvremote()
		elif text == "okay":
			ttsplay("OK")
			requests.post("http://" + tvip + ":8060/keypress/Select")
			tvremote()
		elif text == "home":
			ttsplay("Home")
			requests.post("http://" + tvip + ":8060/keypress/Home")
			tvremote()
		elif text == "quit":
			ttsplay("Exiting")
		else:
			ttsplay("I could not understand that command")
			tvremote()
	except:
		print("Exception")
		tvremote()




def assist(text):
	global tvip
	global tvname
	text=text.lower()
	if text == "addition":
		ttsplay("Enter number 1 to add");

		pygame.mixer.music.unload()
		pygame.mixer.music.load("audio/wakeup.mp3", "mp3")
		pygame.mixer.music.play()
		try:
			num1=int(input())
			print(str(num1))
			ttsplay("Enter number 2 to add");
			pygame.mixer.music.unload()
			pygame.mixer.music.load("audio/wakeup.mp3", "mp3")
			pygame.mixer.music.play()
			num2=int(input())
			ttsplay(str(num1) + " plus " + str(num2) + " is:")
			ttsplay(str(num1 + num2))
		except:
			print("Exception")
			ttsplay("Exception! Did you say a number?")

	elif text == "date":
		current_time=datetime.datetime.now()
		ttsplay("The date and time is " + str(current_time))
	elif text == "tell me a joke":
		ttsplay("One moment")
		joke=json.loads(requests.get("https://official-joke-api.appspot.com/random_joke").text)
		ttsplay(joke["setup"])
		time.sleep(1)
		ttsplay(joke["punchline"])
	elif text == "help":
		ttsplay("Things you can say to me:")
		ttsplay("You can say addition to do addition")
		ttsplay("You can also say date and I will give you the date and time.")
		ttsplay("You can also say 'tell me a joke' and I will tell you a joke from the jokeAPI.")
		ttsplay("If configured properly, you can toggle power on your tv by saying 'Power tvname' and replace tvname with the tvname in integrations dot json.")
		ttsplay("If configured properly, you can also use your voice as a tv remote by saying 'tvname remote' and replace tvname with the tvname in integrations dot json")
		ttsplay("If configured properly, you can also search with your voice with your tv by saying 'search tvname' and replace tvname with the tvname in integrations dot json")
		ttsplay("If configured properly, you can also start youtube (if installed) on your tv by saying 'start youtube on tvname' and replace tvname with the tvname in integrations dot json")
		ttsplay("Thats all!")
	elif text == "power " + tvname.lower():
		if tv:
			ttsplay("Toggle power on TV")
			if requests.post("http://" + tvip + ":8060/keypress/Power").status_code == 200:
				ttsplay("Toggled power on TV")
			else:
				ttsplay("I'm Sorry, but I could not toggle power on the tv right now")
		else:
			ttsplay("Sorry, but your tv is not set up in integrations.json")
	elif text == tvname.lower() + " remote":
		if tv:
			ttsplay("TV Remote activated")
			ttsplay("for help, say 'help'")
			tvremote()
		else:
			ttsplay("Sorry, but your tv is not set up in integrations.json")
	elif text == "search " + tvname.lower():
		if tv:
			ttsplay("What do you want to search?")
			query=input()
			if query:
				ttsplay("Searching for " + query + " on tv")
				requests.post("http://" + tvip + ":8060/keypress/Home")
				time.sleep(5)
				for _ in range(6):
					requests.post("http://" + tvip + ":8060/keypress/Down")
					time.sleep(1)
				requests.post("http://" + tvip + ":8060/keypress/Right")
				for char in query:
					requests.post("http://" + tvip + ":8060/keypress/Lit_" + str(char))
					time.sleep(1)
				requests.post("http://" + tvip + ":8060/keypress/Enter")
				ttsplay("Search complete")
			else:
				ttsplay("Could not understand what you said")
		else:
			ttsplay("Sorry, your tv is not set up in integrations.json")
	elif text == "start youtube on " + tvname.lower():
		if tv:
			ttsplay("Starting youtube on your tv")
			requests.post("http://" + tvip + ":8060/launch/837")
	elif text == "never mind":
		ttsplay("Sleep")
	elif text == "play music":
		ttsplay("playing song.mp3")
		pygame.mixer.music.unload()
		pygame.mixer.music.load("song.mp3", "mp3")
		pygame.mixer.music.play()
	else:
		ttsplay("I Could not understand that.")








tts = gTTS("Ready")
tts.save('temp.mp3')
pygame.mixer.music.load("temp.mp3", "mp3")
pygame.mixer.music.play()









def loop():
	global active
	global awake
	with sr.Microphone() as source:
    		print("Say something!")
    		audio = r.listen(source)

	try:
		sphinx=r.recognize_google(audio)
		print("Processing Input:  " + sphinx)
		if awake == True:
			if sphinx != False:
				active=True
				assist(sphinx)
				active=False
				awake=False
		elif sphinx == "hey Bob" or sphinx == "Bob" or sphinx == "okay Bob":
			ttsplay("Awake")
			awake=True
			print("Awake")
			individual_thread = threading.Thread(target=sleeptimer)
			individual_thread.start()
	except sr.UnknownValueError:
    		print("Google speech could not understand audio")
	except sr.RequestError as e:
    		print("Google speech error; {0}".format(e))
	loop()
loop()
