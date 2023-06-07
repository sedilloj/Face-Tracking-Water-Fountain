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
    # Always running
    while True:
      rect_target = camera.query_expression()

      if not len(rect_target):
        # Search if matching face undetected
        servos.search_step()
      else:
        # Aim to face if face is detected
        diffX = x_middle # adjust this code later
        
  finally:
    # Clean up
    servos.servoX.stop()
    servos.servoY.stop()
    GPIO.cleanup()

  # set servos to refine position to aim towards the face
  
