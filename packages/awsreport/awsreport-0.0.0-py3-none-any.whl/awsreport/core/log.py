from colorama import Fore, init

class Logging():
    def __init__(self):
        init(autoreset=True)

    def print_green(self, msg):
        print('\033[1;92m' + msg)

    def print_yellow(self, msg):
        print('\033[1;93m' + msg)
