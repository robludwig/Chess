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


        