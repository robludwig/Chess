'''
Created on Dec 6, 2014

@author: Robert
'''

from Board import Board

if __name__ == '__main__':
    board = Board.Board()
    board.reset_to_starting_positiion()
    print(board)