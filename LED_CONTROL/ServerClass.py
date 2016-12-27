import socket
from time import sleep
import multiprocessing
import sys

class ServerObject:

    def __init__(self):

        self.server = None


    def create_socket:

        try:
            self.server = socket.socket()

        except:
            print("Error creating socket")
            print("Please restart this program")
            sys.exit(1)


    def process_request(self):

        self.request = self.server.recv(65535)

        if self.request[:13].decode('utf-8') == 'turnOnRequest':
            controlled_client = self.request[13:].decode('utf-8')
            command = '1' + 'o'
            add_to_queue(command, controlled_client)

        elif self.request[:14].decode('utf-8') == 'turnOffRequest':
            controlled_client = self.request[14:].decode('utf-8')
            command = '0' + 'o'
            add_to_queue(command, controlled_client)


        else:
             data = self.request.decode('utf-8')
             for x in range(len(data)):
                 if data[x] == '-'  and data[x+4] == '-':
                     brightness = data[x+1] + data[x+2] + data[x+3]
                     controlled_client = data[(x+5):]
                     command = '1' + 'n' + brightness
                     add_to_queue(command, controlled_client)

                 elif data[x] == '-' and data[x+3] == '-':
                     brightness = data[x+1] + data[x+2]
                     controlled_client = data[(x+4):]
                     command = '1' + 'n' + brightness
                     add_to_queue(command, controlled_client)

                 elif data[x] == '-' and data[x+2] == '-':
                     brightness = data[x+1]
                     controlled_client = data[(x+3):]
                     command = '1' + 'n' + brightness
                     add_to_queue(command, controlled_client)

