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
                      
                      Piece.PAWN  : self.pawn_moves,
                      Piece.BISHOP: self.bishop_moves,
                      Piece.QUEEN : self.queen_moves,
                      Piece.KING  : self.king_moves,
                      Piece.ROOK  : self.rook_moves,
                      Piece.KNIGHT: self.knight_moves
                  
         }[self.piece]
        
    
    def get_moves(self):
        return self.move_function()
    
    def get_base_value(self):
        return {
                      
                      Piece.PAWN  : 1,
                      Piece.BISHOP: 3,
                      Piece.QUEEN : 9,
                      Piece.KING  : 10000,
                      Piece.ROOK  : 5,
                      Piece.KNIGHT: 3
                  
         }[self.piece]
    
    def pawn_moves(self):
        moves = []
        file = self.square[0]
        rank = int(self.square[1])
        first_move = False
        
        #file in front is the file one step forward
        if self.color == 'white':
            rank_in_front = str(rank + 1)
            if rank == 2:
                first_move = file + str(rank + 2)
        else:
            rank_in_front = str(rank - 1)
            if rank == 7:
                first_move = file + str(rank - 2)
            
            
        #pawn can only move forward if unoccupied    
        square_in_front = file + rank_in_front
        if not self.board[square_in_front]:
            moves.append(square_in_front)
        if first_move and not self.board[first_move]:
            moves.append(first_move)
            
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
        