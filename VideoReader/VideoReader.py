import socket
import cv2
from PIL import Image
from io import BytesIO
import base64
import numpy as np

class VideoReader():
    HEADER_LENGTH = 10

    def __init__(self, IP='', PORT=1234, auto_feedback=True):
        self.IP = IP
        self.PORT = PORT
        self.auto_feedback = auto_feedback
        print(f"Start connection")
        self.connect()
        
    def connect(self):
        self.sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sever_socket.bind((self.IP, self.PORT))
        self.sever_socket.listen()

        self.clientsocket, self.address = self.sever_socket.accept()
        self.clientsocket.settimeout(1)
        print(f"Connection from {self.address} has been established.")

    def read(self):
        data = False
        while data is False:
            data = self.receive_message(self.clientsocket)
            if data is not False:
                try:
                    data = eval(data['data'])
                    image = self.decode(data)
                    if self.auto_feedback:
                        self.send_message(self.clientsocket, str('OK'))
                    return True, image
                except:
                    if self.auto_feedback:
                        self.send_message(self.clientsocket, str('OK'))
                    return False, None
            else:
                print(f"Disconnected {self.address}")
                print(f"Reconnecting {self.address}")
                self.connect()
                print(f"Connected {self.address}")
        return False, None

    def send_img(self, img):
        jpg_as_text = self.encode(img)
        return self.send(str(jpg_as_text))

    def dataSend(self, actionName, trainPercent, img):
        data = f'{actionName},{trainPercent},{self.encode(img)}'
        ret = self.send_message(self.clientsocket, data)
        return ret

    def send(self, msg):
        ret = self.send_message(self.clientsocket, msg)
        return ret
        
    def decode(self, data):
        img = Image.open(BytesIO(base64.b64decode(data['data'])))
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img    

    def encode(self, img):
        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text

    def release(self):
        self.clientsocket.close()

    def isOpened(self):
        return True

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

    cap = VideoReader(auto_feedback=True)
    while cap.isOpened():
        _, img = cap.read()
        if img is None:
            continue
        cv2.imshow('', img)
        cv2.waitKey(1)
'''