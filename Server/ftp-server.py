import socket
import select
import sys
import time
import os
import threading

# to hadle send list type
import pickle

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
        
    # def loginAuth(self, username, password, sock):
    #     if username == self.user and password == self.password:
    #         sock.send('201, LOGIN SUCCESS!')
    #     else:
    #         sock.send('500, LOGIN FAILED!')
    #
    # # not fix
    # def getList(self, sock):
    #     list = os.listdir()
    #     print(list)
    #     print('200, success')
    #
    # def currentDir(self, sock):
    #     pwd = os.getcwd()
    #     print(pwd)
    #     print('200, SUCCESS!')
    #
    # # Change directory (not fix)
    # def changeDir(self, path, sock):
    #     try:
    #         cwd = os.chdir(path)
    #         print('200, directory changed')
    #     except:
    #         print('400, directory not found')
    #
    # # Create a new directory
    # def makeDir(self, dirname, sock):
    #     if os.path.exists(dirname):
    #        raise Exception('500, directory already exist')
    #     else:
    #         os.makedirs(dirname)
    #         print('200, directory created')
    #
    # # Download file
    # def downloadFile(self, filename, client_socket):
    #     with open(filename, 'rb') as f:
    #         content = f.read()
    #
    #     client_socket.sendall(content)
    #     print('200, file downloaded successfully')
    #
    # # Upload file
    # def uploadFile(self, filename, client_socket):
    #     with open(filename, 'wb') as f:
    #         content = client_socket.recv(BUFFER)
    #         f.write(content)
    #
    #     print('200, file uploaded successfully')
    #
    # # Rename file
    # def renameFile(self, oldname, newname, sock):
    #     try:
    #         os.rename(oldname, newname)
    #         print('200, file renamed successfully')
    #     except:
    #         print('500, failed to rename file')

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

    def loginAuth(self, username, userpass, sock):
        if username == self.user and userpass == self.password:
            sock.send('201, LOGIN SUCCESS!')
        else:
            sock.send('500, LOGIN FAILED!')

    # not fix
    def getList(self):
        list = os.listdir()
        print(list)
        print(type(list))
        # self.client.send(bytes(list))
        print('200, success')

    def currentDir(self, sock):
        pwd = os.getcwd()
        print(pwd)
        self.client.send(bytes('200, SUCCESS!', 'UTF-8'))
        self.client.send(bytes(pwd, 'UTF-8'))

    # Change directory (not fix)
    def changeDir(self, path):
        if not os.path.exists(path):
            self.client.send(bytes('500, FAILED TO CHANGE DIRECTORY!', 'UTF-8'))
        else:
            os.chdir(path)
            self.client.send(bytes('200, DIRECTORY CHANGED!', 'UTF-8'))

    # Create a new directory
    def makeDir(self, dirname):
        if os.path.exists(dirname):
            self.client.send('500, directory already exist')
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
    def uploadFile(self, filename):
        with open(filename, 'wb') as f:
            content = self.client.recv(BUFFER).decode('UTF-8')
            f.write(content)

        print('200, file uploaded successfully')

    # Rename file
    def renameFile(self, oldname, newname):
        try:
            os.rename(oldname, newname)
            print('200, file renamed successfully')
        except:
            print('500, failed to rename file')

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
                # sock.send(data)
                ftp_command = [
                    'LIST',
                    'PWD',
                    'CWD',
                    'STOR',
                    'RETR',
                    'HELP'
                ]
                command = data.decode().split()

                # this is your choice to command
                # list all files and directories
                if command[0] == ftp_command[0]:
                    list = os.listdir()
                    data = str(list)
                    print(list)
                    print(type(list))
                    self.client.send(bytes(data, 'UTF-8'))
                    print('200, success')

                # get current directory
                elif command[0] == ftp_command[1]:
                    pwd = os.getcwd()
                    print('200, SUCCESS!')
                    self.client.send(pwd.encode('UTF-8'))


                # change directory
                elif command[0] == ftp_command[2]:
                    if len(command) == 2:
                        path = command[1]
                        if path:
                            self.changeDir(path)
                        else:
                            self.client.send(bytes('500, FAILED TO CHANGE DIRECTORY!', 'UTF-8'))
                    else:
                        self.client.send(bytes('500, FAILED TO CHANGE DIRECTORY!', 'UTF-8'))

                # upload file
                elif command[0] == ftp_command[3]:
                    file = command[1]
                    self.uploadFile(file, self.client)

                # download file
                elif command[0] == ftp_command[4]:
                    file = command[1]
                    self.downloadFile(file, self.client)

                elif command[0] == ftp_command[5]:
                    get_help = '''
                    1. LIST :: list all directories and folders
                    2. PWD :: get current working directory
                    3. CWD <dir_path> :: change working directory
                    4. STOR <filename> :: upload file into server
                    5. RETR <filename> :: download file from server
                    6. QUIT :: close client connection from server
                    7. HELP :: get list of ftp command
                    '''
                    self.client.send(bytes(get_help, 'UTF-8'))

                elif command[0] not in ftp_command:
                    self.client.send(bytes('500, WRONG COMMAND!', 'UTF-8'))

            else:
                self.client.close()
                running = 0

if __name__ == '__main__':
    host = '10.8.108.142' or '127.0.0.1'
    port = 8080
    user = 'ferdi'
    password = 'ferdi123'

    Server = FTPServer(host, port, user, password)
    Server.run()



