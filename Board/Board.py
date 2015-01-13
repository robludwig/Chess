'''
Created on Dec 6, 2014

@author: Robert
'''

import string
from copy import deepcopy

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
    
    def copy(self):
        return deepcopy(self)
    
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
    
    
    def get_piece_on_square(self, square):
        piece = self[square]
        if not piece:
            return ''
        else:
            piece_name = Piece.piece_names[piece.lower()]
            color = "white" if piece.isupper() else "black"
            return Piece(piece_name, square, color, self)
                
    def get_piece_square(self, piece):
        for key in self.board.keys():
            if self.board[key] == piece:
                return key
        return ''
            
    def __repr__(self):
        return self.board.__repr__()
    
    
    
    #checks and checkmates...
    def is_white_check(self):
        white_king_square = self.get_piece_square('K')
        return white_king_square in self.get_black_attacked_squares()
    
    def is_white_checkmate(self):
        return self.is_white_check() and self.get_white_moves() == []
    
    def is_black_check(self):
        black_king_square = self.get_piece_square('k')
        return black_king_square in self.get_white_attacked_squares()
    
    def is_black_checkmate(self):
        return self.is_black_check() and self.get_black_moves() == []
    
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
        return [self.get_piece_on_square(square) for square in self.board.keys() if self[square].isupper()]
    def get_black_pieces(self):
        return [self.get_piece_on_square(square) for square in self.board.keys() if self[square].islower()]
    def get_pieces(self):
        return [self.get_piece_on_square(square) for square in self.board.keys()]
    
    #moves
    def get_white_moves(self):
        moves = []
        for piece in self.get_white_pieces():
            moves.extend(piece.get_moves())
        return moves
    def get_black_moves(self):
        moves = []
        for piece in self.get_black_moves():
            moves.extend(piece.get_moves())
        return moves
    
    #attacked squares
    def get_white_attacked_squares(self):
        squares = []
        for piece in self.get_white_pieces():
            squares.extend(piece.get_attacked_squares())
        return squares
    
    def get_black_attacked_squares(self):
        squares = []
        for piece in self.get_black_pieces():
            squares.extend(piece.get_attacked_squares())
        return squares
    
    def do_move(self, move):
        '''
        naively moves a piece from the provided origin to the destination
        does not check for e.g. validity, checkmates, etc.
        deletes the piece at the original square and overwrites the destination with the new piece
        it is advisable to call board.is_finished() after this to see if the game is complete
        '''
        original_piece = self.board[move.origin]    
        del self.board[move.origin]
        if move.en_passant:
            self.en_passant_square = move.en_passant
        else:
            self.en_passant_square = ''
                        
        capture = self.board[move.destination] 
        
        #write in the new piece if it's a promotion, or the original piece otherwise
        if move.castle:
            #move the king
            self.board[move.destination] = original_piece
            
            #move the correct rook
            if move.castle == 'kingside':
                rook_file = 'h'
                target_file = 'f'
            else:
                rook_file = 'a'
                target_file = 'd'
            if self.side_to_move == 'white':
                rook_rank = 1
            else:
                rook_rank = 8
            rook_location = rook_file + str(rook_rank)
            rook_target = target_file + str(rook_rank)
            self.board[rook_target] = self.board[rook_location]
            del self.board[rook_location]
        elif not move.promotion:
            self.board[move.destination] = original_piece
        else:
            promotion = move.promotion
            if self.side_to_move == 'white':
                promotion = promotion.toupper()
            self.board[move.destination] = promotion
        
        #housekeeping    
        self.side_to_move = "white" if self.side_to_move == "black" else "black"
        self.move_count += 1
        #remove castling rights if necessary
        if original_piece in 'kKrR':
            if original_piece == 'k':
                self.black_castle_rights = {}
            if original_piece == 'K':
                self.black_castle_rights = {}
            else:
                if move.origin == 'a1':
                    self.white_castle_rights['queenside'] = False
                elif move.origin == 'h1':
                    self.white_castle_rights['kingside'] = False
                elif move.origin == 'a8':
                    self.black_castle_rights['queenside'] = False
                else:
                    self.black_castle_rights['kingside'] = False
            
        #reset the half-ply counter if capture or pawn move
        if capture or original_piece.tolower == Piece.PAWN:
            self.half_move_count = 0
        else:
            self.half_move_count += 1
        return
        
