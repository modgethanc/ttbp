#!/usr/bin/python

import core

import os

WWW = os.path.join("..","www")
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")

BANNER = open(os.path.join(CONFIG, "banner.txt")).read()
CLOSER = "\n\tsee you later, space cowboy..."

def start():
  print(BANNER)
  print("\n\n\n\n")
  try:
    print(main_menu())
  except ValueError or SyntaxError:
    print("oh no i didn't understand that")
    print(main_menu())
  except KeyboardInterrupt:
    print("eject button fired")
    print(main_menu())
  print(CLOSER)
  
def main_menu():

  print("how are you feeling today? ")

  input()

  return main_menu()
