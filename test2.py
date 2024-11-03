import pygame
from gtts import gTTS
tts = gTTS('hello')
tts.save('temp.mp3')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("temp.mp3", "mp3")
pygame.mixer.music.play()

while True:
	print("e")
