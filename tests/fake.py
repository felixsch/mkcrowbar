class LocalCommands():

    def __init__(self):
        self.registered = {}

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
    def __init__(self, command, func):
        self.command = command
        self.args = []
        self.call = func

    def __getitem__(self, args):
        self.args = args
        return self

    def run(self, **args):
        return self.call(*self.args)


def returnOk(stdout="No message", returncode=0, expect=None):
    def ok(*args):
        if expect:
            expect(*args)
        return (returncode, stdout, "")
    return ok


def returnErr(stderr="No message", returncode=1):
    return (returncode, "", stderr)


def raiseError(error):
    def raise_(*args):
        raise error
    return raise_
