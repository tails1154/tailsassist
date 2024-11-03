print("Loading tailsAssist...")
import speech_recognition as sr
import pygame
from gtts import gTTS
import threading
import time
pygame.init()
pygame.mixer.init()
version="0.1"
awake=False
active=False
print("Loaded modules!")
print("Starting...")
r = sr.Recognizer()






def sleeptimer():
	global active
	global awake
	print(active)
	print(awake)
	time.sleep(10)
	if active == False:
		pygame.mixer.music.unload()
		pygame.mixer.music.load("audio/sleep.mp3", "mp3")
		pygame.mixer.music.play()
		print("Sleep")
		awake = False







def ttsplay(text):
	from gtts import gTTS
	tts = gTTS(text)
	tts.save('temp.mp3')
	pygame.mixer.music.unload()
	pygame.mixer.music.load("temp.mp3", "mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		print("Buzy")









def input():
	print("Wait for input")
	try:
		return r.recognize_google(audio)
	except sr.UnknownValueError:
		print("Google speech could not understand audio")
	except sr.RequestError as e:
		print("Google speech error; {0}".format(e))







def assist(text):
	if text == "addition":
		ttsplay("Enter number 1 to add");
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)

		pygame.mixer.music.unload()
		pygame.mixer.music.load("audio/wakeup.mp3", "mp3")
		pygame.mixer.music.play()









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
		elif sphinx == "hey Bob":
			awake=True
			pygame.mixer.music.unload()
			pygame.mixer.music.load("audio/wakeup.mp3", "mp3")
			pygame.mixer.music.play()
			print("Awake")
			individual_thread = threading.Thread(target=sleeptimer)
			individual_thread.start()
	except sr.UnknownValueError:
    		print("Google speech could not understand audio")
	except sr.RequestError as e:
    		print("Google speech error; {0}".format(e))
	loop()
loop()
