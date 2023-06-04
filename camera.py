# Import Libraries
import cv2

class Camera:
  def __init__(self):
    self.camera = cv2.VideoCapture(0)

    # Skip some frames for startup
    for _ in range(30):
      temp1, temp2 = self.camera.read()

  def read_and_show_img(self):
    self.valid, self.image = self.camera.read()
    cv2.imshow('Camera Feed', self.image)
    
  def query_expression():

    return False