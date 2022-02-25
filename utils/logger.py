from typing import Optional
from termcolor import colored


def log_warning(header: str, message: Optional[str]=''):
    print(colored(f"WARNING: {header}\n{message}", 'yellow'))
