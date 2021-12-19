import socket 
import time
import cv2
import base64
from PIL import Image
from io import BytesIO
import numpy as np

class VideoSender():
    HEADER_LENGTH = 10

    def __init__(self, IP='localhost', PORT=1234):
        self.IP = IP
        self.PORT = PORT
        print(f"Start connection")
        self.connect()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)
        self.client_socket.settimeout(10)
        print(f"Connected {self.IP}")
        
    def send(self, img):
        jpg_as_text = self.encode(img)

        ret = self.send_message(self.client_socket, str(jpg_as_text))
        
        msg = self.receive_message(self.client_socket)
        if msg is not False:
            return msg
        else:
            print(f"Disconnected {self.IP}")
            print(f"Reconnecting {self.IP}")
            self.connect()

        return None

    def read(self, msg):
        return self.decode(msg)

    def decode(self, data):
        img = Image.open(BytesIO(base64.b64decode(data['data'])))
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def encode(self, img):
        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(self.HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            data = client_socket.recv(message_length).decode("utf-8")      
            while len(data) < message_length:
                data += client_socket.recv(message_length - len(data)).decode("utf-8")
                
            return {"header": message_header, "data": data}

        except:
            return False

    def send_message(self, client_socket, message):
        try:
            if not len(message):
                return False
            message = message.encode("utf-8")
            message_header = f'{len(message):<{self.HEADER_LENGTH}}'.encode('utf-8')
            client_socket.sendall(message_header + message)
            
        except:
            return False
        return True


'''
if __name__ == '__main__':
    sender = VideoSender()
    cap = cv2.VideoCapture('test.wmv')

    while True:
        _, img = cap.read()
        cv2.imshow('as', img)
        msg = sender.send(img)
        if  cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
'''