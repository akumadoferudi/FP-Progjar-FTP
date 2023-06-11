import socket

SERVER = '10.8.108.142'
PORT = 8080
USERNAME = 'ferdi'
PASSWORD = 'ferdi123'
# running = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
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
