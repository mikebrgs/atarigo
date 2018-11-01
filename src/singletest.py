import sys
import go

# file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data8.txt", "r")
# game = go.Game()
# state = game.load_board(file)
# print(state)
# print(game.terminal_test(state))
# print(game.utility(state,1))
# print(game.utility(state,2))
# state = game.result(state,(2,5,4))
# print(state)
# print(game.terminal_test(state))
# print(game.utility(state,1))
# print(game.utility(state,2))

file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data9.txt", "r")
game = go.Game()
state = game.load_board(file)
print(state)
print(game.actions(state))
