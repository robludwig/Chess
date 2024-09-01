'''
Created on Jan 8, 2017

@author: rob
'''
from Evalution.Evaluate import evaluate
from collections import deque 

class Tree(object):
    '''
    classdocs
    '''
    

    def __init__(self, board):
        '''
        Constructor
        '''
        self.board = board
        self.search_queue = deque()
        self.depth = 0
        self.searching = False
        self.root = Node(board, evaluate(board))
        
    def doSearch(self, max_depth=3):
        '''naive bfs'''
        original_moves = self.board.get_moves()
        self.search_queue.extend([{'parent' : self.root, 'depth' : 0, 'move' : move} for move in original_moves])
        self.searching = True
        self.evaluated = 0
        best_move = None
        best_move_eval = -1000
        while self.searching and self.depth < max_depth:
            if len(self.search_queue) == 0:
                self.searching = False
                break
            next_move = self.search_queue.popleft()
            print(next_move)
            current_depth = next_move['depth']
            parent = next_move['parent']
            parent_board = parent.board
            next_board = parent_board.copy()
            next_board.do_move(next_move['move'])
            evaluation = evaluate(next_board)
            next_node = Node(next_board, evaluation)
            parent.add_child(next_node)
            if evaluation > best_move_eval:
                best_move_eval = evaluation
                best_move = next_move['move']
            self.search_queue.extend([{'parent' : next_node, 'depth' : current_depth + 1, 'move' : move} for move in next_board.get_moves()])
            self.evaluated = self.evaluated + 1
            self.depth = max(self.depth, current_depth)
            if self.evaluated % 50 == 0: print(self)
        print(self)
        print(f"finished evaluation: {best_move} @ {best_move_eval}" )
   
   
    def __repr__(self) -> str:
        return f"Search Tree: evaluated {self.evaluated} nodes at depth {self.depth}. Queue:{len(self.search_queue)}"

        
        

            
           
           
class Node(object):
    def __init__(self, board, score):
        self.board = board
        self.score = score
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Node: score:{self.score}, num children: {len(self.children)}"
        
                    
            
        
        
        