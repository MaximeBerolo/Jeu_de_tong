# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 04:46:31 2018

@author: maximeberolo
"""

import Board
import Game
import Player

import copy
import numpy as np

# Creation d'un arbre qui représente les possibilités. Un noeud est un possible
# board

class Node():
    
    def __init__(self, game, name, parent = None):
        
        '''
        parent is a Game.Game() object
        child is a list of Game.Game() objects
        actions is a list of all possible insect to eat
        '''
        
        self.parent = parent
        self.name = name
        self.current_state = game
        self.children = []
        self.value = 0
        self.actions = []
        self.SetActions()
        
    def SetActions(self):
        
        self.actions = list(set(self.current_state.line))
        try:
            self.actions.remove(7)
        except:
            pass
                
        
    def AddChild(self, parent = None):
        
        '''
        Method that adds the children to the node.
        First check if the game is ended (meaning that a player lost)
        If so, then set self.children to None
        Otherwise add the children nodes
        '''
        
        if self.current_state.line.count(7) == self.current_state.board.size:
            self.children = None
            
        else:
        
            for action in self.actions:
                
                possible_game = copy.deepcopy(self.current_state)
                possible_game.EatAndMove(action)
                self.children.append(Node(possible_game, parent.name + str(action), parent))
            
    def SetValue(self, ai_played, depth):
        
        '''
        ai_played : boolean to know if AI or player played
        ai_played : True if ai played
                    False otherwise
        '''
    
        print('Set value', depth)        
        
        if self.current_state.line.count(7) == self.current_state.board.size and not ai_played:
            self.value = -20 + depth
        elif self.current_state.line.count(7) == self.current_state.board.size and ai_played:
            self.value = 20 - depth
        else:
            self.value = 0
            
    def IsLeaf(self):
        
        if self.children == None:
            return True
        
        return False
            
        
        
class Tree():
    
    def __init__(self, game, depth):
        
        '''
        game is the state of the game when the AI is called
        depth is the depth or the tree. The larger the greater the AI is
        '''
        
        self.root = Node(game, 'root')
        
        self.depth = depth
        
        self.CreateTree(self.root, 1)
        
        self.PrintTree(self.root)
        
    def CreateTree(self, node, depth):
        
        if depth <= self.depth+1:
            
            node.AddChild(node)
            node.SetValue(depth%2 == 0, depth-1)
            print(node.name)
            print(node.current_state.board)
            print(node.value)
            print('\n')
            
            if not node.IsLeaf():
                for child in node.children:
                    self.CreateTree(child, depth+1)
                    


        
    def PrintTree(self, node):
        
        if not node.IsLeaf():
            
            for child in node.children:

                self.PrintTree(child)

class MiniMax():
    
    def __init__(self, tree, depth):
        
        self.tree = tree
        self.root = tree.root
        self.depth = depth
        self.current_node = None
        
#        self.AlphaBeta(self.root, 1, -float('Inf'), float('Inf'), True)
        
#    def Minimax(self, node, depth, ai_played):
#        
#        if depth == self.depth+1 or node.IsLeaf():
#
#            return node.value
#            
#        if ai_played:
#            best_value = -float('Inf')
#            for child in node.children:
#                v = self.Minimax(child, depth+1, False)
#                best_value = max(v, best_value)
#            return best_value
#            
#        elif not ai_played:
#            best_value = float('Inf')
#            for child in node.children:
#                v = self.Minimax(child, depth+1, True)
#                best_value = min(v, best_value)
#            return best_value
        
        
#    def BetaAlpha(self, node, depth, alpha, beta, ai_played):
#        
#        if depth == self.depth+1 or node.IsLeaf():
#
#            return node.value
#            
#        if ai_played:
#            v = -float('Inf')
#            for child in node.children:
#                v = self.Minimax(child, depth+1, False)
#                alpha = max(alpha, v)
#                if alpha >= beta:
#                    break
#            print()
#            return v
#            
#        elif not ai_played:
#            v = float('Inf')
#            for child in node.children:
#                v = self.Minimax(child, depth+1, True)
#                beta = min(beta, v)
#                if alpha >= beta:
#                    break
#            return v
        
        
    def AlphaBeta(self, node, depth, alpha, beta, ai_played):
        
        if depth == self.depth+1 or node.IsLeaf():

            return node.value
            
        if ai_played:
            v = -float('Inf')
            for i in range(len(node.children)):
                child = node.children[i]
                inter = self.AlphaBeta(child, depth+1, alpha, beta, False)
                if inter > v:
                    v = inter
                    print('Move Maxi')
                    print(node.actions)
                    print(node.actions[i])

                alpha = max(alpha, v)
                
                if alpha >= beta:
                    break
            return v
            
        elif not ai_played:
            v = float('Inf')
            for i in range(len(node.children)):
                child = node.children[i]
                inter = self.AlphaBeta(child, depth+1, alpha, beta, True)
                
                if inter < v:
                    v = inter
                    print('Move mini')
                    print(node.actions[i])
                    
                beta = min(beta, v)
                if alpha >= beta:
                    break
            return v
            
    def GetBestMove(self):
        
        best_move_value = -float('Inf')
        move = 0
        
        for action in self.root.actions:
            
            move_value = self.AlphaBeta(self.root, self.depth, -float('Inf'), float('Inf'), True)
            
            if move_value > best_move_value:
                move = action
        
        return move
            
            
        
            
            
        
                

                

            
            
        
if __name__ == "__main__":
    
    board_test = np.array([[0,0,0,0,0,0], [0,1,7,3,4,0], [0,2,7,1,3,0], [0,4,7,4,1,0], [0,1,7,2,2,0], [0,0,0,0,0,0]])
    board = Board.Board(4)
    board.board = board_test

    Player1 = Player.Player('Max')
    Player2 = Player.Player('Cam')

    Game1 = Game.Game([Player1, Player2])
    
    tree = Tree(Game1, 3) 
    
    AI = MiniMax(tree, 3)
            
        
        
    
    