import sys

from plumbum   import colors
from threading import Thread, Event
from time      import sleep
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


class spinner(object):
   def __init__(self, message):
      self.notes   = 1
      self.message = message
      self.running = Event()
      self.sign    = colors.light_green | '✓'
      self.thread  = Thread(target=self.run_spinner)
      self.steps   = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


   def __enter__(self):
      print("  # {}...".format(self.message), flush=True)
      self.running.set()
      self.thread.start()
      return self


   def stop(self):
      self.running.clear()
      self.thread.join()



   def __exit__(self, type, value, traceback):
      self.stop()


   def note(self, msg):
      self.notes = self.notes + 1
      self.line(colors.reset, msg)
      

   def success(self, msg=None):
      self.stop()
      if msg:
         self.line(colors.light_green, msg)


   def fail(self, msg=None, exit=127):
      self.sign    = colors.light_red | '✗'
      self.stop()

      if msg:
         self.line(colors.light_red, msg)
      if exit:
         sys.exit(exit)


   def run_spinner(self):
      i = 0
      while self.running.is_set():
         step = colors.light_blue | self.steps[i]

         self.display(step)
         sleep(0.05)

         i = (i + 1) if i < len(self.steps) - 1 else 0
      self.display(self.sign)


   def display(self, char):
      n = self.notes

      print("\033[{}F".format(n), end="") 
      print("  {} {}...".format(char, self.message), flush=True)
      print("\033[{}E".format(n), end="")


   def line(self, color, msg):
      spacer  = colors.light_blue | '      ::'
      message = color | '{}'.format(msg)
      print("{} {}".format(spacer, message))
