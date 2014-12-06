'''
Created on Dec 6, 2014

@author: Robert
'''

import string

class Piece:
    '''
    Represents a piece on the board 
    '''
    PAWN = "pawn"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"
    
    move_functions = {
                      
                      PAWN  : pawn_moves,
                      BISHOP: bishop_moves,
                      QUEEN : queen_moves,
                      KING  : king_moves,
                      ROOK  : rook_moves,
                      KNIGHT: knight_moves
                  
                      }
    
    piece_names = {
                   
                   'p' : PAWN,
                   'b' : BISHOP,
                   'n' : KNIGHT,
                   'r' : ROOK,
                   'q' : QUEEN,
                   'k' : KING                             
                   }
    

    def __init__(self, piece, square, color, board):
        '''
        Constructor
        '''
        self.piece = piece
        self.square = square
        self.color = color
        self.board = board
        self.moves = self.move_functions(self.piece)
        
    
    def pawn_moves(self):
        moves = []
        file = self.square[0]
        
        #file in front is the file one step forward
        if self.color == 'white':
            rank_in_front = str(int(self.square[1]) + 1)
        else:
            rank_in_front = str(int(self.square[1]) - 1)
            
        #pawn can only move forward if unoccupied    
        square_in_front = file + rank_in_front
        if not self.board[square_in_front]:
            moves.append(square_in_front)
            
        #pawn can only move to attacking squares if occupied...
        file_index = string.ascii_lowercase.find(file)
        neighboring_files = (string.ascii_lowercase[file_index + 1], string.ascii_lowercase[file_index - 1])
        attackable_squares = (neighboring_files[0] + rank_in_front, neighboring_files[1] + rank_in_front)
        for square in attackable_squares:
            piece_on_square = self.board.get_piece(square)
            if piece_on_square and piece_on_square != self.color:
                moves.append(square)
            elif self.board.en_passant_square == square:
                moves.append(square)
        return moves
    
    
    def knight_moves(self):
        moves = []
        return moves
    def bishop_moves(self):
        moves = []
        return moves
    def rook_moves(self):
        moves = []
        return moves
    def queen_moves(self):
        moves = []
        return moves
    def king_moves(self):
        moves = []
        return moves
    
    def __repr__(self):
        return "{} {} located on {}".format(self.color, self.piece, self.square)
        