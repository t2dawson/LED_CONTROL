import socket
import sys
from time import sleep


# noinspection PyBroadException
class ControllerClient:

    def __init__(self, user_name = "DEFAULT NAME"):

        self.controller = None
        self.brightness = 0
        self.request = 0
        self.user_request = None
        self.initiate_controller_socket()
        self.name = user_name
        self.client_to_control = None

    def initiate_controller_socket(self):

        try:
            self.controller = socket.socket()

        except:
            print("Error creating socket")
            print("Please restart this program")
            sys.exit(1)

# checks if brightness is outside the range of 0 - 100

    def brightness_out_of_bounds(self):

        if self.brightness < 0 or self.brightness > 100:
            return True

        else:
            return False


# obtains a brightness percentage between 0 and 100 from the user

    def get_brightness_from_user(self):
        while True:
            self.brightness = input("Please enter a brightness percentage between 0 and 100")
            if self.brightness_out_of_bounds():
                print("The brightness percentage is out of range. Please enter a number between 0 and 100.")
                continue
            return


# checks to see if the user-entered request ID is outside the list of available commands

    def request_invalid(self):
        if self.request not in range(1, 3):

            return True
        else:
            return False

# formats the user's request in the format to be sent to the server

    def formulate_request(self, commands):
        if self.request == 3:
            self.get_brightness_from_user()
            self.user_request = (commands[2][0] + '-' + self.brightness + '-')

        elif self.request == 2:
            self.user_request = commands[1][0]

        else:
            self.user_request = commands[0][0]
        self.user_request += self.client_to_control

# sends the user's request to the server

    def send_command(self):
        self.controller.sendall(str.encode(self.user_request))
        response = self.controller.recv(1024)
        if response.decode('utf-8') == 'OK':
            print('Command Successful')
        else:
            print('The command was unsuccessful. Please try again')

    def initiate_controller(self, host, port, u_type, commands):

        while True:

            try:
                self.controller.connect((host, port))
            except:
                print("Error connecting to host...Retrying")
                sleep(2)
                continue
            print("Connected to" + host)
            self.controller.send(str.encode(u_type))

            try:

                while True:
                    controlled_clients_list = self.controller.recv(65535)
                    for client in controlled_clients_list:
                        print(client)
                    self.client_to_control = input("Please select the light you want to control")
                    if self.client_to_control not in controlled_clients_list:
                        print("Light does not exist. Please select a valid lightname from the list")
                        continue

                    for command in commands:
                        print("Command: {}, ID: {}".format(command[0], command[1]))
                    self.request = input("Select the ID of the command you wish to give. ")
                    if self.request_invalid():
                        print("The ID you entered is invalid. Please select an ID from the list provided")
                        continue

                    self.formulate_request(commands)
                    self.send_command()
            except:
                print("Lost connection to Host..")
                break

    def close_controller(self):

        print("Closing socket connection for user: " + self.name)
        self.controller.close()
