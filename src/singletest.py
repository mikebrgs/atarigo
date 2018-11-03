import sys
import go

sys.path.insert(0, '/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/ext/aima-python/')
import games

file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data12.txt", "r")
game = go.Game()
state = game.load_board(file)
print(state)
# state1 = game.result(state,(2,2,3))
# print(state1)
# print(game.utility(state1,2))
# state2 = game.result(state,(2,5,3))
# print(state2)
# print(game.utility(state2,2))

# print(game.utility(game.result(state,(2,5,3)),2))
# print(game.actions(state))
print(games.alphabeta_cutoff_search(state,game))