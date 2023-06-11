import socket
import select
import sys
import time
import os
import threading

sys.path.append('../Client')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
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
        
    def loginAuth(self, username, password, sock):
        if username == self.user and password == self.password:
            sock.send('201, LOGIN SUCCESS!')
        else:
            sock.send('500, LOGIN FAILED!')

    # not fix
    def getList(self, sock):
        list = os.listdir()
        print(list)
        print('200, success')

    def currentDir(self, sock):
        pwd = os.getcwd()
        print(pwd)
        print('200, SUCCESS!')

    # Change directory (not fix)
    def changeDir(self, path, sock):
        try:
            cwd = os.chdir(path)
            print('200, directory changed')
        except:
            print('400, directory not found')

    # Create a new directory
    def makeDir(self, dirname, sock):
        if os.path.exists(dirname):
           raise Exception('500, directory already exist')
        else:
            os.makedirs(dirname)
            print('200, directory created')

    # Download file
    def downloadFile(self, filename, client_socket):
        with open(filename, 'rb') as f:
            content = f.read()

        client_socket.sendall(content)
        print('200, file downloaded successfully')

    # Upload file
    def uploadFile(self, filename, client_socket):
        with open(filename, 'wb') as f:
            content = client_socket.recv(BUFFER)
            f.write(content)

        print('200, file uploaded successfully')

    # Rename file
    def renameFile(self, oldname, newname, sock):
        try:
            os.rename(oldname, newname)
            print('200, file renamed successfully')
        except:
            print('500, failed to rename file')

    def run(self):
        self.bind()
        inputSocket = [self.serverSocket]

        try:
            while True:
                readList, writeList, exceptionList = select.select(self.inputSocket, [], [])

                for sock in readList:
                    if sock == self.serverSocket:
                        client_socket, client_address = self.serverSocket.accept()
                        cThread = ClientThread(client_socket, client_address)
                        cThread.start()
                        self.threads.append(cThread)
                        inputSocket.append(client_socket)
                        print('connected to client: ', client_address)

                    else:
                        sock.close()
                        self.inputSocket.remove(sock)
                        # data = sock.recv(1024)
                        # print(sock.getpeername(), data)
                        #
                        # if data:
                        #     # sock.send(data)
                        #     command = data.split()
                        #
                        #     # this is your choice to command
                        #     if command[0] == 'LOGIN':
                        #         username = command[1]
                        #         password = command[2]
                        #         self.loginAuth(username, password, sock)
                        #
                        #     # list all files and directories
                        #     elif command[0] == 'LIST':
                        #         self.getList()
                        #
                        #     # get current directory
                        #     elif command[0] == 'PWD':
                        #         self.currentDir()
                        #
                        #     # change directory
                        #     elif command[0] == 'CWD':
                        #         path = command[1]
                        #         cwd = self.changeDir(path)
                        #
                        #     # upload file
                        #     elif command[0] == 'STOR':
                        #         file = command[1]
                        #         self.uploadFile(file, client_socket)
                        #
                        #     # download file
                        #     elif command[0] == 'RETR':
                        #         file = command[1]
                        #         self.downloadFile(file, client_socket)

                        # else:
                        #     sock.close()
                        #     self.inputSocket.remove(sock)

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

    def loginAuth(self, username, password, sock):
        if username == self.user and password == self.password:
            sock.send('201, LOGIN SUCCESS!')
        else:
            sock.send('500, LOGIN FAILED!')

    # not fix
    def getList(self, sock):
        list = os.listdir()
        print(list)
        print('200, success')

    def currentDir(self, sock):
        pwd = os.getcwd()
        print(pwd)
        print('200, SUCCESS!')

    # Change directory (not fix)
    def changeDir(self, path, sock):
        try:
            cwd = os.chdir(path)
            print('200, directory changed')
        except:
            print('400, directory not found')

    # Create a new directory
    def makeDir(self, dirname, sock):
        if os.path.exists(dirname):
           raise Exception('500, directory already exist')
        else:
            os.makedirs(dirname)
            print('200, directory created')

    # Download file
    def downloadFile(self, filename, client_socket):
        with open(filename, 'rb') as f:
            content = f.read()

        client_socket.sendall(content)
        print('200, file downloaded successfully')

    # Upload file
    def uploadFile(self, filename, client_socket):
        with open(filename, 'wb') as f:
            content = client_socket.recv(BUFFER)
            f.write(content)

        print('200, file uploaded successfully')

    # Rename file
    def renameFile(self, oldname, newname, sock):
        try:
            os.rename(oldname, newname)
            print('200, file renamed successfully')
        except:
            print('500, failed to rename file')

    def run(self):
        auth = self.client.recv(self.buffer).decode('UTF-8')
        loginCredentials = 'LOGIN ' + self.user + '' + self.password

        if auth == loginCredentials:
            self.client.send('201, LOGIN SUCCESS!')
            running = 1
        else:
            self.client.send('500, LOGIN FAILED!')
            self.client.close()
            running = 0

        while running:
            data = self.client.recv(self.buffer)
            print('received: ', self.address, data)
            if data:
                # sock.send(data)
                command = data.split()

                # this is your choice to command
                if command[0] == 'LOGIN':
                    username = command[1]
                    password = command[2]
                    self.loginAuth(username, password, sock)

                # list all files and directories
                elif command[0] == 'LIST':
                    self.getList()

                # get current directory
                elif command[0] == 'PWD':
                    self.currentDir()

                # change directory
                elif command[0] == 'CWD':
                    path = command[1]
                    cwd = self.changeDir(path)

                # upload file
                elif command[0] == 'STOR':
                    file = command[1]
                    self.uploadFile(file, client_socket)

                # download file
                elif command[0] == 'RETR':
                    file = command[1]
                    self.downloadFile(file, client_socket)
            else:
                self.client.close()
                running = 0

if __name__ == '__main__':
    host = ' '
    port = 21
    user = ' '
    password = ' '


