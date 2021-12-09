import socket, time
class DJI_simple:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = ('192.168.10.1', 8889)
        self.sock.bind(self.locaddr)

        self.sock.sendto('command'.encode(encoding="utf-8"), self.tello_address)
        print(self.sock.recv(4096).decode(encoding="utf-8"))

    def telemetry(self):
        self.sock.sendto('speed?'.encode(encoding="utf-8"), self.tello_address)
        speed = self.sock.recv(4096).decode(encoding="utf-8").strip()

        self.sock.sendto('battery?'.encode(encoding="utf-8"), self.tello_address)
        battery = self.sock.recv(4096).decode(encoding="utf-8").strip()

        self.sock.sendto('time?'.encode(encoding="utf-8"), self.tello_address)
        time_of_flight = self.sock.recv(4096).decode(encoding="utf-8").strip()
        return speed, battery, time_of_flight

    def rotate(self, angle):
        # Rotate clockwise 360
        self.sock.sendto('cw {}'.format(angle).encode(encoding="utf-8"), self.tello_address)
        return self.sock.recv(4096).decode(encoding="utf-8")

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




if __name__ == "__main__":
    dji = DJI_simple()
    print(dji.takeoff())
    dji.rotate(360)
    dji.forward(30)
    dji.backward(40)
    print(dji.land())
    print("Test_success")






