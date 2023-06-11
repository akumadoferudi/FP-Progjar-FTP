# import socket
# import select
# import sys
# import time
# import os
# import threading
#
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
#
# class FTPClient(threading.Thread):
#     def __init__(self, host, port, user, password):
#         self.host = host
#         self.port = int(port)
#         self.user = user
#         self.password = password
#         self.buffer = 1024
#         self.address = (self.host, self.port)
#         self.serverSocket = None
#
#     def connect(self):
#         self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.serverSocket.connect((self.host, self.port))
#
#     def login(self):
#
#
#
# client = FTPClient('localhost', 8000, 'ferdi', '123')
#
#
#
# if __name__ == '__main__':


import socket
SERVER = "127.0.0.1"
PORT = 8080
USERNAME = 'ferdi'
PASSWORD = 'ferdi123'
running = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.send(bytes('LOGIN ' + USERNAME + '' + PASSWORD, 'UTF-8'))
while True:
  in_data =  client.recv(1024)
  print("From Server :" ,in_data.decode())
  out_data = input()
  client.sendall(bytes(out_data,'UTF-8'))
  if out_data=='bye':
  break
client.close()