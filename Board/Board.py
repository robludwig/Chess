'''
Created on Dec 6, 2014

@author: Robert
'''

import string

from . import BoardException

class Board:
    '''
    Represents a board as a dictionary and allows piece lookup using board['a1'] syntax.
    Provides helper functions for getting information about the board and its state
    
    Capital letters indicate White pieces, lowercase letters indicate black pieces
    K/k = king
    Q/q = queen
    R/r = rook
    N/n = knight
    B/b = bishop
    P/p = pawn
    This matches the FEN format
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.board = {}
        self.side_to_move = "white"
        self.white_castle_rights = {}
        self.black_castle_rights = {}
        
    def reset_to_starting_positiion(self):
        self.parse_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
    def parse_from_fen(self, fen_string):
        '''
        Loads a FEN string into the current board
        See the specification @ wikipedia: http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        '''
        try:
            piece_placements, active_color, castling_rights, en_passant, half_moves, full_moves = fen_string.split(" ")
        except Exception as fenception:
            print("exception parsing FEN string: ", fenception)     
            raise BoardException("incorrect or unparsable FEN string")
        
        current_square = ['a', 8]
        ranks = piece_placements.split('/')
        for rank_string in ranks:
            for char in rank_string:
                if char.isdigit():
                    current_letter_index = string.lowercase.find(current_square[0])
                    print("current_letter_index is ", current_letter_index, " and the char there is ", string.lowercase[current_letter_index])
                    current_square[0] = string.lowercase[current_letter_index + int(char)]
                else:
                    self.board[current_square[0] + str(current_square[1])] = char
            current_square[1] = current_square[1] - 1
            current_square[0] = 'a'
            
    def __repr__(self):
        return self.board.__repr__()
    
    def is_white_checkmate(self):
        return False
    
    def is_black_checkmate(self):
        return False
    
    def is_checkmate(self):
        return self.is_black_checkmate() or self.is_white_checkmate()
    
    def is_stalemate(self):
        return False
    
    def is_forced_draw(self):
        return self.is_stalemate or self.half_move_counter > 50
        
