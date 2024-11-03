import pyttsx3
engine = pyttsx3.init(driverName="espeak")
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[11].id) #English
engine.say("hello world")
engine.runAndWait()
