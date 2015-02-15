'''
Created on Dec 7, 2014

@author: Robert
'''

from Board import Board, Piece, Utils

from collections import Counter

def evaluate_material(board):
    #list
    white_pieces = sum([piece.get_base_value() for piece in board.get_white_pieces()])
    black_pieces = sum([piece.get_base_value() for piece in board.get_black_pieces()])
    return white_pieces - black_pieces     

def evaluate_squares(board):
    white_squares = Counter(board.get_white_attacked_squares())
    black_squares = Counter(board.get_black_attacked_squares())
    
    #print ("white squares", white_squares)
    #print ("black squares", black_squares)
    sum = 0
    for square in Utils.all_squares:
        square_attack = white_squares[square] - black_squares[square]
        if square_attack > 0:
            sum += 1
        elif square_attack < 0:
            sum -= 1
    return sum
    
def evaluate(board):
    return {
                'material' : evaluate_material(board),
                'squares'  : evaluate_squares(board)
            }
          