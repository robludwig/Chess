'''
Created on Dec 7, 2014

@author: Robert
'''

class Move():
    '''
    Represents a move, which is a transformation to the board state.
    '''


    def __init__(self, origin, destination, en_passant=False, promotion='', castle=False):
        '''
        Constructor
        '''
        self.origin = origin
        self.destination = destination
        self.en_passant = en_passant
        self.promotion = promotion
        self.castle = castle
        
    def __repr__(self):
        if self.castle:
            return 'O-O' if self.castle == 'kingside' else 'O-O-O'
        promotion_suffix = '=' + self.promotion if self.promotion else ''
        return self.origin + self.destination + promotion_suffix
        