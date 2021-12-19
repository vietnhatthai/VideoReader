import VideoSender as VS
import cv2

sender = VS.VideoSender()
cap = cv2.VideoCapture('test.wmv')

while True:
    _, img = cap.read()
    cv2.imshow('as', img)
    msg = sender.send(img)
    if  cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()