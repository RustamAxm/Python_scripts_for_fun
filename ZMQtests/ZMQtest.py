import zmq
import zmq
import random
import sys
import time

port = "6000"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = random.choice(['IPS120', 'RS830'])
    messagedata = random.randrange(1,215) - 80
    print("%s %d" % (topic, messagedata))
    socket.send_pyobj("%s %d" % (topic, messagedata))
    time.sleep(1)