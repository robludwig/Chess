'''
Created on Dec 6, 2014

@author: Robert
'''

from .PieceMoves import bishop_moves, pawn_moves, knight_moves, king_moves, rook_moves, queen_moves
from .PieceAttacks import bishop_attacks, pawn_attacks, knight_attacks, king_attacks, rook_attacks, queen_attacks

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
        self.move_function = {                   
          Piece.PAWN  : pawn_moves,
          Piece.BISHOP: bishop_moves,
          Piece.QUEEN : queen_moves,
          Piece.KING  : king_moves,
          Piece.ROOK  : rook_moves,
          Piece.KNIGHT: knight_moves  
         }[self.piece]
         
        self.attack_functions = {                               
          Piece.PAWN  : pawn_attacks,
          Piece.BISHOP: bishop_attacks,
          Piece.QUEEN : queen_attacks,
          Piece.KING  : king_attacks,
          Piece.ROOK  : rook_attacks,
          Piece.KNIGHT: knight_attacks         
         }[self.piece]
         
        self.file = self.square[0]
        self.rank = int(self.square[1])
        
    
    def get_moves(self):
        return self.move_function(self)
    
    def get_attacked_squares(self):
        return self.attack_functions(self)
    
    def get_base_value(self):
        return {
                      
                      Piece.PAWN  : 1,
                      Piece.BISHOP: 3,
                      Piece.QUEEN : 9,
                      Piece.KING  : 10000,
                      Piece.ROOK  : 5,
                      Piece.KNIGHT: 3
                  
         }[self.piece]
    
    
    def __repr__(self):
        return "{} {} located on {}".format(self.color, self.piece, self.square)
        