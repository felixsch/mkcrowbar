
import plumbum


def patch_local():
    plumbum.local = Local()


class LocalModule():

    def __init__(self):
        self.registered = {}

    def __getattr__(self, name):
        if name not in self.registered:
            self.registered[name] = FakeCommand()

        return self.registered[name]

    def has_command(self, name):
        if name in self.registered:
            return True
        return False


class Command():
    def __init__(self):
        self.args = []
        self.name = None

    def __getattr__(self, name, *args):
        pass

    def __getitem__(self, name, *args):
        pass





