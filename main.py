#!/usr/bin/env python
from socket import *
import time

__author__ = "Hieu Nguyen"
__copyright__ = "Copyright 2017, Hieu Nguyen"
__version__ = "1.0"

def display_help():
    print("")

class multicast_connection:
    def __init__(self, ip_address, port, buffer_size=1024):
        self.ip_address = ip_address
        self.port = port
        self.buffer_size = buffer_size
        self.connected = False

        self.connect_socket()

    def connect_socket(self):
        # create UDP socket
        self.socket = socket(AF_INET,
                             SOCK_DGRAM)

        # connect to source address and port
        # self.socket.connect((self.ip_address, self.port))
        self.socket.connect((self.ip_address, self.port))

        self.connected = True

    def _run(self):
        while self.connected:
            try:
                #data = self.socket.recvfrom(self.buffer_size)
                data = self.socket.recv(self.buffer_size)
                print(data)
            except:
                pass



## Main
udp_ip = "127.0.0.1"
udp_port = 5005

multicast_ip = "224.2.10.100"
multicast_port = 30000

connection = multicast_connection(udp_ip, udp_port)

connection._run()