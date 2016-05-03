import pytest
import os
import builtins
"""
Implement some test utility functionality. Mostly to test plumbum command based stuff
"""

class LocalCommands():
    """
    Fake the complete LocalMaschine object from plumbum
    """

    def __init__(self):
        self.registered = {}
        self.env = {}

    def has(self, command, func):
        self.registered[command] = func

    def __getitem__(self, command):
        if command not in self.registered:

            raise RuntimeError("""
                               local-commands: Try to run not mocked local call '{}'.

                               If you want to mock this object, use local.register(command, func)
                               """.format(command))
        return LocalCommand(command, self.registered[command])


class LocalCommand():
    """
    A single command implementing the __getitem__ interface
    """

    def __init__(self, command, func):
        self.command = command
        self.args = []
        self.call = func

    def __getitem__(self, args):
        if not isinstance(args, (list, tuple)):
            self.args += [args]
        else:
            self.args += list(args)
        return self

    def __call__(self, *args):
        self.__getitem__(args)
        return self.run()

    def run(self, **args):
        if isinstance(self.call, Stub):
            return self.call.exec(self.command, *self.args)
        return self.call(*self.args)


class Stub():
    """
    Dependency injection for command name
    """
    def __init__(self, func):
        self.func = func

    def exec(self, command, *args):
        return self.func(command, *args)


class StubOpen():
    """
    Fake a file handle
    """
    def __init__(self, monkeypatch=None, func=None):
        self.content = []
        self.func = func
        self.real_open = builtins.open
        self.patch = monkeypatch
        self.args = []

    def read(self):
        if not self.func:
            pytest.fail('Could not call defined function. No wrapper defined')

        self.patch.setattr('builtins.open', self.real_open)
        result = self.func.exec('open', *self.args)
        self.patch.setattr('builtins.open', self)
        return result


    def write(self, line):
        self.content += [line]

    def __call__(self, args):
        self.args = args
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def result(self):
        return self.content


def return_ok(stdout="No message", returncode=0, expect=None):
    """
    return a function which indicates success (return code = 0)
    """
    def ok(*args):
        if expect:
            expect(*args)
        return (returncode, stdout, "")
    return Stub(ok)


def return_error(stderr="No message", returncode=1, expect=None):
    """
    return a function which indicates a failure (higher return code)
    """
    def error(command, *args):
        if expect:
            expect(*args)
        return (returncode, "", command + ": " + stderr)
    return Stub(error)


def raise_error(error):
    """
    returns a function which raises an exception
    """
    def raise_(_, *args):
        raise error
    return Stub(raise_)


def expect_args(required, data=None):
    """
    checks if a command was called with some arguments
    """
    def check_args(command, *args):
        for require in required:
            if require not in args:
                pytest.fail("""
                            {command} called without `{arg}`...
                            Call was: {command} {commands}
                            """.format(command=command, arg=required, commands=" ".join(args)))

        # Step down the Stub stack
        if isinstance(data, Stub):
            return data.exec(command, *args)

        # Plain value
        if not callable(data):
            return data

        # lambda or function
        return data(*args)

    return Stub(check_args)


def load_fixture(filename):
    """
    Load fixture
    """
    def load(command, *args):
        path = os.path.join('tests', 'fixtures', filename + '.fixture')
        try:
            with open(path) as hdl:
                return hdl.read()
        except FileNotFoundError:
            pytest.fail("""
                        Could not load `{}`. Check your fixtures!
                        filepath is `{}`
                        """.format(filename, path))
    return Stub(load)
