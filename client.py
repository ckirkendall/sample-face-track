#!venv/bin/python

import time
import numpy as np
import cv2

from camera.usb import USBCam

try:
  from camera.rpi import RPICam
except:
    pass

import config as settings

dpath = "haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier(dpath)

scale_factor = 0.25

if settings.CAMERA == 'USB':
  cam = USBCam(settings.CAM_RESOLUTION)
  
if settings.CAMERA == 'RPI':
  cam = RPICam(settings.CAM_RESOLUTION)


def scale_rect(rect):
  x, y, x2, y2 = rect
  tmp = (int(x / scale_factor),
         int(y / scale_factor),
         int(x2 / scale_factor),
         int(y2 / scale_factor))
  return tmp


def scale_frame(frame):
  return cv2.resize(frame,
                    (0,0),
                    fx=scale_factor,
                    fy=scale_factor,
                    interpolation = cv2.INTER_AREA)


def cv2_find_face(frame, attempt = 0):
  start = time.clock()
  detected = list(face_cascade.detectMultiScale(frame,
                                                scaleFactor=(2.01 - (attempt * 0.25)),
                                                minNeighbors=3,
                                                minSize=(25, 25),
                                                flags=cv2.CASCADE_SCALE_IMAGE))
  if len(detected) > 0:
    detected.sort(key=lambda a: (-1.0 * a[-1] * a[-2]))
    y, x, h, w = detected[0]
    rect =  (x.item(), (y + h).item(), (x + w).item(), y.item())
    print("cv2 found a face: ",
          "attempt=", attempt,
          "in", (time.clock() - start) * 1000, "ms")
    return rect
  elif attempt < 3:
    print("cv2 did not find a face:",
          "attempt=", attempt,
          "in", (time.clock() - start) * 1000, "ms")
    return cv2_find_face(frame, attempt + 1)
  return

def process_frame():
  frame = cam.get_frame()
  scaled_frame = scale_frame(frame)
  rect = cv2_find_face(scaled_frame)
  if rect is not None:
    x1, y1, x2, y2 = scale_rect(rect)
    cv2.rectangle(frame, (y1, x1), (y2, x2), (255,0,0), 2)
  cv2.imshow('',frame)
  

if __name__ == "__main__":
  while True:
    process_frame()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
