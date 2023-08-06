
import wexpect
from wexpect import EOF, TIMEOUT
from typing import NamedTuple, Pattern, Union, NoReturn, Iterable, List
from .templates import CMD


class TempPrompt:
    def __init__(self, parent, enter_cmd, regex,
                 exit_cmd, *, timeout=-1, quiet=True):
        self.parent = parent
        self.enter_cmd = enter_cmd
        self.regex = regex
        self.exit_cmd = exit_cmd
        self.timeout = timeout
        self.quiet = quiet

    def __enter__(self):
        self.default_re = self.parent.prompt
        self.default_exit_cmd = self.parent.exit_cmd

        self.parent.prompt = self.regex
        self.parent.exec(self.enter_cmd,
                         timeout=self.timeout,
                         quiet=self.quiet)
        return self.parent

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.parent.prompt = self.default_re
        self.parent.exit_cmd = self.default_exit_cmd

        self.parent.exec(self.exit_cmd,
                         timeout=self.timeout,
                         quiet=self.quiet)


class QTerm:
    def __init__(self, spawn: str = None,
                 prompt_regex: Pattern[str] = None,
                 exit_cmd: str = 'exit',
                 timeout: Union[int, float] = 30) -> None:
        matters_args = spawn, prompt_regex
        assert all(matters_args) or not any(matters_args)

        if not any(matters_args):
            spawn, prompt_regex, exit_cmd = CMD

        assert spawn
        assert prompt_regex
        assert exit_cmd

        self.spawn_cmd = spawn
        self.prompt = prompt_regex
        self.exit_cmd = exit_cmd

        self.spawn(timeout=timeout)

    def spawn(self, timeout: Union[int, float] = 30) -> None:
        self.instance = wexpect.spawn(self.spawn_cmd)
        self.expect(self.prompt, timeout=timeout)

    def temp_prompt(self,
                    command: Union[str, Iterable[str]],
                    regex: Pattern[str],
                    exit_cmd: str = 'exit', *,
                    timeout: Union[int, float] = -1) -> TempPrompt:
        return TempPrompt(self, command, regex, exit_cmd)

    @property
    def prompt(self) -> Pattern[str]:
        return self._prompt_re

    @prompt.setter
    def prompt(self, regex: Pattern[str]) -> None:
        self._prompt_re = regex

    def sendline(self, line: str) -> None:
        self.instance.sendline(line)

    def expect(self, *args, **kwargs) -> int:
        return self.instance.expect(*args, **kwargs)

    def wait_control_flow(self, *args, **kwargs) -> Union[None, NoReturn]:
        res = self.expect([self.prompt, EOF, TIMEOUT], *args, **kwargs)
        if res == 1:
            raise EOF('End-of-file')
        elif res == 2:
            raise TIMEOUT(f'Timeout at output: {self.last_output}')

    def exec(self, lines: Union[str, Iterable[str]],
             quiet: bool = True, *,
             timeout: Union[int, float] = -1,
             step_by_step: bool = False) -> List[str]:

        if isinstance(lines, str):
            lines = lines.split('\n')

        res = []

        def track(line):
            for text in self.track(timeout=timeout):
                if text == line:
                    continue

                if line == '':
                    res.append(text)
                else:
                    res.append(text.rpartition(line)[-1])

                if not quiet:
                    print(text)

        if step_by_step:
            for line in lines:
                self.sendline(line)
                track(line)
        else:
            for line in lines:
                self.sendline(line)
            track(line)

        return res

    def track(self, timeout: Union[int, float] = -1):

        output_map = {ord('\n'): None, ord('\r'): None}
        expect_res = ['\n', self.prompt, EOF, TIMEOUT]

        while True:
            index = self.expect(expect_res, timeout=timeout)
            if index == 0:
                yield self.last_output.translate(output_map)
            elif index == 1:
                return
            elif index == 2:
                raise EOF('End-of-file')
            elif index == 3:
                raise TIMEOUT(f'Timeout at output: {self.last_output}')

    @property
    def last_output(self) -> str:
        if self.after == TIMEOUT:
            return self.before
        return self.before + self.after

    @property
    def before(self) -> str:
        return self.instance.before

    @property
    def after(self) -> Union[str, TIMEOUT]:
        return self.instance.after

    def close(self) -> None:
        self.instance.close()

    def exit(self) -> None:
        self.instance.sendline(self.exit_cmd)

    def sendeof(self) -> None:
        self.instance.sendeof()

    def terminate(self) -> None:
        self.instance.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sendeof()
        self.close()
        self.terminate()
