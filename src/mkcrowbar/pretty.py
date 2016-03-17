import sys

from plumbum   import colors
from threading import Thread, Event
from time      import sleep


def say(msg):
   print(colors.light_gray | msg)

def fatal(msg, exit=127):
   print(colors.red | "  Fatal: {}".format(msg))
   if exit:
      sys.exit(exit)

def warn(msg):
   print(colors.red | "  Warn: {}".format(msg))

def info(msg):
   print(colors.blue | "  Info: {}".format(msg))


class spinner(object):
   def __init__(self, message):
      self.message = message
      self.running = Event()
      self.sign = colors.light_green | '✓'
      self.thread  = Thread(target=self.run_spinner)
      self.steps   = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

   def __enter__(self):
      self.running.set()
      self.thread.start()
      return self

   def __exit__(self, type, value, traceback):
      self.running.clear()
      self.thread.join()

   def success(self, msg=None):
      self.running.clear()
      self.thread.join()
      if msg:
         print(colors.light_gray | '      :: {}'.format(msg))

   def fail(self, msg=None, exit=127):
      self.sign    = colors.light_red | '✗'
      self.running.clear()
      self.thread.join()
      if msg:
         print(colors.light_red | '      !! {}'.format(msg))
         if exit:
            sys.exit(exit)

   def run_spinner(self):
      i = 0
      while self.running.is_set():
         step = colors.light_blue | self.steps[i]

         print("\r  {char} {message}...".format(char = step, message = self.message), end='', flush=True)
         sleep(0.05)

         i = (i + 1) if i < len(self.steps) - 1 else 0
      print("\r  {char} {message}...".format(char = self.sign, message = self.message))

      

         




