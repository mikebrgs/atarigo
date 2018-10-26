import sys

sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/src/')
import go
sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/ext/aima-python/')
import games

file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/clean.txt", "r")
game = go.Game()
state = game.load_board(file)
print("You are player? [1/2]")
entry = input()
player = 1
computer = 2
exit = False
if entry == "2":
  player = 2
  computer = 1
  # action = game.alphabeta_cutoff_search(state,game)
  # state = game.result(state,action)
while not exit:
  print(state)
  if game.to_move(state) == player:
    entry = input()
    if "exit" in entry:
      exit == True
    elif len(entry.split(" ")) == 2:
      row = int(entry.split(" ")[0])
      column = int(entry.split(" ")[1])
      state = game.result(state,(player,row,column))
  elif game.to_move(state) == computer:
    action = games.alphabeta_cutoff_search(state,game)
    state = game.result(state,action)
  else:
    print("Error")
    sys.exit(0)
  if game.terminal_test(state):
    print(state)
    result = game.utility(state, player)
    if result == 1:
      print("YOU WON")
    elif result == -1:
      print("YOU LOST")
    else:
      print("DRAW")
    sys.exit(0)
