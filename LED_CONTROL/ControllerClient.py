from ControllerClientClass import *

# TODO: work on command line argument parsing to include background and debug types


def main():
    total_commands = [('turnOnRequest', 1), ('turnOffRequest', 2), ('brightness', 3)]
    host = input("Enter server IP")
    port = 12345
    user_type = "master"
    user_name = input("Please enter the username you wish to use")

    controller = ControllerClient(user_name)
    controller.initiate_controller(host, port, user_type, total_commands)
    controller.close_controller()


if __name__ == '__main__':
    main()
