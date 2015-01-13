'''
Created on Dec 6, 2014

@author: Robert
'''

class BoardException(Exception):
    '''
    Illegal board state.
    '''


    def __init__(self, message):
        '''
        Constructor
        '''
        self.message = message