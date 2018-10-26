# standard imports
import sys

sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/ext/aima-python/')
import games

PLAYERS = [1,2]

class State(object):
  """docstring for State"""
  def __init__(self, side, turn):
    super(State, self).__init__()
    # Size of the board
    self.side = side
    # Next player
    self.turn = turn
    # State of the board
    self.board = list()
    for i in range(0, side):
      self.board.append(list())
      for j in range(0, side):
        self.board[-1].append(0)
    return

  # row and column from 1, 2, ..., side
  def set(self, code, row, column):
    crow = row - 1
    ccolumn = column - 1
    self.board[crow][ccolumn] = code
    return

  # row and column from 1, 2, ..., side
  def play(self, player, row, column):
    crow = row - 1
    ccolumn = column - 1
    if player != self.turn:
      return
    if self.board[crow][ccolumn] != 0:
      return
    self.board[crow][ccolumn] = player
    self.turn = PLAYERS[(PLAYERS.index(player)+1)%2]
    return

  def next(self):
    return self.turn

  def rows(self):
    return self.side

  def columns(self):
    return self.side

  def getitem(self, row, column):
    crow = row - 1
    ccolumn = column - 1
    item = None
    if (crow >= 0
      and crow < self.side
      and ccolumn >= 0
      and ccolumn < self.side):
      item = self.board[crow][ccolumn]
    return item

  def __str__(self):
    string = ""
    for i in range(0,self.side):
      for j in range(0,self.side):
        if self.board[i][j] == 1:
          string += " ⚪️ "
        elif self.board[i][j] == 2:
          string += " ⚫️ "
        else:
          string += " 🌫 "
        # string += str(self.board[i][j])
      string += "\n"
    string += "Next player: " + str(self.turn) + "\n"
    return string

class GameOver(object):
  """docstring for GameOver"""
  def __init__(self):
    super(GameOver, self).__init__()

  def cluster(self):
    for row in range(1, self.state.rows()+1):
      for column in range(1, self.state.columns()+1):
        # Skip empty spots
        if self.state.getitem(row,column) == 0:
          continue
        id = (row,column)
        # Check if already associated to a cluster
        flat_clusters = [stone for cluster in self.clusters for stone in cluster]
        # for cluster in clusters:
        if id in flat_clusters:
          continue
        # If not, create a new cluster
        cluster = list()
        cluster = self.next(cluster, row, column, self.state.getitem(row,column))
        self.clusters.append(cluster)
    return

  def next(self, cluster, row, column, stone_colour):
    stone_id = (row, column)
    cluster.append(stone_id)
    stone_colour = self.state.getitem(row, column)
    if (self.state.getitem(row+1, column) == stone_colour
      and not ((row+1,column) in cluster) ):
      cluster = self.next(cluster, row+1, column, stone_colour)
    if (self.state.getitem(row-1, column) == stone_colour
      and not ((row-1,column) in cluster) ):
      cluster = self.next(cluster, row-1, column, stone_colour)
    if (self.state.getitem(row, column+1) == stone_colour
      and not ((row,column+1) in cluster) ):
      cluster = self.next(cluster, row, column+1, stone_colour)
    if (self.state.getitem(row, column-1) == stone_colour
      and not ((row,column-1) in cluster) ):
      cluster = self.next(cluster, row, column-1, stone_colour)
    return cluster

  def suicide(self, row, column, stone_colour):
    stone_id = (row, column)
    cluster = list()
    cluster = self.next(cluster, row, column, stone_colour)
    is_suicide = True
    for stone in cluster:
      if (not (self.state.getitem(stone[0]+1,stone[1]) in PLAYERS)
        and not (self.state.getitem(stone[0]+1,stone[1]) is None)):
        is_suicide = False
        break
      if (not (self.state.getitem(stone[0]-1,stone[1]) in PLAYERS)
        and not (self.state.getitem(stone[0]-1,stone[1]) is None)):
        is_suicide = False
        break
      if (not (self.state.getitem(stone[0],stone[1]+1) in PLAYERS)
        and not (self.state.getitem(stone[0],stone[1]+1) is None)):
        is_suicide = False
        break
      if (not (self.state.getitem(stone[0],stone[1]-1) in PLAYERS)
        and not (self.state.getitem(stone[0],stone[1]-1) is None)):
        is_suicide = False
        break
    if is_suicide:
      return True

  def checkborders(self):
    for cluster in self.clusters:
      is_gameover = True
      for stone in cluster:
        if (not (self.state.getitem(stone[0]+1,stone[1]) in PLAYERS)
          and not (self.state.getitem(stone[0]+1,stone[1]) is None)):
          is_gameover = False
          break
        if (not (self.state.getitem(stone[0]-1,stone[1]) in PLAYERS)
          and not (self.state.getitem(stone[0]-1,stone[1]) is None)):
          is_gameover = False
          break
        if (not (self.state.getitem(stone[0],stone[1]+1) in PLAYERS)
          and not (self.state.getitem(stone[0],stone[1]+1) is None)):
          is_gameover = False
          break
        if (not (self.state.getitem(stone[0],stone[1]-1) in PLAYERS)
          and not (self.state.getitem(stone[0],stone[1]-1) is None)):
          is_gameover = False
          break
      if is_gameover:
        return self.state.getitem(stone[0],stone[1])
    full = True
    for row in range(1,self.state.rows()+1):
      for column in range(1,self.state.columns()+1):
        if self.state.getitem(row,column) == 0:
          return -1
    return 0

  def condition(self, state):
    self.state = state
    self.clusters = list()
    self.cluster()
    if self.checkborders() == -1:
      return False
    return True

  def winner(self, state):
    self.state = state
    self.clusters = list()
    self.cluster()
    return self.checkborders()

class Game(object):
  """docstring for Game"""
  def __init__(self):
    super(Game, self).__init__()

  def to_move(self, s):
    return s.next()
    
  def terminal_test(self, s):
    gameover = GameOver()
    return gameover.condition(s)

  def utility(self, s, p):
    gameover = GameOver()
    winner = gameover.winner(s)
    if winner == p:
      return 1
    elif winner == 0:
      return 0
    elif winner in PLAYERS:
      return -1
    # Real utility function
    

  def actions(self, s):
    actions = list()
    for row in range(1, s.rows()+1):
      for column in range(1, s.columns()+1):
        if s.getitem(row,column) == 0:
          actions.append((s.next(), row, column))
    return actions

  def result(self, s, a):
    s.play(a[0], a[1], a[2])
    return s

  def load_board(self, s):
    state = None
    line_number = 0
    for line in s:
      line = line.replace("\n","")
      # Line 0 -- get game parameters
      if line_number == 0:
        line = line.split(" ")
        if len(line) != 2:
          return
        else:
          state = State(int(line[0]), int(line[1]))
      # Line != 0 -- get board status
      else:
        for i in range(0,state.side):
          state.set(int(line[i]),line_number, i + 1)
      line_number += 1
    return state

def main(argv):
  file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data4.txt", "r")
  game = Game()
  state = game.load_board(file)
  print(state)
  print(game.terminal_test(state))
  # print(games.alphabeta_search(state, game))
  # print(state)
  # print(game.actions(state))
  # state = game.result(state, (1,1,1))
  # print(state)
  # state = game.result(state, (2,2,1))
  # print(state)
  pass

if __name__ == "__main__":
  main(sys.argv)