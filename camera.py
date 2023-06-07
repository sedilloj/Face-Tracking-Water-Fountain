# Import Libraries
import cv2

tracker_ahegao = cv2.CascadeClassifier('resources/models/haarcascade_ahegao_25stages.xml')
tracker_mouth = cv2.CascadeClassifier('resources/models/haarcascade_mcs_mouth.xml')

class Camera:
  def __init__(self):
    self.cascade_ahegao = cv2.CascadeClassifier('resources/models/100x100_15/cascade.xml')
    self.camera = cv2.VideoCapture(0)

    # Skip some frames for startup
    for _ in range(30):
      temp1, temp2 = self.camera.read()

  def read_and_show_img(self):
    self.valid, self.image = self.camera.read()
    cv2.imshow('Camera Feed', self.image)
    
  def query_expression(self):
    self.valid, self.image = self.camera.read()
    gray_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)    

    objects_ahegao = tracker_ahegao.detectMultiScale(gray_img, 1.05, 1) # ahegao
    objects_mouth = tracker_mouth.detectMultiScale(gray_img, 1.55, 4) # mouth

    # for (x, y, w, h) in objects_mouth:
    #   cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #   cv2.putText(img, 'smile', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # for (x, y, w, h) in objects_ahegao:
    #   cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #   cv2.putText(img, 'ahegao', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    b_intersect = False
    max_area_ratio = 0
    intersect_final = ()

    for ahegao in objects_ahegao:
      (x1_ahegao, y1_ahegao, w_ahegao, h_ahegao) = ahegao
      x2_ahegao = x1_ahegao + w_ahegao
      y2_ahegao = y1_ahegao + h_ahegao
      area_ahegao = w_ahegao * h_ahegao
      
      for mouth in objects_mouth:
        (x1_mouth, y1_mouth, w_mouth, h_mouth) = mouth
        x2_mouth = x1_mouth + w_mouth
        y2_mouth = y1_mouth + h_mouth

        x1_intersect = max(x1_ahegao, x1_mouth)
        x2_intersect = min(x2_ahegao, x2_mouth)
        y1_intersect = max(y1_ahegao, y1_mouth)
        y2_intersect = min(y2_ahegao, y2_mouth)

        w_intersect = x2_intersect - x1_intersect
        h_intersect = y2_intersect - y1_intersect

        if (w_intersect > 0 and h_intersect > 0):
          b_intersect = True
          area_intersect = w_intersect * h_intersect

          if area_intersect / area_ahegao > max_area_ratio:
            ahegao_final = (x1_ahegao, y1_ahegao, x2_ahegao, y2_ahegao)
            mouth_final = (x1_mouth, y1_mouth, x2_mouth, y2_mouth)
            intersect_final = (x1_intersect, y1_intersect, x2_intersect, y2_intersect)
      
    if b_intersect:
      cv2.rectangle(self.image, (ahegao_final[0], ahegao_final[1]), (ahegao_final[2], ahegao_final[3]), (0, 0, 255), 2)
      cv2.putText(self.image, 'ahegao', (ahegao_final[0], ahegao_final[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
      cv2.rectangle(self.image, (mouth_final[0], mouth_final[1]), (mouth_final[2], mouth_final[3]), (0, 255, 255), 2)
      cv2.putText(self.image, 'mouth', (mouth_final[0], mouth_final[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
      cv2.rectangle(self.image, (intersect_final[0], intersect_final[1]), (intersect_final[2], intersect_final[3]), (0, 255, 0), 2)
      cv2.putText(self.image, 'intersect', (intersect_final[0], intersect_final[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return intersect_final