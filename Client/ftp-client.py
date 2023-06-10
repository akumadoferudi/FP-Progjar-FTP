import socket
import select
import sys
import time
import os
import threading

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class ftpClient(threading.Thread):
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.buffer = 1024
        self.address = (self.host, self.port)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == '__main__':
