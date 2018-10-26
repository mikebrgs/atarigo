# standard imports
import sys
import copy

sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/ext/aima-python/')
import games

PLAYERS = [1,2]
EMPTY = 0
WIN = 1
DRAW = 0
LOSS = -1
INCOMPLETE = -1

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

  def clone(self):
    return copy.deepcopy(self)

  # Where are the stones with colours in colours.
  # colours should be a list
  def stoneplaces(self, colours):
    places = list()
    for row in range(0, self.side):
      for column in range(0, self.side):
        if self.board[row][column] in colours:
          places.append((row+1,column+1))
    return places

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

class GameAnalytics(object):
  """docstring for GameAnalytics"""
  def __init__(self, state = None):
    super(GameAnalytics, self).__init__()
    # Maybe for later
    self.state = None

  def cluster(self,state):
    clusters = list()
    for row in range(1, state.rows()+1):
      for column in range(1, state.columns()+1):
        # Skip empty spots
        if state.getitem(row,column) == 0:
          continue
        id = (row,column)
        # Check if already associated to a cluster
        flat_clusters = [stone for cluster in clusters for stone in cluster]
        # for cluster in clusters:
        if id in flat_clusters:
          continue
        # If not, create a new cluster
        cluster = list()
        cluster = self.next(state, cluster, row, column, state.getitem(row,column))
        clusters.append(cluster)
    return clusters

  def next(self, state, cluster, row, column, stone_colour):
    stone_id = (row, column)
    cluster.append(stone_id)
    stone_colour = state.getitem(row, column)
    if (state.getitem(row+1, column) == stone_colour
      and not ((row+1,column) in cluster) ):
      cluster = self.next(state, cluster, row+1, column, stone_colour)
    if (state.getitem(row-1, column) == stone_colour
      and not ((row-1,column) in cluster) ):
      cluster = self.next(state, cluster, row-1, column, stone_colour)
    if (state.getitem(row, column+1) == stone_colour
      and not ((row,column+1) in cluster) ):
      cluster = self.next(state, cluster, row, column+1, stone_colour)
    if (state.getitem(row, column-1) == stone_colour
      and not ((row,column-1) in cluster) ):
      cluster = self.next(state, cluster, row, column-1, stone_colour)
    return cluster

  # Returns true if a play is suicidal or false otherwise
  def suicide(self, state, row, column, stone_colour):
    suicide_state = state.clone()
    suicide_state.play(stone_colour,row,column)
    suicide_cluster = self.next(state, list(), row, column, stone_colour)
    return self.surrounded(state, suicide_cluster)

  # Checks the surroundings of a cluster and returns True if it's surronded
  # or false otherwise
  def surrounded(self, state, cluster):
    for stone in cluster:
      if (not (state.getitem(stone[0]+1,stone[1]) in PLAYERS)
        and not (state.getitem(stone[0]+1,stone[1]) is None)):
        return False
      if (not (state.getitem(stone[0]-1,stone[1]) in PLAYERS)
        and not (state.getitem(stone[0]-1,stone[1]) is None)):
        return False
      if (not (state.getitem(stone[0],stone[1]+1) in PLAYERS)
        and not (state.getitem(stone[0],stone[1]+1) is None)):
        return False
      if (not (state.getitem(stone[0],stone[1]-1) in PLAYERS)
        and not (state.getitem(stone[0],stone[1]-1) is None)):
        return False
    return True

  # Returns the player who won the game, 0 for a draw or -1 for a game
  # that is not over
  def condition(self, state):
    # Checks if the clusters are surrounded
    clusters = self.cluster(state)
    for cluster in clusters:
      if self.surrounded(state,cluster):
        stone = cluster[0]
        return state.getitem(stone[0],stone[1])
    # Check if the board is full -- in this case we are not able to tell
    # who one. This is a bad board, shouldn't happen
    if (len(state.stoneplaces(PLAYERS)) >=
      state.rows() * state.columns()):
      return DRAW
    # Checks for suicidal moves
    empty_points = state.stoneplaces([EMPTY])
    for blank in empty_points:
      if not self.suicide(state,blank[0],blank[1],state.next()):
        return INCOMPLETE
    return DRAW

  # Returns the points of freedom of a specific cluster
  def freedom(self, state, cluster):
    freedom_score = 0
    freedom_list = list()
    for stone in cluster:
      if (state.getitem(stone[0]+1,stone[1]) == EMPTY
        and not ((stone[0]+1,stone[1]) in freedom_list)):
        freedom_score += 1
      if (state.getitem(stone[0]-1,stone[1]) == EMPTY
        and not ((stone[0]-1,stone[1]) in freedom_list)):
        freedom_score += 1
      if (state.getitem(stone[0],stone[1]+1) == EMPTY
        and not ((stone[0],stone[1]+1) in freedom_list)):
        freedom_score += 1
      if (state.getitem(stone[0],stone[1]-1) == EMPTY
        and not ((stone[0],stone[1]-1) in freedom_list)):
        freedom_score += 1
    return freedom_score


  def score(self, state, player):
    clusters = self.cluster(state)
    freedoms = dict()
    for plr in PLAYERS:
      freedoms[plr] = list()
    # colours = list()
    for cluster in clusters:
      stone = cluster[0]
      colour = state.getitem(stone[0],stone[1])
      freedoms[colour].append(self.freedom(state,cluster))
    this_score = float(max(freedoms[player]))
    other_score = float(max(freedoms[freedoms.index(player)-1]))
    return (other_score-this_score)/(other_score+this_score)


class Game(object):
  """docstring for Game"""
  def __init__(self):
    super(Game, self).__init__()

  def to_move(self, s):
    return s.next()
    
  def terminal_test(self, s):
    analytics = GameAnalytics()
    # analytics.setstate(s)
    condition = analytics.condition(s)
    if condition == INCOMPLETE:
      return False
    return True

  def utility(self, s, p):
    analytics = GameAnalytics()
    # analytics.setstate(s)
    condition = analytics.condition(s)
    if condition == p:
      return 1
    elif condition == DRAW:
      return 0
    elif condition in PLAYERS:
      return -1
    return analytics.score(s,p)
    

  def actions(self, s):
    analytics = GameAnalytics()
    # analytics.setstate(s)
    actions = list()
    for row in range(1, s.rows()+1):
      for column in range(1, s.columns()+1):
        if (s.getitem(row,column) == 0
          and analytics.suicide(s,row,column,s.next())):
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
  file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data6.txt", "r")
  game = Game()
  state = game.load_board(file)
  # cloned_state = game.result(state.clone(), (1,1,1))
  # print(state)
  # print(cloned_state)
  # print(state)
  print(game.terminal_test(state))
  # print(games.alphabeta_search(state, game))
  # print(state)
  # print(game.actions(state))
  # print(state)
  # state = game.result(state, (2,2,1))
  # print(state)
  pass

if __name__ == "__main__":
  main(sys.argv)