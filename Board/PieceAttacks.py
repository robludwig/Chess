'''
Created on Jan 10, 2015
Piece attack functions
@author: Robert
'''

from .Utils import on_board, move_file, northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal
from .Utils import down_file, up_file, east_rank, west_rank

def pawn_attacks(pawn):
    if pawn.color == 'white':
        rank_in_front = str(pawn.rank + 1)
    else:
        rank_in_front = str(pawn.rank - 1)
    neighboring_files = (move_file(pawn.file, 1), move_file(pawn.file, -1 ))
    return [square for square in (neighboring_files[0] + rank_in_front, neighboring_files[1] + rank_in_front) 
            if(on_board(square))]

def rook_attacks(rook):
    attacked_squares = []
    for direction in [down_file, up_file, east_rank, west_rank]:
        obstructed = False
        current_square = rook.square
        while not obstructed:
            target_square = direction(current_square)
            if not on_board(target_square):
                break
            if rook.board[target_square]:
                obstructed = True
                attacked_squares.append(target_square)
            else:
                attacked_squares.append(target_square)
                current_square = target_square                 
    return attacked_squares

def queen_attacks(queen):
    return rook_attacks(queen) + bishop_attacks(queen)

def king_attacks(king):
    directions = [down_file, up_file, east_rank, west_rank, northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal]
    return [direction(king.square) for direction in directions if on_board(direction(king.square))]

def bishop_attacks(bishop):
    squares = []
    for direction in [northeast_diagonal, northwest_diagonal, southeast_diagonal, southwest_diagonal]:
        obstructed = False
        current_square = bishop.square
        while not obstructed:
            target_square = direction(current_square)
            if not on_board(target_square):
                break
            if bishop.board[target_square]:
                obstructed = True
                squares.append(target_square)
            else:
                squares.append(target_square)
                current_square = target_square                 
    return squares

def knight_attacks(knight):
    squares = []
    for rank in [knight.rank + 2, knight.rank - 2]:
        for file in [move_file(knight.file, -1), move_file(knight.file, 1)]:
            target_square = file + str(rank)
            #print("checking target_square", target_square)
            if on_board(target_square):
                 squares.append(target_square)
                 
    for rank in [knight.rank + 1, knight.rank - 1]:
        for file in [move_file(knight.file, -2), move_file(knight.file, 2)]:
            target_square = file + str(rank)
            #print("checking target_square", target_square)
            if on_board(target_square):
                 squares.append(target_square)
    return squares