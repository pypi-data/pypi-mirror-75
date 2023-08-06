#!/usr/bin/env python
import os
import sys

USE_COLOR = os.isatty(sys.stdout.fileno())


class COLOR:
  # https://github.com/gawin/bash-colors-256
  black = '\033[30m'
  red = '\033[31m'
  green = '\x1b[38;5;%sm' % "046"
  yellow = '\x1b[38;5;%sm' % "011"
  blue = '\x1b[38;5;%sm' % "051"
  magenta = '\033[35m'
  cyan = '\033[36m'
  gray = '\x1b[38;5;%dm' % 240
  underline = '\033[4m'
  reset = '\033[0m'


RESET = '\033[0m'


class Color:
  def __init__(self, color):
    self.color = getattr(COLOR, color)

  def __call__(self, msg):
    if USE_COLOR:
      if isinstance(msg, (list, tuple)):
        msg = f"{RESET} {self.color}".join(map(str, msg))
      elif not isinstance(msg, str):
        msg = str(msg)
      for i in msg.split("\n"):
        msg = self.color + i + RESET
    return msg

  def __lshift__(self, msg):
    print(self(msg))


class Cout:
  def __getattr__(self, color):
    return Color(color)

  def __lshift__(self, msg):
    if isinstance(msg, (list, tuple)):
      print(*msg)
    else:
      print(msg)


cout = Cout()

if __name__ == "__main__":
  cout.gray << "term"
# import os
# NUMCOL = os.popen("tput colors 2>/dev/null", "r").read()
# print("color", NUMCOL)
