# Import Libraries
import RPi.GPIO as GPIO
import pygame
import random
import time

# Audio File Paths
FILE_DIR = 'resources/audio/'
FILES = [
  FILE_DIR + 'ahh.mp3',
  FILE_DIR + 'bus.mp3',
  FILE_DIR + 'omg.mp3',
  FILE_DIR + 'tagalog.mp3'
]

# Other Constants
PUMP_PIN_OUT = 16
SETUP_TIME = 1.0
MAX_SPRAY_TIME = 6
SPRAY_TOGGLE_TIMES = [
  [0, 1],
  [0, 1],
  [0, 1],
  [0, 1]
]

class Sprayer:
  """Controls the diaphagm pump and the audio speakers."""

  def __init__(self):
    pygame.mixer.init()
    GPIO.setup(PUMP_PIN_OUT, GPIO.OUT)

    # Spray for a limited time to guarantee water is at the spray tip
    GPIO.output(PUMP_PIN_OUT, GPIO.HIGH)
    timeStart = time.time()

    while time.time() - timeStart < SETUP_TIME:
      continue
    
    # Turn off spray once time has passed
    self.sprayState = GPIO.LOW
    GPIO.output(PUMP_PIN_OUT, self.sprayState)

  def __exit__(self):
    GPIO.output(PUMP_PIN_OUT, GPIO.LOW)

  def spray(self):
    """
    Sprays while playing a random audio file. 
    The spray pattern will depend on the audio file selected.
    """

    # Select random audio file
    audioIdx = random.randint(0, len(FILES) - 1)
    maxSprayToggleIdx = len(SPRAY_TOGGLE_TIMES[audioIdx]) - 1
    pygame.mixer.music.load(FILES[audioIdx])
    pygame.mixer.music.play()

    self.sprayTimeIdx = -1
    timeStart = time.time()

    # Set spray pattern to match the audio playback
    while pygame.mixer.music.get_busy() == True:
      if self.sprayTimeIdx < maxSprayToggleIdx:
        timePlayback = time.time() - timeStart

        # Toggle the diaphagm pump on/off
        if timePlayback > SPRAY_TOGGLE_TIMES[audioIdx][self.sprayTimeIdx + 1]:
          self.sprayTimeIdx += 1
          self.sprayState = int(not self.sprayState)
          GPIO.output(PUMP_PIN_OUT, self.sprayState)

      continue
    
    # Continue spraying for given duration
    while time.time() - timeStart < MAX_SPRAY_TIME:
      continue
    
    # Turn off the spray once the set time has passed
    self.sprayState = GPIO.LOW
    GPIO.output(PUMP_PIN_OUT, self.sprayState)

