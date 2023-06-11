# GROUP 12 COMPUTER NETWORKING D

import socket
import os
import time

SERVER = '127.0.0.1'
PORT = 8080
USERNAME = 'ferdi'
PASSWORD = 'ferdi123'

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# login onto server
client.send(bytes('LOGIN ' + USERNAME + '' + PASSWORD, 'UTF-8'))

while True:
  in_data =  client.recv(1024)
  print("From Server : ", in_data.decode())
  out_data = input('>> ')
  command = out_data.split()

  if command[0] == 'QUIT':
    print('200, CONNECTION CLOSED!')
    break

  elif command[0] == 'STOR':
    if len(command) == 2:
      file = command[1]
      filepath = os.getcwd() + "\\" + file

      if not os.path.exists(filepath):
        print('500, FILE NOT FOUND!')
      else:
        client.send(bytes('STOR ' + file, 'UTF-8'))
        with open(file, 'rb') as chunk:
          while True:
            data = chunk.read()

            if not chunk:
              break

            client.send(data)
            print(data)
            print("[SEND] buffer or data!")
        print('200, FILE UPLOADED')

  else:
    client.send(bytes(out_data, 'UTF-8'))

client.close()
