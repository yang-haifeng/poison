#!/usr/bin/env python

# Paramters setting 
NP = 4
import base
#base.muteAI = True
NRounds = NP * 1 # Setting for a full regular game of NP rounds
#NRounds = 1 

from base import *
from ai import NEv1 as AI

# Initialize the board
board = Board()

# Initialize the players
Players = initPlayers(NP, AI)
#Players = initAllAI(NP, AI)
Starter = Players[0] # Always start from Player[0]

for i in range(NRounds):
  board.Initialize(NP)
  CurrentPlayer = Starter
  Starter = Starter.next()

  # Check if game finished
  while board.checkState():
    # One player make a move
    CurrentPlayer.play(board)

    # Switch to the next player
    CurrentPlayer = CurrentPlayer.next()

  PrintScores(board, Players)
#board.Score()
