# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 10:18:11 2018

@author: maximeberolo
"""

import sys
import ast
from functools import partial
from operator import itemgetter
import time

from PyQt4 import QtGui, QtCore, QtTest
import Game
import Player
import AI

insect_pictures = ["araignees.gif", "papillons.gif", "chenilles.gif", "mouches.gif"]
difficulties = ['Easy', 'Medium', 'Hard']

def BorderOfRectangle(size):
    lst = []   
    
    for j in range(1,size-1):
        lst.append([1, j+1])
        lst.append([size, j+1])
        lst.append([j+1, 1])
        lst.append([j+1, size])
        
    lst = sorted(lst, key=itemgetter(0))
        
    return lst
        
    
class Window(QtGui.QMainWindow):
    
    def __init__(self):
        
        super(Window, self).__init__()
        
        self.setGeometry(50, 50, 1500, 1000)
        self.setWindowTitle("Jeu de Tong")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        self.nb_players = 0
        self.players = []
        self.board_size = 0
        self.who_played = 0
        
        self.save = self.GetSave()
        
        
        # Block the game until the player clicks a white tile and put the cameleon at the beginning of the game
        self.play = False
        # Check if the size of the new board is the same or not
        self.new_size = False
        
        
        
        self.NewGame()
        
        self.lst_button = [0]*((self.board_size+2)**2)
        
        self.Initialization()
        
    @property
    def players(self):
        return self.__players
        
    @players.setter
    def players(self, players):
        self.__players = players
        
    def GetSave(self):
        
        save = {}
        
        with open('ranking.txt', 'r') as f:
            
            for line in f.readlines():
                save = ast.literal_eval(line)
        
        return save
        
    def ResetInstanceVariable(self):
        
        self.players = []
        self.who_played = 0
        self.play = False
        
        
    def NewGame(self):
        
        self.ResetInstanceVariable()
        
        ##################
        # Player related #
        ##################
        
        # Define the number of players
        text, ok = QtGui.QInputDialog.getText(self, "Text Input Dialog", "Enter the number of players")
    		
        if ok:
            self.nb_players = int(text)
        
        # Enter the name of the players    
        for i in range(self.nb_players):
            box = QtGui.QInputDialog(self)
            
            text, ok = box.getText(self, "Text Input Dialog", "Enter player %d's name:" %(i+1))
            
            if ok:
                self.players.append(Player.Player(str(text)))
                
        # If only one player, need to create an AI player
        if self.nb_players == 1:
                
            item, ok = QtGui.QInputDialog.getItem(self, "Initialization", 
                                          "Select the difficulty of the AI", tuple(difficulties), 0, False)
                                          
            self.players.append(Player.ArtificalIntelligence('AI ' + str(item), difficulties.index(str(item)) + 1))
            
        
        ################
        # Game related #
        ################
            
        item, ok = QtGui.QInputDialog.getItem(self, "Initialization", 
                                              "Choose the size of the board", ('4','6', '8'), 0, False)
                                              
        if ok and item:
            if int(item) != self.board_size:
                self.new_size = True
            else:
                self.new_size = False
            self.board_size = int(item)
            
            
    def PutCameleon(self, btn, i, j):
        if not self.play :
            btn.setIcon(QtGui.QIcon("Cameleon.gif"))
            btn.setIconSize(QtCore.QSize(100,100))
            self.game.board.UpdatePosition([i,j], self.game.pos)
            self.game.pos = [i,j]
            self.play = True       
            
            self.textbox.setText(self.players[self.who_played%len(self.players)].name + ' choose the insect to eat')
        
    def Initialization(self):
        
        self.game = Game.Game(self.players, self.board_size)
        
        print(self.game.board)
        
        for i in range(self.board_size+2):
            for j in range(self.board_size+2):
                
                value = self.game.board.GetElement([i,j])
                
                if value not in [0,7,9] :
                    
                    btn = QtGui.QPushButton('', self)
                    btn.resize(100,100)
                    btn.move(j*100,i*100)
                    self.lst_button[(self.board_size+2)*i+j] = btn
                
                    btn.setIcon(QtGui.QIcon(insect_pictures[value-1]))
                    btn.setIconSize(QtCore.QSize(100,100))
                    btn.clicked.connect(partial(self.SelectedInsect, value))
                    
                else:
                    
                    btn = QtGui.QPushButton('', self)
                    btn.resize(100,100)
                    btn.move(j*100,i*100)
                    self.lst_button[(self.board_size+2)*i+j] = btn
                    
                    btn.setIcon(QtGui.QIcon("white.png"))
                    btn.setIconSize(QtCore.QSize(90,90))
                    
                    if [i,j] not in [[0,0], [0,self.board_size+1], [self.board_size+1, 0], [self.board_size+1, self.board_size+1]]:
                        btn.clicked.connect(partial(self.PutCameleon, btn, i, j))
                    
        self.textbox = QtGui.QLineEdit(self)
        self.textbox.move((self.board_size+3)*100, 20)
        self.textbox.resize(500,40)
        self.textbox.setText(self.players[0].name + ' choose the initial position of the cameleon. Click any white tile.')
        
        self.textbox_rank = QtGui.QPlainTextEdit(self)
        self.textbox_rank.move((self.board_size+3)*100, 150)
        self.textbox_rank.resize(500, 300)
        self.textbox_rank.insertPlainText('RANKINGS\nName\tScore\n----------------------------\n\n')
        
        self.ShowRanking()
                        
        self.show()
        
    def UpdateBoard(self):
        
        print('UpdateBoard')
        print(self.game.board)
        
        for i in range(self.board_size+2):
            for j in range(self.board_size+2):
                
                value = self.game.board.GetElement([i,j])
                
                if value == 7:
                    
                    self.lst_button[(self.board_size+2)*i+j].setIcon(QtGui.QIcon('Arriere.gif'))
                    
                elif value == 0:
                    
                    self.lst_button[(self.board_size+2)*i+j].setIcon(QtGui.QIcon('white.png'))
                    self.lst_button[(self.board_size+2)*i+j].setIconSize(QtCore.QSize(90,90))
                    
                elif value == 9: 
                    
                    self.lst_button[(self.board_size+2)*i+j].setIcon(QtGui.QIcon('Cameleon.gif'))
                    self.lst_button[(self.board_size+2)*i+j].setIconSize(QtCore.QSize(100,100)) 

                    
    def UpdateRestart(self):

        if self.new_size:
            
            self.textbox.move((self.board_size+3)*100, 20)
            self.textbox_rank.move((self.board_size+3)*100, 150)
            
            for btn in self.lst_button:
                btn.deleteLater()
            
            self.lst_button = [0]*((self.board_size+2)**2)
            
            for i in range(self.board_size+2):
                for j in range(self.board_size+2):
                    
                    value = self.game.board.GetElement([i,j])
                    
                    if value not in [0,7,9] :
                        
                        btn = QtGui.QPushButton('', self)
                        btn.resize(100,100)
                        btn.move(j*100,i*100)
                        self.lst_button[(self.board_size+2)*i+j] = btn
                    
                        btn.setIcon(QtGui.QIcon(insect_pictures[value-1]))
                        btn.setIconSize(QtCore.QSize(100,100))
                        btn.clicked.connect(partial(self.SelectedInsect, value))
                        
                        btn.show()
                        
                    else:
                        
                        btn = QtGui.QPushButton('', self)
                        btn.resize(100,100)
                        btn.move(j*100,i*100)
                        self.lst_button[(self.board_size+2)*i+j] = btn
                        
                        btn.setIcon(QtGui.QIcon("white.png"))
                        btn.setIconSize(QtCore.QSize(90,90))
                        btn.clicked.connect(partial(self.PutCameleon, btn, i, j))
                        
                        btn.show()

            
        elif not self.new_size:
            
            for i in range(self.board_size+2):
                for j in range(self.board_size+2):
                    
                    value = self.game.board.GetElement([i,j])
                    
                    if value not in [0,7,9] :
                        
                        self.lst_button[(self.board_size+2)*i+j].clicked.disconnect()
                        self.lst_button[(self.board_size+2)*i+j].clicked.connect(partial(self.SelectedInsect, value))
                        
                        self.lst_button[(self.board_size+2)*i+j].setIcon(QtGui.QIcon(insect_pictures[value-1]))
                        self.lst_button[(self.board_size+2)*i+j].setIconSize(QtCore.QSize(100,100))
                        
                    else:
                        
                        self.lst_button[(self.board_size+2)*i+j].setIcon(QtGui.QIcon("white.png"))
                        self.lst_button[(self.board_size+2)*i+j].setIconSize(QtCore.QSize(90,90))
                        
        
    def SelectedInsect(self, value):
        
        if self.play:
            
            self.who_played += 1
            
            self.textbox.setText(self.players[self.who_played%len(self.players)].name + ' chooses an insect to eat')
            
            self.game.EatAndMove(value)
            self.UpdateBoard()
            
            if self.IsLost():
                self.Restart()
                
            if self.nb_players == 1:

                self.textbox.setText(self.players[self.who_played%(self.nb_players+1)].name + ' chooses an insect to eat')
                
                QtTest.QTest.qWait(1000)
                
                value = self.AiPlays()
                
                self.game.EatAndMove(value)
                self.UpdateBoard()

                self.textbox.setText(self.players[self.who_played%(self.nb_players+1)].name + ' ate ' + insect_pictures[value-1][:-3])
                
                self.who_played += 1
                
                if self.IsLost():
                    self.Restart()     
                    
                    
    def AiPlays(self):
        print('AiPlays()')
        print(self.who_played, len(self.players), self.who_played%len(self.players))
        tree = Player.Tree(self.game, self.players[self.who_played%len(self.players)].depth)
        print('Tree created')
        self.players[self.who_played%len(self.players)].SetTree(tree)
        print('Value calculating')
        value = self.players[self.who_played%len(self.players)].GetBestMove()
        
        return value
        
    def Restart(self):
        
        self.textbox_res = QtGui.QLineEdit(self)
        self.textbox_res.move((self.board_size+3)*100 + 50, 70)
        self.textbox_res.resize(150,40)
        self.textbox_res.setText(self.players[(self.who_played)%len(self.players)].name + ' lost !')   
        self.SaveResults(self.players[(self.who_played-1)%len(self.players)].name)
        self.ShowRanking()
        self.textbox_res.show()
        
        item, ok = QtGui.QInputDialog.getItem(self, 'Restart', 
                                      'Do you want to start again ?', ('Yes','No'), 0, False)
                                      
        if item == 'Yes':
            
            self.NewGame()
            self.game = Game.Game(self.players, self.board_size)
            self.textbox_res.hide()
            self.textbox.setText('Please choose the initial position of the cameleon. Click any white tile.')                    
            self.UpdateRestart()
            
        elif item == 'No':
            self.WriteResults()
            sys.exit()
            
    def IsLost(self):
        
        if self.game.line.count(7) == self.board_size:
                return True
        
    def ChangeIcon(self, btn):
        btn.setIcon(QtGui.QIcon("Arriere.gif"))
        
    def SaveResults(self, winner):
        
        if winner not in self.save:
            self.save[winner] = 1
        else:
            self.save[winner] += 1
            
    def WriteResults(self):
        
        with open('ranking.txt', 'w') as f:
            
            f.write(str(self.save))
                
    def ShowRanking(self):
        
        self.textbox_rank.clear()
        
        save_sorted = sorted(self.save.items(), key = itemgetter(1), reverse = True)
        
        save_str = 'RANKINGS\nName\tScore\n----------------------------\n\n'
        
        for player_score in save_sorted:
            save_str += player_score[0] + '\t' + str(player_score[1]) + '\n'
        
        self.textbox_rank.insertPlainText(save_str)
            
            

        
        

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    
#    Player1 = Player.Player('player1')
#    Player2 = Player.Player('player2')
    run()

    