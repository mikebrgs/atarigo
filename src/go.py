# standard imports
import sys
import copy

PLAYERS = [1,2]
EMPTY = 0
WIN = 1
DRAW = 0
FLOWER = 3
LOSS = -1
INCOMPLETE = -1

# Cortar extremidades do tabuleir quando elas estão vazias
class State(object):
  """docstring for State"""
  def __init__(self, side, turn):
    super(State, self).__init__()
    # Size of the board
    self.side = side
    # Next player
    self.turn = turn
    self.other = PLAYERS[(PLAYERS.index(self.turn)+1)%2]
    # State of the board
    self.board = list()
    for i in range(0, side):
      self.board.append(list())
      for j in range(0, side):
        self.board[-1].append(0)
    self.clusters = list()
    return

  # row and column from 1, 2, ..., side
  def set(self, colour, row, column):
    if not (colour in PLAYERS):
      return 
    crow = row - 1
    ccolumn = column - 1
    self.board[crow][ccolumn] = colour
    # Update clusters
    self.update_clusters(row,column,colour)
    return

  # row and column from 1, 2, ..., side
  def play(self, player, row, column):
    if not (player in PLAYERS):
      return 
    crow = row - 1
    ccolumn = column - 1
    if player != self.turn:
      return
    if self.board[crow][ccolumn] != 0:
      return
    self.board[crow][ccolumn] = player
    self.turn = PLAYERS[(PLAYERS.index(player)+1)%2]
    self.other = PLAYERS[(PLAYERS.index(self.turn)+1)%2]
    # Update clusters
    self.update_clusters(row,column,player)
    return

  def update_clusters(self, row, column, colour):
    # Update clusters
    new_cluster = [(row, column)]
    old_clusters = list()
    # Above
    if colour == self.getitem(row+1, column):
      for cluster in self.clusters:
        if cluster in old_clusters:
          continue
        if (row+1, column) in cluster:
          old_clusters.append(cluster)
          break
    # Below
    if colour == self.getitem(row-1, column):
      for cluster in self.clusters:
        if cluster in old_clusters:
          continue
        if (row-1, column) in cluster:
          old_clusters.append(cluster)
          break
    # Right
    if colour == self.getitem(row, column+1):
      for cluster in self.clusters:
        if cluster in old_clusters:
          continue
        if (row, column+1) in cluster:
          old_clusters.append(cluster)
          break
    # Left
    if colour == self.getitem(row, column-1):
      for cluster in self.clusters:
        if cluster in old_clusters:
          continue
        if (row, column-1) in cluster:
          old_clusters.append(cluster)
          break
    # Remove old clusters and create new big cluster
    for cluster in old_clusters:
      self.clusters.remove(cluster)
      new_cluster.extend(cluster)
    self.clusters.append(new_cluster)
    return

  def next(self):
    return self.turn

  def previous(self):
    return self.other

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

  def getclusters(self):
    return self.clusters

  def getcluster(self, row, column):
    for cluster in self.clusters:
      if (row,column) in cluster:
        return cluster
    return list()

  def __str__(self):
    string = ""
    for i in range(0,self.side):
      for j in range(0,self.side):
        if self.board[i][j] == 1:
          string += " ⚫ "
        elif self.board[i][j] == 2:
          string += " ⚪ "
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

  # Returns true if a play is suicidal or false otherwise
  def suicide(self, state, row, column, stone_colour):
    other_colour = PLAYERS[(PLAYERS.index(stone_colour)+1)%2]
    suicide_state = state.clone()
    suicide_state.play(stone_colour,row,column)
    suicide_cluster = suicide_state.getcluster(row,column)
    if not self.surrounded(state, suicide_cluster):
      return False
    if suicide_state.getitem(row+1, column) == other_colour:
      neighbour_cluster = state.getcluster(row+1,column)
      if self.surrounded(suicide_state, neighbour_cluster):
        return False
    if suicide_state.getitem(row-1, column) == other_colour:
      neighbour_cluster =state.getcluster(row-1,column)
      if self.surrounded(suicide_state, neighbour_cluster):
        return False
    if suicide_state.getitem(row, column+1) == other_colour:
      neighbour_cluster = state.getcluster(row,column+1)
      if self.surrounded(suicide_state, neighbour_cluster):
        return False
    if suicide_state.getitem(row, column-1) == other_colour:
      neighbour_cluster = state.getcluster(row,column-1)
      if self.surrounded(suicide_state, neighbour_cluster):
        return False
    return True


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
    # Check if the board is full -- in this case we are not able to tell
    # who one. This is a bad board, shouldn't happen
    if (len(state.stoneplaces(PLAYERS)) >=
      state.rows() * state.columns()):
      return state.previous()
    # Checks if the clusters are surrounded
    clusters = state.getclusters()
    colours = set()
    for cluster in clusters:
      if self.surrounded(state,cluster):
        stone = cluster[0]
        colours.add(state.getitem(stone[0],stone[1]))
    if len(colours) > 1:
      return FLOWER
    elif len(colours) == 1:
     return PLAYERS[PLAYERS.index(colours.pop())-1]
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

  # Returns a score associated to how good the play is
  def score(self, state, player):
    clusters = state.getclusters()
    freedoms = dict()
    for plr in PLAYERS:
      freedoms[plr] = list()
    for cluster in clusters:
      stone = cluster[0]
      colour = state.getitem(stone[0],stone[1])
      freedoms[colour].append(self.freedom(state,cluster))
    other_player = PLAYERS[PLAYERS.index(player)-1]
    if len(freedoms[other_player]) == 0:
      return 0.0
    if len(freedoms[player]) == 0:
      return 0.0
    this_score = float(min(freedoms[player]))
    other_score = float(min(freedoms[other_player]))
    return (this_score - other_score) / (other_score + this_score)

  def neighbours(self, state, action):
    count = 0
    if state.getitem(action[1]+1,action[2]) in PLAYERS:
      count += 1
    if state.getitem(action[1],action[2]+1) in PLAYERS:
      count += 1
    if state.getitem(action[1]-1,action[2]) in PLAYERS:
      count += 1
    if state.getitem(action[1],action[2]-1) in PLAYERS:
      count += 1
    return count


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
    elif condition == FLOWER:
      if s.previous() == p:
        return 1
      else:
        return -1
    return analytics.score(s,p)

  def actions(self, s):
    analytics = GameAnalytics()
    # analytics.setstate(s)
    actions = list()
    for row in range(1, s.rows()+1):
      for column in range(1, s.columns()+1):
        if (s.getitem(row,column) == 0
          and not analytics.suicide(s,row,column,s.next())):
          actions.append((s.next(), row, column))
    # Usar função mais rápida e ordenar os primeiros com o terminal
    actions.sort(key = lambda action: analytics.neighbours(s,action), reverse = True)
    selective = [action for action in actions if analytics.neighbours(s,action) != 0]
    nelective = [action for action in actions if analytics.neighbours(s,action) == 0]
    selective.sort(key = lambda action: self.utility(self.result(s,action),self.to_move(s)), reverse = True)
    actions = selective
    actions.extend(nelective)
    return actions

  def result(self, s, a):
    result_state = s.clone()
    result_state.play(a[0],a[1],a[2])
    return result_state

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