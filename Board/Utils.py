'''
Created on Dec 7, 2014

@author: Robert
'''
import string 

def on_board(square):
    if len(square) > 2: return False
    return square[0] in 'abcdefgh' and 0 < int(square[1]) < 9

def move_file(file_letter, value):
    current_file =  string.ascii_lowercase.find(file_letter)
    return string.ascii_lowercase[current_file + value]

def northeast_diagonal(square):
    file, rank = square[0], int(square[1])
    return move_file(file, 1) + str(rank + 1)

def northwest_diagonal(square):
    file, rank = square[0], int(square[1])
    return move_file(file, -1) + str(rank + 1)

def southeast_diagonal(square):
    file, rank = square[0], int(square[1])
    return move_file(file, 1) + str(rank - 1)

def southwest_diagonal(square):
    file, rank = square[0], int(square[1])
    return move_file(file, -1) + str(rank - 1)

def up_file(square):
    file, rank = square[0], int(square[1])
    return file + str(rank + 1)

def down_file(square):
    file, rank = square[0], int(square[1])
    return file + str(rank - 1)

def east_rank(square):
    file, rank = square[0], int(square[1])
    return move_file(file, -1) + str(rank)

def west_rank(square):
    file, rank = square[0], int(square[1])
    return move_file(file, 1) + str(rank)


 


        