from typing import Optional
from termcolor import colored


def log_warning(header: str, message: Optional[str]='') -> None:
    '''Prints a warning message in yellow.'''
    _log('yellow', header, message)

def log_error(header: str, message: Optional[str]='') -> None:
    '''Prints an error message in red.'''
    _log('red', header, message)


def _log(color: str, header: str, message: Optional[str]='') -> None:
    print(colored(f"WARNING: {header}\n{message}", color))