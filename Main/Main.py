'''
Created on Dec 6, 2014

@author: Robert
'''

from Board import Board, Utils
from Evalution.Evaluate import evaluate
from Tree import Tree


if __name__ == '__main__':
    board = Board.Board()
    print("all squares:", Utils.all_squares)
    board.reset_to_starting_position()
    print(board)
    print(board.get_white_pieces())
    print(sum([piece.get_base_value() for piece in board.get_black_pieces()]))
    print("available moves: ", board.get_white_moves())
    print("white attacked squares: ", board.get_white_attacked_squares())
    print("black attacked squares: ", board.get_black_attacked_squares())
    print(evaluate(board))
    game_tree = Tree.Tree(board)
    game_tree.doSearch()
    