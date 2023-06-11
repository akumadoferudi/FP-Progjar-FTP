# GROUP 12 COMPUTER NETWORKING D

import socket

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
  if out_data == 'QUIT':
    print('200, CONNECTION CLOSED!')
    break

  client.send(bytes(out_data, 'UTF-8'))

client.close()
