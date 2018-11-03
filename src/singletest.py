import sys
import go

sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/ext/aima-python/')
import games

file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data13.txt", "r")
game = go.Game()
state = game.load_board(file)
print(state)
# print(game.actions(state))
print(games.alphabeta_cutoff_search(state,game))