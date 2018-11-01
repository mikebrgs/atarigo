import sys
import go

file = open("/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/data7.txt", "r")
game = go.Game()
state = game.load_board(file)
print(state)
print(game.terminal_test(state))
state = game.result(state,(2,5,4))
print(state)