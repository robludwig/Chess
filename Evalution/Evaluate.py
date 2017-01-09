'''
Created on Dec 7, 2014

@author: Robert
'''

from Board import Board, Piece, Utils

from collections import Counter

CHECKMATE_VALUE = 10000
CENTRAL_SQUARES = ['e4', 'e5', 'd4', 'd5']

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

def evaluate_control(board):
    white_center_squares = [square for square in board.get_white_attacked_squares() if square in CENTRAL_SQUARES]
    black_central_squares = [square for square in board.get_black_attacked_squares() if square in CENTRAL_SQUARES]
    return len(white_center_squares) - len(black_central_squares)                         
    
def evaluate(board):
    if board.is_checkmate():
        return CHECKMATE_VALUE if board.is_white_checkmate() else -1 * CHECKMATE_VALUE
    return {
                'material' : evaluate_material(board),
                'squares'  : evaluate_squares(board),
                'center_control' : evaluate_control(board)
            }
          