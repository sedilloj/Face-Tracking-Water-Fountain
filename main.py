# Import Libraries
import RPi.GPIO as GPIO

# Import files
from servo import Servos
from sprayer import Sprayer
from camera import Camera

x_middle = 320
y_middle = 240

if __name__ == '__main__':
  # Set mode as BOARD
  GPIO.setmode(GPIO.BOARD)

  # Initialize all individual components
  sprayer = Sprayer()
  servos = Servos()
  camera = Camera()

  try:
    # always running
    while True:
      # query for face here

      # search if matching face undetected
      while not face_query:
        servos.search_step()

      # aim to face if face is detected
      while face_query:
        diffX = x_middle - image
        
  finally:
    # Clean up
    servos.servoX.stop()
    servos.servoY.stop()
    GPIO.cleanup()

  # set servos to refine position to aim towards the face
  
