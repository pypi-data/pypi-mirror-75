# QTerm
QTerm is a Python module for spawning child applications and controlling them automatically.

## **Usage**

To interract with a child process use `QTerm` class:

```python
from qterm import QTerm

with QTerm() as term:
    print(term.exec('cd'))
```

In case command prompt pattern changes use `temp_prompt` method:

```python
from qterm import QTerm, PYTHON

print(PYTHON)

with QTerm() as term:
    with term.temp_prompt(*PYTHON):
        print(term.exec('1+1'))

# TermArgs(SPAWN_COMMAND='python', PROMPT=re.compile('^>>> '), EXIT_COMMAND='exit()')
# ['2']
```

