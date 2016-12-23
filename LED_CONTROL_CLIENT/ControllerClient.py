import socket
import sys
from time import sleep


# checks if brightness is outside the range of 0 - 100

def brightness_out_of_bounds(brightness):
    if brightness < 0 or brightness > 100:
        return True
    else:
        return False


# obtains a brightness percentage between 0 and 100 from the user

def get_brightness_from_user():
    while True:
        brightness = input("Please enter a brightness percentage between 0 and 100")
        if brightness_out_of_bounds(brightness):
            print("The brightness percentage is out of range. Please enter a number between 0 and 100.")
            continue
        break
    return brightness

# checks to see if the user-entered request ID is outside the list of available commands


def request_invalid(request):
    if request not in range(1, 3):

        return True
    else:
        return False

# formats the user's request in the format to be sent to the server


def formulate_request(request):
    if request == 3:
        brightness_value = get_brightness_from_user()
        user_request = 'brightness' + brightness_value
        return user_request
    elif request == 2:
        user_request = 'turnOffRequest'
        return user_request

    else:
        user_request = 'turnOnRequest'
        return user_request

# sends the user's request to the server


def send_command(socket_object, request_to_send):
    socket_object.sendall(str.encode(request_to_send))
    response = socket_object.recv(1024)
    if response.decode('utf-8') == 'OK':
        print('Command Successful')
    else:
        print('The command was unsuccessful. Please try again')


# noinspection PyBroadException
def main():
    total_commands = {('turnOnRequest', 1), ('turnOffRequest', 2), ('brightness', 3)}
    host = input("Enter server IP")
    port = 12345
    user_type = "master"

    try:
        controller = socket.socket()

    except:
        print("Error creating socket")
        print("Check your Network Connection and restart this program")
        sys.exit(1)

    while True:

        try:
            controller.connect((host, port))
        except:
            print("Error connecting to host...Retrying")
            sleep(2)
            continue
        print("Connected to" + host)
        controller.send(str.encode(user_type))
        break

    while True:

        for command in total_commands:
            print("Command: {}, ID: {}".format(command[0], command[1]))
        control_request = input("Select the ID of the command you wish to give. ")
        if request_invalid(control_request):
            print("The ID you entered is invalid. Please select an ID from the list provided")
            continue

        formatted_request = formulate_request(control_request)
        send_command(controller, formatted_request)


if __name__ == '__main__':
    main()
