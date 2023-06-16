# Import Libraries
import RPi.GPIO as GPIO
import time

# Constants
SERVO_DUTY_FREQ = 50
SERVO_X_PIN_OUT = 12
SERVO_Y1_PIN_OUT = 11
SERVO_Y2_PIN_OUT = 13
SERVO_X_RESTING_DUTY = 6
SERVO_Y_RESTING_DUTY = 5
SERVO_X_RANGE =  1.5
SERVO_Y_RANGE =  1
WAIT_TIME = 0.5

class Servos:
  """
  Controls two servo motors that change the vertical and horizontal 
  positioning of the camera and the spray tube.
  """

  def __init__(self):
    # Constants
    self.servoXDutyInc = 0.5
    self.servoYDutyInc = 1
    self.servoXBounds = (SERVO_X_RESTING_DUTY - SERVO_X_RANGE, SERVO_X_RESTING_DUTY + SERVO_X_RANGE)
    self.servoYBounds = (SERVO_Y_RESTING_DUTY - SERVO_Y_RANGE, SERVO_Y_RESTING_DUTY + SERVO_Y_RANGE)

    # Initialize servomotor instances
    GPIO.setup(SERVO_X_PIN_OUT, GPIO.OUT)
    GPIO.setup(SERVO_Y1_PIN_OUT, GPIO.OUT)
    GPIO.setup(SERVO_Y2_PIN_OUT, GPIO.OUT)
    self.servoX = GPIO.PWM(SERVO_X_PIN_OUT, SERVO_DUTY_FREQ)
    self.servoY1 = GPIO.PWM(SERVO_Y1_PIN_OUT, SERVO_DUTY_FREQ)
    self.servoY2 = GPIO.PWM(SERVO_Y2_PIN_OUT, SERVO_DUTY_FREQ)

    # Start servos
    self.servoX.start(SERVO_X_RESTING_DUTY)
    self.servoY1.start(SERVO_Y_RESTING_DUTY)
    self.servoY2.start(SERVO_Y_RESTING_DUTY)
    time.sleep(WAIT_TIME)
    
    # Set servos to starting positions
    self.dutyX = SERVO_X_RESTING_DUTY
    self.dutyY1 = SERVO_Y_RESTING_DUTY
    self.dutyY2 = SERVO_Y_RESTING_DUTY

  def __del__(self):
    # Clean up
    self.servoX.stop()
    self.servoY1.stop()
    self.servoY2.stop()
     
  def search_step(self):
    """
    Increments step in search path by one step.
    Search scans horizontally then repeats after adjusting to a different vertical height.
    """

    # Start rotating other way when 90 deg past resting angle
    if self.duty_x_at_bounds():
      self.servoXDutyInc *= -1
      
      # Y increment
      self.search_step_Y()

    # X increment
    self.search_step_X() # this will unfortunately skip checking the corners
      
    self.print_positions()
    time.sleep(WAIT_TIME)

  def search_step_X(self):
    self.dutyX += self.servoXDutyInc
    self.servoX.ChangeDutyCycle(self.dutyX)

  def search_step_Y(self):
    if self.dutyY1 != SERVO_Y_RESTING_DUTY or self.dutyY2 != SERVO_Y_RESTING_DUTY:
      self.dutyY1 = SERVO_Y_RESTING_DUTY
      self.dutyY2 = SERVO_Y_RESTING_DUTY
    else:
      self.dutyY1 = SERVO_Y_RESTING_DUTY + self.servoYDutyInc
      self.dutyY2 = SERVO_Y_RESTING_DUTY - self.servoYDutyInc

    self.servoY1.ChangeDutyCycle(self.dutyY1)
    self.servoY2.ChangeDutyCycle(self.dutyY2)

  def print_positions(self):
    print("X = " + str(self.dutyX) + " Y1 = " + str(self.dutyY1) + " Y2 = " + str(self.dutyY2))

  def duty_x_at_bounds(self):
    return self.dutyX in self.servoXBounds

  def duty_y1_at_bounds(self):
    return self.dutyY1 in self.servoYBounds
  
  def duty_y2_at_bounds(self):
    return self.dutyY2 in self.servoYBounds
  
  def increment_servos(self, servoXInc, servoYInc):
    if self.duty_x_at_bounds() or self.duty_y_at_bounds():
      return False
    
    self.dutyX = max(min(self.dutyX + servoXInc, self.maxServoXBounds), self.minServoXBounds)
    self.dutyY = max(min(self.dutyY + servoYInc, self.maxServoYBounds), self.minServoYBounds)

    self.servoX.ChangeDutyCycle(self.dutyX)
    self.servoY.ChangeDutyCycle(self.dutyY)

    return True
