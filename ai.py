from base import *

class weighted(Player):
  """
  This is still incomplete
  """
  def play(self, board):
    hand = board.hands[self.ID]

    weights = [0] * 3
    wdict = {1:0, 2:0, 4:1, 5:2, 7:3}

    for ic, c in 'rby':
      for card in hand:
        if card.color==c:
	  weights[ic] += wdict[card.point]

class not_eat(Player):
  def play(self, board):
    hand = board.hands[self.ID]
    # Get the hand in decreasing point order.
    decreasing = sorted(hand, key=lambda x: -x.point)

    # Try to play the card with highest point first
    for card in decreasing:
      for potID in range(3):
        if board.playable(card, potID):
	  if board.pots[potID].point+card.point <= 13:
	    board.play(self.ID, potID, card)
	    if not muteAI:
	      print "Player ", self.ID," played ", card," into pot #", potID
	    hand.remove(card)
	    return

    # There's no way not to eat. Just play the card with highest point
    card = decreasing[0]
    for potID in range(3):
      if board.playable(card, potID):
	board.play(self.ID, potID, card)
	if not muteAI:
	  print "Player ", self.ID," played ", card," into pot #", potID
	hand.remove(card)
	return

class NEv1(Player):
  def play(self, board):
    hand = board.hands[self.ID]
    # Get the hand in decreasing point order.
    decreasing = sorted(hand, key=lambda x: -x.point) 

    # Try to play the card with highest point first
    for card in decreasing:
      for potID in range(3):
        if board.playable(card, potID):
	  if board.pots[potID].point+card.point <= 13 \
	     or isLeading(board, self.ID, card.color):
	    board.play(self.ID, potID, card)
	    if not muteAI:
	      print "Player ", self.ID," played ", card," into pot #", potID
	    hand.remove(card)
	    return

    # There's no way not to eat. Just play the card with highest point
    card = decreasing[0]
    for potID in range(3):
      if board.playable(card, potID):
	board.play(self.ID, potID, card)
	if not muteAI:
	  print "Player ", self.ID," played ", card," into pot #", potID
	hand.remove(card)
	return

def isLeading(board, pID, c):
  if board.eaten[pID][c] == 0: return False
  Nplayer = len(board.eaten)
  for i in range(Nplayer):
    if board.eaten[i][c] > board.eaten[pID][c] and i!=pID:
      return False
  return True

class NEv2(Player):
  def play(self, board):
    hand = board.hands[self.ID]
    # Sort it by color first, from longer suit to shorter suit
    CSfun = self.getColorSort(hand)
    decreasing = sorted(hand, key=CSfun)
    # Get the hand in decreasing point order.
    decreasing = sorted(decreasing, key=lambda x: -x.point) 

    # Try to play the card with highest point first
    for card in decreasing:
      for potID in range(3):
        if board.playable(card, potID):
	  if board.pots[potID].point+card.point <= 13 \
	     or isLeading(board, self.ID, card.color):
	    board.play(self.ID, potID, card)
	    if not muteAI:
	      print "Player ", self.ID," played ", card," into pot #", potID
	    hand.remove(card)
	    return

    # There's no way not to eat. Just play the card with highest point
    card = decreasing[0]
    for potID in range(3):
      if board.playable(card, potID):
	board.play(self.ID, potID, card)
	if not muteAI:
	  print "Player ", self.ID," played ", card," into pot #", potID
	hand.remove(card)
	return

  def getColorSort(self, hand):
    CSdict = {'y':0, 'r':0, 'b':0, 'g':3} # Green is always the last
    cardCounts = [0,0,0]
    cList = 'yrb'
    for card in hand:
      if card.color == 'g': continue
      ind = cList.index(card.color)
      cardCounts[ind]+=1
    inds = sorted( range(3), key=lambda x: -cardCounts[x] )
    for c in cList:
      CSdict[c] = inds.index( cList.index(c) )
    def CSfun(card):
      return CSdict[card.color]
    return CSfun






