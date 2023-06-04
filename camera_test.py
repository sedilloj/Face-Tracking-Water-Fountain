# Import Libraries
import cv2

def run():
  camera = cv2.VideoCapture(0)

  # Skip some frames for startup
  for _ in range(30):
    temp1, temp2 = camera.read()

  while True:
    valid , image = camera.read()
    cv2.imshow('frame', image)

    imageGrayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  camera.release()
  cv2.destroyAllWindows()

run()