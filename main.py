# Import Libraries
import RPi.GPIO as GPIO
import time

# Import files
from servo import Servos
from sprayer import Sprayer
from camera import Camera

X_CENTER = 320
Y_CENTER = 240
X_TOLERANCE = 50
Y_TOLERANCE = 25
MAX_WAITS = 4

def calculate_rect_dist_to_center(coordRect):
  coordRectCenter = ((coordRect[0] + coordRect[2]) / 2, (coordRect[1] + coordRect[3]) / 2)
  return X_CENTER - coordRectCenter[0], Y_CENTER - coordRectCenter[1]

def calculate_servoX_adjustment(diffX):
  # This function will never be called if the center difference is between (-X_TOLERANCE, X_TOLERANCE)
  if diffX < -300:
    return -1
  elif diffX < -200:
    return -0.75
  elif diffX < -100:
    return -0.5
  elif diffX < -X_TOLERANCE:
    return -0.25
  elif diffX < X_TOLERANCE:
    return 0
  elif diffX < 100:
    return 0.25
  elif diffX < 200:
    return 0.5
  elif diffX < 300:
    return 0.75
  else:
    return 1
  
def calculate_servoY_adjustment(diffY):
  # This function will never be called if the center difference is between (-Y_TOLERANCE, Y_TOLERANCE)
  if diffY < -100:
    return -0.75
  elif diffY < -50:
    return -0.5
  elif diffY < -Y_TOLERANCE:
    return -0.25
  elif diffY < Y_TOLERANCE:
    return 0
  elif diffY < 50:
    return 0.25
  elif diffY < 100:
    return 0.5
  else:
    return 0.75

if __name__ == '__main__':
  # Set mode as BOARD
  GPIO.setmode(GPIO.BOARD)

  # Initialize all individual components
  sprayer = Sprayer()
  servos = Servos()
  camera = Camera()

  try:
    waitCounter = 0

    # Always running
    while True:
      if waitCounter == MAX_WAITS:
        waitCounter = 0
        # reset the servos to starting position

      rectTarget = camera.query_expression()

      if not len(rectTarget):
        if waitCounter:
          # Wait to re-detect face if adjusting made it undetectable
          waitCounter += 1
          time.sleep(1.0)
          continue

        else:
          # Search if matching face undetected
          servos.search_step()

      else:
        # Aim to face if face is detected
        distXToCenter, distYToCenter = calculate_rect_dist_to_center(rectTarget)

        adjustX = calculate_servoX_adjustment(distXToCenter)
        adjustY = calculate_servoY_adjustment(distYToCenter)

        if not adjustX and not adjustY:
          # spray
          print('spraying')
        else:
          print('adjust')

          
        
  finally:
    # Clean up
    GPIO.cleanup()
  
