from termcolor import colored


def log_warning(message: str):
    print(colored(message, 'yellow'))
