'''
Created on Jan 10, 2015
Move functions for pieces
@author: Robert
'''
from .Move import Move
from .Utils import on_board, move_file, northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal
from .Utils import down_file, up_file, east_rank, west_rank

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
    for direction in [down_file, up_file, east_rank, west_rank]:
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
def queen_moves(self):
    moves = bishop_moves(self) + rook_moves(self)
    return moves
def king_moves(self):
    moves = [] 
    
    #single moves
    directions = [down_file, up_file, east_rank, west_rank, northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal]
    possible_squares = [direction(self.square) for direction in directions if on_board(direction(self.square)) and not self.board[direction(self.square)]]
    for square in possible_squares:
        test_board = self.board.copy()
        possible_move = Move(self.square, square)
        test_board.do_move(possible_move)
        if self.color == 'white':
            if not test_board.is_white_check():
                moves.append(possible_move)
        else:
            if not test_board.is_black_check():
                moves.append(possible_move)
    #castling
    if self.color == 'white':
        if not self.board.is_white_check():
            if self.board.white_castle_rights['kingside']:
                #check the possible squares
                for intervening_square in ['g1', 'f1']:
                    if not self.board[intervening_square] and intervening_square not in self.board.get_black_attacked_squares():
                        moves.append(self.square, 'g1', castling='kingside')
            if self.board.white_castle_rights['queenside']:
                #check the possible squares
                if not self.board['b1']:
                    for intervening_square in ['d1', 'c1']:
                        if not self.board[intervening_square] and intervening_square not in self.board.get_black_attacked_squares():
                            moves.append(self.square, 'c1', castling='queenside')
    if self.color == 'black':
        if not self.board.is_black_check():
            if self.board.check_castle_rights['kingside']:
                #check the possible squares
                for intervening_square in ['g8', 'f8']:
                    if not self.board[intervening_square] and intervening_square not in self.board.get_white_attacked_squares():
                        moves.append(self.square, 'g8', castling='kingside')
            if self.board.white_castle_rights['queenside']:
                #check the possible squares
                if not self.board['b8']:
                    for intervening_square in ['d8', 'c8']:
                        if not self.board[intervening_square] and intervening_square not in self.board.get_white_attacked_squares():
                            moves.append(self.square, 'c8', castling='queenside')
        
    return moves
