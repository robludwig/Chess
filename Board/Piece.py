'''
Created on Dec 6, 2014

@author: Robert
'''

import string
from .Move import Move
from .Utils import on_board, move_file, northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal
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
        self.file = self.square[0]
        self.rank = int(self.square[1])
        
    
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
        first_move = False
        
        #file in front is the file one step forward
        if self.color == 'white':
            rank_in_front = str(self.rank + 1)
            if self.rank == 2:
                first_move = self.file + str(self.rank + 2)
            promotion_rank = 8
        else:
            rank_in_front = str(self.rank - 1)
            if self.rank == 7:
                first_move = self.file + str(self.rank - 2)
            promotion_rank = 1
            
        #pawn can only move forward if unoccupied    
        square_in_front = self.file + rank_in_front
        if not self.board[square_in_front]:
            if rank_in_front == promotion_rank:
                for piece in ['q', 'r', 'n', 'b']:
                    moves.append(Move(self.square), square_in_front, False, piece)                    
            else:
                moves.append(Move(self.square, square_in_front))
        if first_move and not self.board[first_move] and not self.board[square_in_front]:
            moves.append(Move(self.square, first_move, True))
            
        #pawn can only move to attacking squares if occupied...
        neighboring_files = (move_file(self.file, 1), move_file(self.file, -1 ))
        attackable_squares = (neighboring_files[0] + rank_in_front, neighboring_files[1] + rank_in_front)
        for square in attackable_squares:
            piece_on_square = self.board.get_piece_on_square(square)
            if piece_on_square and piece_on_square != self.color:
                moves.append(Move(self.square, square))
            elif self.board.en_passant_square == square:
                moves.append(Move(self.square, square))
        return moves
    
    
    def knight_moves(self):
        moves = []
        for rank in [self.rank + 2, self.rank - 2]:
            for file in [move_file(self.file, -1), move_file(self.file, 1)]:
                target_square = file + str(rank)
                #print("checking target_square", target_square)
                if on_board(target_square) and (not self.board[target_square] or self.board.get_piece_on_square(target_square).color != self.color):
                     moves.append(Move(self.square, target_square))
                     
        for rank in [self.rank + 1, self.rank - 1]:
            for file in [move_file(self.file, -2), move_file(self.file, 2)]:
                target_square = file + str(rank)
                #print("checking target_square", target_square)
                if on_board(target_square) and (not self.board[target_square] or self.board.get_piece_on_square(target_square).color != self.color):
                     moves.append(Move(self.square, target_square))
        return moves
    
    def bishop_moves(self):
        moves = []
        for direction in [northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal]:
            obstructed = False
            current_square = self.square
            while not obstructed:
                target_square = direction(current_square)
                if not on_board(target_square):
                    break
                if self.board[target_square]:
                    obstructed = True
                    piece = self.board.get_piece_on_square(target_square)
                    if piece.color != self.color:
                        moves.append(Move(self.square, target_square))
                else:
                    moves.append(Move(self.square, target_square))
                    current_square = target_square                 
        return moves
    def rook_moves(self):
        moves = []
        return moves
    def queen_moves(self):
        moves = self.bishop_moves() + self.rook_moves()
        return moves
    def king_moves(self):
        moves = []
        return moves
    
    def __repr__(self):
        return "{} {} located on {}".format(self.color, self.piece, self.square)
        