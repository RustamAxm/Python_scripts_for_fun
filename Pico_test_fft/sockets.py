import socket
import time
import traceback

import zmq


class ZMQReqSocket(object):
    context = None
    def __init__(self,address,timeout):
        self.address = address
        if self.context is None:
            self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(*self.address))
    def ask(self,msg):
        try:
            if type(msg)==str:
                msg = msg.encode()
            self.socket.send(msg)
            ret = self.socket.recv()
            return ret
        except:
            traceback.print_exc()


class TcpReqSocket(object):
    context = None
    def __init__(self,address,timeout):
        self.address = address
        self.address_fmt = "{}:{}".format(*self.address)
        # if self.context is None:
        #     self.context = zmq.Context()
        # self.socket = self.context.socket(zmq.REQ)
        # self.socket.connect(self.address)
        self.socket = socket.create_connection(address,timeout = timeout)
    def ask(self,msg):
        try:
            print("{} {}<< {}".format(time.strftime("%H:%M:%S",time.localtime()), self.address_fmt,msg))
            if type(msg)==str:
                msg = msg.encode()
            self.socket.send(msg)
            ret = self.socket.recv(1024)
            print("         {}>>{}".format(self.address_fmt,ret))
            return ret
        except:
            traceback.print_exc()