'''
Created on Dec 6, 2014

@author: Robert
'''

import string

from . import BoardException
from .Piece import Piece

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
        self.en_passant_square = None
        self.half_move_count = 0
        self.move_count = 0
        
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
        def move_forward_on_rank(steps=1):
            current_letter_index = string.ascii_lowercase.find(current_square[0])
           #print("current_letter_index is ", current_letter_index, " and the char there is ", string.ascii_lowercase[current_letter_index])
            current_square[0] = string.ascii_lowercase[current_letter_index + steps]

        #place all the pieces
        print("piece placements: ", piece_placements)
        ranks = piece_placements.split('/')
        for rank_string in ranks:
            for char in rank_string:
                #print("current square {}{} and current char {}".format(current_square[0], current_square[1], char))
                if char.isdigit():
                    #print("skipping forward")
                    move_forward_on_rank(int(char))
                else:
                    #print("writing char")
                    self.board[current_square[0] + str(current_square[1])] = char
                    move_forward_on_rank()
                    
            current_square[1] = current_square[1] - 1
            current_square[0] = 'a'
        
        #active color
        print("active color: ", active_color)
        if active_color == 'w':
            self.side_to_move = "white"
        else:
            self.side_to_move = "black"
            
        #castling rights are either "-" for none, or a list of letters
        print("castling rights: ", castling_rights)
        if castling_rights == "-":
            print("nobody has castling rights")
        else:
            self.black_castle_rights['queenside'] = 'q' in castling_rights
            self.black_castle_rights['kingside'] = 'k' in castling_rights
            self.white_castle_rights['queenside'] = 'Q' in castling_rights
            self.white_castle_rights['kingside'] = 'K' in castling_rights
        
        #ep
        print("en passant square ", en_passant)
        self.en_passant_square = en_passant if en_passant != "-" else ''
        
        #half and full move clocks...
        self.half_move_count = int(half_moves)
        self.move_count = int(full_moves)
    
    #magic methods for treating a board as a dictionary
    def __getitem__(self, key):
        return self.board.get(key, '')
    def __iter__(self):
        return self.board.__iter__()
    def __contains__(self, key):
        return self.board.__contains__(key)
    
    
    def get_piece(self, square):
        piece = self[square]
        if not piece:
            return ''
        else:
            piece_name = Piece.piece_names[piece.lower()]
            color = "white" if piece.is_upper() else "black"
            return Piece(piece_name, square, color, self)
            
    def __repr__(self):
        return self.board.__repr__()
    
    
    
    #checkmates...
    def is_white_checkmate(self):
        return False
    
    def is_black_checkmate(self):
        return False
    
    def is_checkmate(self):
        return self.is_black_checkmate() or self.is_white_checkmate()
    
    #draws
    def is_stalemate(self):
        return False
    def is_forced_draw(self):
        return self.is_stalemate or self.half_move_counter > 50
    
    def is_finished(self):
        return self.is_checkmate() or self.is_forced_draw()
    
    #pieces
    def get_white_pieces(self):
        return {}
    def get_black_pieces(self):
        return {}
    def get_pieces(self):
        return self.get_black_pieces() + self.get_white_pieces()
    
  
        
