# GROUP 12 COMPUTER NETWORKING D

import socket
import select
import sys
import os
import threading
import time

# sys.path.append('../Client')

BUFFER = 1024

class FTPServer:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.address = (self.host, self.port)
        self.buffer = 1024
        self.serverSocket = None
        self.threads = []

    def bind(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind(self.address)
            self.serverSocket.listen(5)
            print('bind successfully!')
        except:
            print('failed to bind!')

    def run(self):
        self.bind()
        inputSocket = [self.serverSocket]

        try:
            while True:
                readList, writeList, exceptionList = select.select(inputSocket, [], [])

                for sock in readList:
                    if sock == self.serverSocket:
                        client_socket, client_address = self.serverSocket.accept()
                        cThread = ClientThread(client_socket, client_address, self.user, self.password)
                        cThread.start()
                        self.threads.append(cThread)
                        inputSocket.append(client_socket)
                        print('connected to client: ', client_address)

                    else:
                        sock.close()
                        inputSocket.remove(sock)
                        # data = sock.recv(1024)
                        # print(sock.getpeername(), data)

        except KeyboardInterrupt:
            self.serverSocket.close()
            for cThread in self.threads:
                cThread.join()

            sys.exit(0)

class ClientThread(threading.Thread):
    def __init__(self, client, address, user, password):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.buffer = 1024
        self.user = user
        self.password = password

    def run(self):
        auth = self.client.recv(self.buffer).decode('UTF-8')
        login_credentials = 'LOGIN ' + self.user + '' + self.password

        if auth == login_credentials:
            self.client.send(bytes('201, LOGIN SUCCESS!', 'UTF-8'))
            running = 1
        else:
            self.client.send(bytes('500, LOGIN FAILED!', 'UTF-8'))
            self.client.close()
            running = 0

        while running:
            data = self.client.recv(self.buffer)
            print('received: ', self.address, data.decode())
            if data:
                # list all valid command
                ftp_command = [
                    'LIST', 'PWD',
                    'CWD', 'MKD',
                    'RMD', 'STOR',
                    'RETR', 'RNTO',
                    'DELE', 'HELP'
                ]
                # make command per args
                command = data.decode().split()

                # 1. list all files and directories (fixed)
                if command[0] == ftp_command[0]:
                    list = os.listdir()
                    format_list = []

                    # check if path is a directory or file
                    for member in list:
                        if os.path.isdir(member):
                            # print(member)
                            member += '/'
                            format_list.append(member)
                        else:
                            format_list.append(member)
                            continue

                    data = str(format_list)
                    self.client.send(bytes("200, SUCCESS\n list dir: " + data, 'UTF-8'))
                    print('200, SUCCESS!')

                # 2. get current directory (fixed)
                elif command[0] == ftp_command[1]:
                    pwd = os.getcwd()
                    self.client.send(bytes("200, SUCCESS!\ncurrent directory: " + pwd, 'UTF-8'))
                    print('200, SUCCESS!')


                # 3. change directory (fixed)
                elif command[0] == ftp_command[2]:
                    if len(command) == 2:
                        path = command[1]
                        currentdir = os.getcwd()
                        navigation_dir = currentdir + "\\" + path
                        if os.path.exists(navigation_dir):
                            # print(navigation_dir)
                            os.chdir(path)
                            self.client.send(bytes('200, DIRECTORY CHANGED!', 'UTF-8'))

                        else:
                            self.client.send(bytes('500, DIRECTORY NOT FOUND!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # 4. create new directory (fixed)
                elif command[0] == ftp_command[3]:
                    if len(command) == 2:
                        dirname = command[1]
                        if os.path.exists(dirname):
                            self.client.send(bytes('500, DIRECTORY ALREADY EXIST', 'UTF-8'))
                        else:
                            os.makedirs(dirname)
                            self.client.send(bytes('200, DIRECTORY CREATED!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # 5. remove directory (fixed)
                elif command[0] == ftp_command[4]:
                    if len(command) == 2:
                        dirname = command[1]
                        if not os.path.exists(dirname):
                            self.client.send(bytes('500, DIRECTORY NOT EXIST!', 'UTF-8'))
                        elif not os.listdir(dirname): # check if directory was empty
                            os.rmdir(dirname)
                            self.client.send(bytes('200, EMPTY DIRECTORY HAS BEEN DELETED!', 'UTF-8'))
                        else: # if directory was not empty
                            os.remove(dirname)
                            self.client.send(bytes('200, DIRECTORY HAS BEEN DELETED!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # 6. upload file (not yet)
                elif command[0] == ftp_command[5]:
                    if len(command) == 2:
                        file = command[1]

                        # read file from client and store it
                        with open(f'{file}', 'wb+') as client_file:
                            real_file = []
                            while True:
                                chunk = self.client.recv(2048)
                                # end of file
                                if not chunk:
                                    break

                                real_file.append(chunk)
                                print('[RECV] buffer or data!')
                                time.sleep(0.3)

                            for data in real_file:
                                client_file.write(data)


                        print('200, FILE UPLOADED!')
                        self.client.send(bytes('200, FILE UPLOADED!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # 7. download file (not yet)
                elif command[0] == ftp_command[6]:
                    file = command[1]
                    self.downloadFile(file, self.client)

                # 8. rename file (fixed)
                elif command[0] == ftp_command[7]:
                    if len(command) == 3:
                        oldname = command[1]
                        newname = command[2]
                        old_filepath = os.getcwd() + "\\" + oldname
                        new_filepath = os.getcwd() + "\\" + newname

                        if not os.path.exists(old_filepath):
                            self.client.send(bytes("500, FILE DOESN'T EXIST!", 'UTF-8'))
                        else:
                            os.rename(old_filepath, new_filepath)
                            self.client.send(bytes('200, SUCCESS TO RENAME FILE!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # 9. delete file (fixed)
                elif command[0] == ftp_command[8]:
                    if len(command) == 2:
                        filename = command[1]

                        filepath = os.getcwd() + "\\" + filename

                        if not os.path.exists(filepath):
                            self.client.send(bytes("500, FILE DOESN'T EXIST!", 'UTF-8'))
                        else:
                            os.remove(filepath)
                            self.client.send(bytes('200, FILE DELETED!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

                # get help
                elif command[0] == ftp_command[9]:
                    get_help = '''
                     1. LIST :: list all directories and folders
                     2. PWD :: get current working directory
                     3. CWD <dir_path> :: change working directory
                     4. MKD <dirname> :: create new directory
                     5. RMD <dirname> :: remove directory
                     6. STOR <filename> :: upload file into server
                     7. RETR <filename> :: download file from server
                     8. RNTO <oldname> <newname> :: change filename
                     9. DELE <filename> :: delete file
                    10. QUIT :: close client connection from server
                    11. HELP :: get list of ftp command
                    '''
                    self.client.send(bytes(get_help, 'UTF-8'))

                elif command[0] not in ftp_command:
                    self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

            else:
                self.client.close()
                running = 0

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    user = 'ferdi'
    password = 'ferdi123'

    Server = FTPServer(host, port, user, password)
    Server.run()



