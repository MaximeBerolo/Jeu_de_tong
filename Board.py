# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 11:22:54 2018

@author: maximeberolo
"""

import numpy as np
import random

class Board():
    
    def __init__(self, size):
        
        self.size = size
        self.board = self.GenerateBoard()
        
    def __repr__(self):
        print(self.board)
        return "done"
        
    def GetElement(self, index):
        return int(self.board[index[0], index[1]])
        
    def GenerateBoard(self):
        
        generated_board = np.zeros((self.size+2, self.size+2))

        count = 0
                
        while count != self.size**2:
            
            color = int(random.randint(1,4))
            if np.count_nonzero(generated_board == color) < self.size**2/4:
                generated_board[(count // (self.size)) + 1, count%(self.size) +1] = color
            else:
                color_prev = color
                while color == color_prev:
                    color = random.randint(1,4)
                generated_board[(count // (self.size)) + 1, count%(self.size) +1] = color
            
            count += 1
        
#        generated_board = np.array([[0,0,0,0,0,0], [0,1,3,7,7,0], [0,7,2,1,7,0], [0,7,7,7,7,0], [0,2,7,7,7,0], [0,9,0,0,0,0]])
        
        return generated_board
        
    def UpdatePosition(self, current_pos, prev_pos = 0):
        
        try:
            self.board[prev_pos[0], prev_pos[1]] = 0
        except:
            pass
        self.board[current_pos[0], current_pos[1]] = 9
        
        
    def UpdateLineColumn(self, choice, pos):
        
        if pos[1] == 0 or pos[1] == self.size + 1:
            for i in range(len(self.board[pos[0], :])):
                if self.board[pos[0], :][i] == choice:
                    self.board[pos[0], :][i] = 7
                    
        elif pos[0] == 0 or pos[0] == self.size + 1:
            for j in range(len(self.board[:, pos[1]])):
                if self.board[:, pos[1]][j] == choice:
                    self.board[:, pos[1]][j] = 7
        
        
    def ReturnLine(self, rank):
        
        return [int(x) for x in self.board[rank,1:self.size+1]]
        
    def ReturnColumn(self, rank):
        
        return [int(x) for x in self.board[1:self.size+1, rank]]
        

if __name__ == "__main__":
    
    size = 4
    ## if size*size % 4 != 0 then not ok   
    
    Board1 = Board(size)
#    print(Board1.board)
#    
#    Board1.UpdateLineColumn(3, [0,3])
#    print(Board1.board)
    
    print(Board1.GetElement([2,1]))
    
#    print(type(Board1.ReturnLine(2)))
#    print(Board1.ReturnLine(2))
#    Board1.UpdatePosition([1,0])
#    print(Board1.board)
#    Board1.UpdatePosition([3,0], [1,0])
#    print(Board1.board)