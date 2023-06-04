# Import Libraries
import RPi.GPIO as GPIO
import time

# Constants
SERVO_DUTY_FREQ = 50
SERVO_X_PIN_OUT = 11
SERVO_Y_PIN_OUT = 12
SERVO_X_RESTING_DUTY = 6
SERVO_Y_RESTING_DUTY = 6
SERVO_X_RANGE =  5
SERVO_Y_RANGE =  3
WAIT_TIME = 0.5

class Servos:
  """
  Controls two servo motors that change the vertical and horizontal 
  positioning of the camera and the spray tube.
  """

  def __init__(self):
    # Constants
    self.servoXDutyInc = 1
    self.servoYDutyInc = 2
    self.minServoXBounds = SERVO_X_RESTING_DUTY - SERVO_X_RANGE
    self.maxServoXBounds = SERVO_Y_RESTING_DUTY + SERVO_X_RANGE
    self.minServoYBounds = SERVO_Y_RESTING_DUTY - SERVO_Y_RANGE
    self.maxServoYBounds = SERVO_Y_RESTING_DUTY + SERVO_Y_RANGE

    # Set mode as BOARD
    GPIO.setmode(GPIO.BOARD) # move to generic area

    # Initialize servomotor instances
    GPIO.setup(SERVO_X_PIN_OUT, GPIO.OUT)
    GPIO.setup(SERVO_Y_PIN_OUT, GPIO.OUT)
    self.servoX = GPIO.PWM(SERVO_X_PIN_OUT, SERVO_DUTY_FREQ)
    self.servoY = GPIO.PWM(SERVO_Y_PIN_OUT, SERVO_DUTY_FREQ)

    # Start servos
    self.servoX.start(SERVO_X_RESTING_DUTY)
    self.servoY.start(SERVO_Y_RESTING_DUTY)
    time.sleep(WAIT_TIME)
    
    # Set servos to starting positions
    self.dutyX = SERVO_X_RESTING_DUTY
    self.dutyY = SERVO_Y_RESTING_DUTY

  def __del__(self):
    # Clean up
    self.servoX.stop()
    self.servoY.stop()
    GPIO.cleanup() # move to generic area

  def search_step(self):
    """
    Increments step in search path by one step.
    Search scans horizontally then repeats after adjusting to a different vertical height.
    """

    # Start rotating other way when 90 deg past resting angle
    if self.duty_x_at_bounds():
      self.servoXDutyInc *= -1

      # Reflect Y offset
      self.servoYDutyInc *= -1
      self.dutyY = SERVO_Y_RESTING_DUTY + self.servoYDutyInc
      print("Y = " + str(self.dutyY))
      self.servoY.ChangeDutyCycle(self.dutyY)
    else:
      # X increment
      self.dutyX += self.servoXDutyInc
      print("X = " + str(self.dutyX))
      self.servoX.ChangeDutyCycle(self.dutyX)
    
    time.sleep(WAIT_TIME)

  def duty_x_at_bounds(self):
    return self.dutyX in (self.minServoXBounds, self.minServoXBounds)

  def duty_y_at_bounds(self):
    return self.dutyY in (self.minServoYBounds, self.minServoYBounds)
  
  def increment_servos(self, servoXInc, servoYInc):
    if self.duty_x_at_bounds() or self.duty_y_at_bounds():
      return False
    
    self.dutyX = max(min(self.dutyX + servoXInc, self.maxServoXBounds), self.minServoXBounds)
    self.dutyY = max(min(self.dutyY + servoYInc, self.maxServoYBounds), self.minServoYBounds)

    self.servoX.ChangeDutyCycle(self.dutyX)
    self.servoY.ChangeDutyCycle(self.dutyY)

    return True
