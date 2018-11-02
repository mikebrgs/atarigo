import sys
import go
import time
sys.path.insert(0, '/Users/loure/Documents/Github/AIma-python/aima-python')
import games


file = open("data/data13.txt", "r")
game = go.Game()
state = game.load_board(file)
print(state)
print(game.utility(game.result(state, (1,2,1)),2))
print(game.actions(state))
start_time = time.time()
action = games.alphabeta_cutoff_search(state,game,d=4)
print("alpha_beta =", action)
execution_time = time.time() - start_time
print("execution time:", execution_time, "secs")