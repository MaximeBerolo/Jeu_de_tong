# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:49:23 2018

@author: maximeberolo
"""

import random

import Board
import Player

class Game():
    
    def __init__(self, players, size_board = 4, initial_pos = [0,1], previous_pos = [0,0]):
        
        '''
        players : list of the players
        size_board : size of the board
        line : line or column in front of the cameleon
        pos : current position of the cameleon
        '''
        
        self.board = Board.Board(size_board)
#        self.player1 = players[0]
#        self.player2 = players[1]
        self.players = players
        self.nb_players = len(self.players)
        self.pos = initial_pos
        self.prev_pos = previous_pos
        self.GetLine()

        self.board.UpdatePosition(self.pos)
    
    @property
    def pos(self):
        return self.__pos
        
    @pos.setter
    def pos(self, pos):
        self.__pos = pos
        
    @property
    def prev_pos(self):
        return self.__prev_pos
    
    @prev_pos.setter
    def prev_pos(self, prev_pos):
        self.__prev_pos = prev_pos
        
    @property
    def line(self):
        return self.__line
    
    @line.setter
    def line(self, line):
        self.__line = line
            
    def UpdatePos(self, move):
         
        if self.pos[0] == 0:
            if self.pos[1] + move <= self.board.size:
                self.pos = [self.pos[0] , self.pos[1] + move]
            else:
                self.pos = [move - (self.board.size - self.pos[1]), self.board.size+1]
        

        elif self.pos[0] == self.board.size+1:
            if self.pos[1] - move >= 1:
                self.pos = [self.pos[0], self.pos[1] - move]
            else:
                self.pos = [self.board.size - (move - self.pos[1])%self.board.size, 0]

        elif self.pos[1] == 0:
            if self.pos[0] - move >= 1:
                self.pos = [self.pos[0] - move, 0]
            else:
                self.pos = [0, 1 + abs(self.pos[0]-move)]
                
        elif self.pos[1] == self.board.size+1:
            if self.pos[0] + move <= self.board.size:
                self.pos= [self.pos[0] + move, self.board.size+1]
            else:
                self.pos = [self.board.size+1, (self.board.size + 1) - (move - (self.board.size - self.pos[0]))]
        
        
    def GetLine(self):

        if self.pos[1] == 0 or self.pos[1] == self.board.size + 1:
            self.line = self.board.ReturnLine(self.pos[0])
            
        elif self.pos[0] == 0 or self.pos[0] == self.board.size + 1:
            self.line = self.board.ReturnColumn(self.pos[1])

            
    def EatAndMove(self, choice):
        
        move = self.line.count(choice)
        self.board.UpdateLineColumn(choice, self.pos)
        self.prev_pos = self.pos
        self.UpdatePos(move)
        self.board.UpdatePosition(self.pos, self.prev_pos)
        self.GetLine()
        
    def Play(self):
        
        rand = random.randint(0,self.nb_players-1)
        
        lost = False
        while not lost:
            print(self.board)
            print(self.line)
            choice = self.players[rand%self.nb_players].Choice()
            self.EatAndMove(choice)
            if self.line.count(7) == self.board.size:
                print('Vous avez perdu !')
                lost = True
            
if __name__ == "__main__":
    
    Player1 = Player.Player()
    Player2 = Player.Player()

    Game1 = Game([Player1, Player2])

    Game1.Play()
#    print(Game1.GetLine())
#    print(Game1.pos)
#    Game1.UpdatePos(6)
#    print(Game1.pos)
            
            
            
            

        
    