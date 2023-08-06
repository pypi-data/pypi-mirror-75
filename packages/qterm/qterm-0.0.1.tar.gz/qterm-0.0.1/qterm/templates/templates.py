
import re
from typing import NamedTuple, Union


class TermArgs(NamedTuple):
    SPAWN_COMMAND: str
    PROMPT: Union[str, re.Pattern]
    EXIT_COMMAND: str = 'exit'


CMD_PROMPT = re.compile(r'[A-Z]\:.+>')
CMD = TermArgs('cmd', CMD_PROMPT)

PYTHON_PROMPT = re.compile(r'^>>> ')
PYTHON = TermArgs('python', PYTHON_PROMPT, 'exit()')
PYTHON3 = TermArgs('python3', PYTHON_PROMPT, 'exit()')

UBUNTU_2004_PROMPT = re.compile(r'^[\w\-]+@[\w\-]+\:.+\$ ')
UBUNTU_2004 = TermArgs('ubuntu2004', UBUNTU_2004_PROMPT)

ARCH_PROMPT = re.compile(r'^\[[\w\-]+@[\w\-]+ .+\]# ')
ARCH = TermArgs('arch', ARCH_PROMPT)
