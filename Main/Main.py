'''
Created on Dec 6, 2014

@author: Robert
'''

from Board import Board
from Evalution.EvaluateBoard import evaluate

if __name__ == '__main__':
    board = Board.Board()
    board.reset_to_starting_positiion()
    print(board)
    print(board.get_white_pieces())
    print(sum([piece.get_base_value() for piece in board.get_black_pieces()]))
    print(evaluate(board))