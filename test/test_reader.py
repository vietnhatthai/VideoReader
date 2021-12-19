import VideoReader as VR
import cv2

cap = VR.VideoReader()
while cap.isOpened():
    _, img = cap.read()
    if img is None:
        continue
    cv2.imshow('', img)
    cv2.waitKey(1)