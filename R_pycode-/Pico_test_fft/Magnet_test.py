import numpy as np
from time import sleep
from sockets import ZMQReqSocket, TcpReqSocket
from magnet_IPS_class import *
from magnet_control import *
import zmq



mg = magnet_IPS ('serial','COM8')
mc = magnet_control(mg)
print (mg.getID())