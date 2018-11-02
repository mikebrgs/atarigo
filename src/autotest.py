import sys

import go

path = "/Users/mikebrgs/CurrentWork/tecnico/iasd/proj1/data/"
#path = "C:/Users/loure/Dropbox/Lourenço/Faculdade/5A1S/IASD/atarigo/data/"

print("---terminal_test---")
# Test 1
file = open(path+"data1.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.terminal_test(state) == False:
  print("Test 1: Success")
else:
  print("Test 1: Failure")

# Test 2
file = open(path+"data2.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.terminal_test(state) == False:
  print("Test 2: Success")
else:
  print("Test 2: Failure")

# Test 3
file = open(path+"data3.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.terminal_test(state) == True:
  print("Test 3: Success")
else:
  print("Test 3: Failure")

# Test 4
file = open(path+"data4.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.terminal_test(state) == False:
  print("Test 4: Success")
else:
  print("Test 4: Failure")

# Test 5
file = open(path+"data5.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.terminal_test(state) == True:
  print("Test 5: Success")
else:
  print("Test 5: Failure")

# # Test 6
# file = open(path+"data6.txt", "r")
# game = go.Game()
# state = game.load_board(file)
# if game.terminal_test(state) == True:
#   print("Test 6: Success")
# else:
#   print("Test 6: Failure")

print("---utitity---")
# Test 1
file = open(path+"data1.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == 0.2:
  print("Test 1: Success")
else:
  print("Test 1: Failure")

# Test 2
file = open(path+"data2.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == 0.0:
  print("Test 2: Success")
else:
  print("Test 2: Failure")

# Test 3
file = open(path+"data3.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == 0:
  print("Test 3: Success")
else:
  print("Test 3: Failure")

# Test 4
file = open(path+"data4.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == -1.0/3.0:
  print("Test 4: Success")
else:
  print("Test 4: Failure")

# Test 5
file = open(path+"data5.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == -1:
  print("Test 5: Success")
else:
  print("Test 5: Failure")

# Test 6
file = open(path+"data6.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == 0.0:
  print("Test 6: Success")
else:
  print("Test 6: Failure")

# Test 7
file = open(path+"data7.txt", "r")
game = go.Game()
state = game.load_board(file)
if game.utility(state,game.to_move(state)) == -1:
  print("Test 7: Success")
else:
  print("Test 7: Failure")