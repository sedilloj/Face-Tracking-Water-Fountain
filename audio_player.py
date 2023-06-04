import pygame
import random

fileDir = 'resources/audio/'
files = [
  fileDir + 'ahh.mp3',
  fileDir + 'bus.mp3',
  fileDir + 'omg.mp3',
  fileDir + 'tagalog.mp3'
]

def PlayAudio():
  pygame.mixer.init()
  pygame.mixer.music.load(files[random.randint(0, len(files) - 1)])
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
    continue

PlayAudio()