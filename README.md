# Jeu_de_tong

Welcome to Jeu de Tong. This is a personnal project that I did to train myself to use PyQt and code some artificial intelligence.

# Prerequisites :

Python 2.x <br>
PyQt4

# Disclaimers :

The Game was created by [Bruno Cathala](http://www.brunocathala.com/tong/). <br>
The pictures used are not mine and were created by [Camile Chaussy](http://camille-chaussy.com/) and are used for the original game.

# Rules :

This is a 2 players game. Each turn, a player decides of a type of insect to feed the cameleon. The Cameleon then eats all the insects of this type that are in the line or column in front of which the cameleon is. Then the cameleon moves clock-wise. The number of insects eaten decides of how much the cameleon moves. If one insect was eaten, the camelon moves of 1, if two insects were eaten, then the cameleon moves of 2 ... <br>
The first player who cannot feed the cameleon because all the insect of the line/column were eaten loses the game.

# Getting started

Simply run the file GUI.py and the game should start immediately.

# Artificial Intelligence :

In case one player wants to play the game, an AI was created. It uses a decision tree and an alpha-beta pruning algorithm, based on the minimax algorithm. <br>
There are 3 difficulties for the AI : easy, medium and hard.
