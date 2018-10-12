# standard imports
import sys
import numpy as np

class Game(object):
  """docstring for Game"""
  def __init__(self, arg):
    super(Game, self).__init__()
    self.arg = arg

  def to_move(self, s):
    pass
    
  def terminal_test(self, s):
    pass

  def utility(self, s):
    pass

  def actions(self, s):
    pass

  def result(self, s, a):
    pass

  def load_board(self, s):
    pass

def main(argv):
  pass

if __name__ == "__main__":
  main(sys.argv)