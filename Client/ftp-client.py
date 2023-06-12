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
client.send(bytes('LOGIN@' + USERNAME + '@' + PASSWORD, 'UTF-8'))

while True:
  in_data =  client.recv(1024).decode('UTF-8')
  print("From Server : ", in_data)
  out_data = input('>> ')
  command = out_data.split('@')

  if command[0] == 'QUIT':
    print('200, CONNECTION CLOSED!')
    break

  elif command[0] == 'STOR':
    if len(command) == 2:
      file = command[1]
      filepath = os.path.join(os.getcwd(), file)
      print(filepath)

      if not os.path.exists(filepath):
        print('500, FILE NOT FOUND!')

      else:
        # client.send(bytes('STOR ' + file, 'UTF-8'))
        # local_file = open(file, 'rb')
        # chunk = local_file.read()
        # client.send(chunk)
        # print(chunk.decode())
        # print("[SEND] buffer or data!")

        # with open(filepath, 'rb') as f:
        #   chunk = f.read()

        f = open(filepath, 'rb')
        chunk = f.read()

        print(chunk.decode())
        print("[SEND] buffer or data!")
        command_file = 'STOR@' + file + '@' + chunk.decode()
        print(command_file)
        client.send(command_file.encode('UTF-8'))
          # while chunk is not None:
          #   client.send(chunk)
          #   print("[SEND] buffer or data!")
          #   time.sleep(1)


        # while chunk != "":
        #   chunk = local_file.read(1024)
        #   client.send(chunk)
        #   print(chunk.decode())
        #   print("[SEND] buffer or data!")
        #   time.sleep(0.5)

        print('200, FILE UPLOADED')
        # client.send(bytes('200, FILE UPLOADED!', 'UTF-8'))

  client.send(bytes(out_data, 'UTF-8'))

client.close()
