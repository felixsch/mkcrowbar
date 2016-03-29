import sys

from plumbum   import colors
from threading import Thread, Event
from time      import sleep
from enum      import Enum
import shutil


def say(msg):
   print(msg)


def fatal(msg, exit=127):
   print(colors.red | "  Fatal: {}".format(msg))
   if exit:
      sys.exit(exit)


def warn(msg):
   print(colors.red | "  Warn: {}".format(msg))


def info(msg):
   print(colors.blue | "  Info: {}".format(msg))


class step(object):

   SIGN_OK         = colors.light_green | '✓'
   SIGN_FAIL       = colors.light_red | '✗'
   SIGN_WAIT       = colors.light_blue | '#'

   SPINNER_STEPS   = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

   def __init__(self, title, indent=0):
      self.title        = title
      self.current      = title
      self.current_note = None
      self.thread       = Thread(target=self.run)
      self.running      = Event()
      self.running_task = False
      self.indent       = indent


   def task(self, desc):
      if self.running_task:
         self.done()

      self.print(self.SIGN_WAIT, desc, self.indent + 2)
      self.current = desc
      self.running_task = True

      if not self.running.is_set():
         self.running.set()
         self.thread.start()


   def note(self, note):
      self.current_note = note


   def done(self, desc=None):
      self.running_task = False
      self.current_note = None
      self.up(1)
      self.print(self.SIGN_OK, self.current, self.indent + 2, desc)


   def fail(self, message, exit=False):
      self.stop()
      self.print(self.SIGN_FAIL, colors.light_red | message, self.indent + 2)
      if exit:
         sys.exit(exit)


   def success(self, message):
      self.stop()
      self.print(self.SIGN_OK, colors.light_green | message, self.indent + 2)


   def substep(self, message):
      return Step(message, self.ident + 2)


   def __enter__(self):
      self.print('', self.title, 0)
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


   def print(self, sign, message, indent=None, note=None):
      if not indent:
        indent = self.indent

      if note:
         note = "[{}]".format(note)
      else:
         note = ''

      print("\033[2K{indent}{sign} {message} {note}".format(indent  = " " * indent,
                                              sign    = sign,
                                              message = message,
                                              note    = note), flush=True) 
