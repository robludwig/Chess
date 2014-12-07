'''
Created on Dec 7, 2014

@author: Robert
'''

from Board import Board, Piece

def evaluate(board):
    white_pieces = sum([piece.get_base_value() for piece in board.get_white_pieces()])
    black_pieces = sum([piece.get_base_value() for piece in board.get_black_pieces()])
    return white_pieces - black_pieces        