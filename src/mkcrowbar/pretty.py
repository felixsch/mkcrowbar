import sys

from plumbum   import colors
from threading import Thread, Event
from time      import sleep


def say(msg):
    print(msg)


def fatal(msg, exit=127):
    print(colors.red | "  Fatal: {}".format(msg), file=sys.stderr)
    if exit:
        sys.exit(exit)


def warn(msg):
    print(colors.red | "  Warning: {}".format(msg), file=sys.stderr)


def info(msg):
    print(colors.blue | "  Info: {}".format(msg))


class step(object):

    SIGN_OK         = colors.light_green | '✓'
    SIGN_FAIL       = colors.light_red | '✗'
    SIGN_WAIT       = colors.light_blue | '#'

    SPINNER_STEPS   = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, title, indent=0, interactive=True):
        self.title        = title
        self.current      = title
        self.current_note = None
        self.thread       = Thread(target=self.run)
        self.running      = Event()
        self.running_task = False
        self.indent       = indent
        self.interactive  = interactive

    def task(self, desc):
        if self.running_task:
            self.done()

        self.print(self.SIGN_WAIT, desc, self.indent + 2)
        self.current = desc
        self.running_task = True

        if not self.running.is_set() and self.interactive:
            self.running.set()
            self.thread.start()

    def note(self, note):
        self.current_note = note
        if not self.interactive:
            self.print('    :: ', note)

    def done(self, desc=None):
        self.running_task = False
        self.current_note = None
        if self.interactive:
            self.up(1)
            self.print(self.SIGN_OK, self.current, self.indent + 2, desc)

    def fail(self, message, exit=1):
        self.stop()
        self.print(colors.light_red | '==>', colors.light_red | message, self.indent + 2)
        if exit:
            sys.exit(exit)

    def success(self, message):
        self.stop()
        self.print(colors.light_green | '==>', colors.light_green | message, self.indent + 2)

    def substep(self, message):
        return step(message, self.ident + 2)

    def __enter__(self):
        self.print('', self.title + '...', 0)
        return self

    def stop(self):
        if self.running_task:
            self.done()
        if self.running.is_set():
            self.running.clear()
            self.thread.join()

    def __exit__(self, type, value, traceback):
        self.stop()

    def run(self):
        i = 0
        while self.running.is_set():
            if not self.running_task:
                sleep(0.05)
                continue
            step = colors.light_blue | self.SPINNER_STEPS[i]
            self.up(1)
            self.print(step, self.current, self.indent + 2, self.current_note)
            sleep(0.05)

            i = (i + 1) if i < len(self.SPINNER_STEPS) - 1 else 0

    def up(self, n):
        print("\033[{}F".format(n), end="", flush=True)

    def print(self, sign, message, indent=0, note=None, out=sys.stdout):
        erase = ''

        # only erase up 2 rows if in interactive mode
        if self.interactive:
            erase = '\033[2K'

        if not indent:
            indent = self.indent

        if note:
            note = "[{}]".format(note)
        else:
            note = ''

        output = {'erase': erase,
                  'indent': " " * indent,
                  'sign': sign,
                  'message': message,
                  'note': note}
        print("{erase}{indent}{sign} {message} {note}".format(**output), flush=True, file=out)
