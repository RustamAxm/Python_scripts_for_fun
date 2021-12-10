import socket, time
import cv2
import threading

class DJI_simple:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)

        self.stream_state = False
        self.last_frame = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = ('192.168.10.1', 8889)
        self.sock.bind(self.locaddr)

        self.sock.sendto('command'.encode(encoding="utf-8"), self.tello_address)
        #print(self.sock.recv(4096).decode(encoding="utf-8"))

    def telemetry(self):
        self.sock.sendto('speed?'.encode(encoding="utf-8"), self.tello_address)
        speed = self.sock.recv(4096).decode(encoding="utf-8").strip()

        self.sock.sendto('battery?'.encode(encoding="utf-8"), self.tello_address)
        battery = self.sock.recv(4096).decode(encoding="utf-8").strip()

        self.sock.sendto('time?'.encode(encoding="utf-8"), self.tello_address)
        time_of_flight = self.sock.recv(4096).decode(encoding="utf-8").strip()
        return speed, battery, time_of_flight

    def rotate(self, angle):
        # Rotate clockwise angle
        self.sock.sendto('cw {}'.format(angle).encode(encoding="utf-8"), self.tello_address)
        #return self.sock.recv(4096).decode(encoding="utf-8")

    def takeoff(self):
        # Takeoff
        self.sock.sendto('takeoff'.encode(encoding="utf-8"), self.tello_address)
        time.sleep(2)
        return self.sock.recv(4096).decode(encoding="utf-8")

    def land(self):
        # Land
        self.sock.sendto('land'.encode(encoding="utf-8"), self.tello_address)
        time.sleep(2)
        return self.sock.recv(4096).decode(encoding="utf-8")

    def forward(self, x):
        self.sock.sendto('forward {}'.format(x).encode(encoding="utf-8"), self.tello_address)
        return self.sock.recv(4096).decode(encoding="utf-8")

    def backward(self, x):
        self.sock.sendto('back {}'.format(x).encode(encoding="utf-8"), self.tello_address)
        return self.sock.recv(4096).decode(encoding="utf-8")

    def _video_cupture(self):
        # Creating stream capture object
        cap = cv2.VideoCapture('udp:/0.0.0.0:11111')
        # Runs while 'stream_state' is True
        while self.stream_state:
            ret, self.last_frame = cap.read()
            cv2.imshow('DJI Tello', self.last_frame)

            # Video Stream is closed if escape key is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def streamon(self):
        self.sock.sendto('streamon'.encode(encoding="utf-8"), self.tello_address)
        self.stream_state = True
        self.video_thread = threading.Thread(target=self._video_cupture)
        self.video_thread.daemon = True
        self.video_thread.start()
        #return self.sock.recv(4096).decode(encoding="utf-8")

    def streamoff(self):
        self.stream_state = False
        self.sock.sendto('streamoff'.encode(encoding="utf-8"), self.tello_address)
        return self.sock.recv(4096).decode(encoding="utf-8")




if __name__ == "__main__":
    dji = DJI_simple()
    dji.streamon()
    time.sleep(5)
    dji.streamoff()

    print("Test_success")






