import random
from termcolor import colored

muteAI = False

class Board:
  def __init__(self):
    """
    This does nothing.
    """
    self.cards = None
    self.pots = None
    self.hands = None
    self.eaten = None
    self.nround = 0
    self.scores = None

  def Initialize(self, Nplayers):
    if self.nround == 0:
      self.scores = [0]*Nplayers

    # Put 50 cards into cards list
    self.cards = []
    Nlist = [1,1,1,2,2,2,4,4,5,5,5,7,7,7]
    for n in Nlist:
      self.cards.append(Card('r', n))
      self.cards.append(Card('b', n))
      self.cards.append(Card('y', n))
    for i in range(8):
      self.cards.append(Card('g', 4))

    # Create Nplayers hands
    self.hands = []
    for i in range(Nplayers):
      self.hands.append([])
    # Randomly distribute cards
    i = self.nround % Nplayers # Starting from the nround player
    self.nround += 1
    while (len(self.cards)>0):
      card = random.choice(self.cards)
      self.hands[i].append(card)
      self.cards.remove(card)
      i+=1
      if i==Nplayers:
        i=0
    # Sort cards in hands
    for i in range(Nplayers):
      self.hands[i] = sorted(self.hands[i], key=lambda card: card.__repr__())

    # Initialize cards eaten
    self.eaten = []
    for i in range(Nplayers):
      self.eaten.append({'r':0, 'b':0, 'y':0, 'g':0})

    # Three empty pots
    self.pots=[]
    for i in range(3):
      self.pots.append(Pot(i))

  def checkState(self):
    Ntot = 0
    for hand in self.hands:
      Ntot += len(hand)
    if Ntot == 0:
      return False
    else:
      return True

  def play(self, ID, potID, card):
    eaten = self.pots[potID].addCard(card)
    for key in self.eaten[ID].keys():
      self.eaten[ID][key] += eaten[key]

  def playable(self, card, potID):
    if card.color == 'g':
      return True
    if self.pots[potID].color == card.color:
      return True
    if self.pots[potID].color != 'w':
      return False
    else:
      for pot in self.pots:
        if pot.color == card.color:
          return pot.ID == potID
      return True

  def Score(self):
    Nplayer = len(self.eaten)
    scores = [0 for i in range(Nplayer)]
    for c in "rby":
      nmax = 0
      for i in range(Nplayer):
	if self.eaten[i][c] == nmax:
	  #print "Increasing nmax: ", i, c, self.eaten[i][c], nmax
	  nmax += 1
        if self.eaten[i][c] > nmax:
	  nmax = self.eaten[i][c]
      for i in range(Nplayer):
        #print i, c, self.eaten[i][c], nmax
        if self.eaten[i][c] == nmax:
	  continue
	scores[i] += self.eaten[i][c]
    for i in range(Nplayer):
      scores[i] += 2*self.eaten[i]['g']
    return scores

  def printState(self, playerID):
    for i in range(3):
      print "Pot #", i, "has cards (Totaling {0:>2d}):".format(self.pots[i].point), self.pots[i]
    print "You have", self.hands[playerID], "in your hand."

    Nplayer = len(self.eaten)
    for i in range(Nplayer):
      playerString = "Player # {0:d}".format(i)
      if i==playerID: playerString+=" (You):"
      else: playerString+="      :"
      print playerString, self.eaten[i]

class Card:
  def __init__(self, color, point):
    self.color=color
    self.point=point
  #def __str__(self):
  #  return self.color+"{0:d}".format(int(self.point))
  def __repr__(self):
    return self.color+"{0:d}".format(int(self.point))

class Pot:
  def __init__(self, ID):
    self.cards = []
    self.color = "w"
    self.point = 0
    self.ID = ID
  def addCard(self, card):
    eaten = {'r':0, 'b':0, 'y':0, 'g':0}
    if self.color != "w": # Check if add card is valid
      try:
        assert self.color == card.color or card.color == 'g'
      except:
        print colored("Error: ","red"), card, \
	      colored("cannot be played in this pot. ","red")
	print "Cards in pot:", self.cards
	raise 
    self.point += card.point
    if self.point > 13: # If overload
      for c in self.cards:
        eaten[c.color] += 1
      self.cards = [card]
      self.point = card.point

      if card.color == 'g':
        self.color = 'w'
      else:
        self.color = card.color
    else:
      self.cards.append(card)
      if self.color == 'w':
        if card.color == 'g':
          self.color = 'w'
        else:
          self.color = card.color
    return eaten

  def __repr__(self):
    return self.cards.__repr__()

class Player:
  def __init__(self,ID):
    self.nextplayer = None
    self.ID = ID

  def setNextPlayer(self, p):
    assert isinstance(p, Player)
    self.nextplayer = p

  def play(self, board):
    hand = board.hands[self.ID]
    card = random.choice(hand) # Choose a card to play

    trialCount = 0
    while True:
      potID = random.randint(0,2)
      if board.playable(card, potID):
        board.play(self.ID, potID, card) # Play into that pod
	break
      trialCount += 1
      if trialCount > 27:
        print card, " cannot find a pot to put in."
	for pot in board.pots:
	  print pot
	raise Exception()
    if not muteAI:
      print "Player ", self.ID," played ", card," into pot #", potID

    hand.remove(card) # Remove card from hand

  def next(self):
    return self.nextplayer

  def __repr__(self):
    return "Player "+str(self.ID)

class Human(Player):
  def play(self, board):
    while True:
      board.printState(self.ID)

      pstring = raw_input().strip()

      if len(pstring) != 3:
        print "Invalid input."
	continue
      
      try:
        int(pstring[1])
        int(pstring[2])
      except ValueError:
        print "Invalid input."
	continue
      
      cstring = pstring[:2]
      found = False
      for card in board.hands[self.ID]:
        if card.color == cstring[0]:
	  if card.point == int(cstring[1]):
	    found = True
	    break
      if not found:
        print "Card", cstring, "isn't in your hand."
	continue

      potID = int(pstring[2])
      try:
        if not board.playable(card, potID):
          print "Card", cstring, "cannot be played in pot #", potID
	  print "Cards in pot #", potID, ":", board.pots[potID]
	else: break
      except IndexError:
        print "Pot #", potID, "doesn't exist. Please enter number (0~2)."

    board.play(self.ID, potID, card)
    print "You played", cstring, "into pot #", potID

    board.hands[self.ID].remove(card)

  def __repr__(self):
    return "  You   "

def initPlayers(NPlayers, PClass):
  Players = []

  PID = random.randint(0, NPlayers-1)
  print "You are Player #", PID

  for i in range(PID):
    Players.append(PClass(i))
  Players.append(Human(PID))
  for i in range(PID+1, NPlayers):
    Players.append(PClass(i))
  for i in range(NPlayers-1):
    Players[i].setNextPlayer(Players[i+1])
  Players[NPlayers-1].setNextPlayer(Players[0])
  return Players

def initAllAI(Nplayers, PClass):
  Players = []

  for i in range(Nplayers):
    Players.append(PClass(i))

  for i in range(Nplayers-1):
    Players[i].setNextPlayer(Players[i+1])
  Players[Nplayers-1].setNextPlayer(Players[0])

  return Players

def PrintScores(board, Players):
  oneround = board.Score()

  for i in range(len(Players)):
    board.scores[i] += oneround[i]
  
  Nplayer = len(Players)
  IDs = range(Nplayer)
  IDs = sorted(IDs, key=lambda x: board.scores[x])

  print "-=-=-=-=-=-=-=-=-=-=-=-=-=-ROUND{0:d}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-".format(board.nround)
  for i in range(Nplayer):
    s = Players[IDs[i]].__repr__() + '\t' + board.eaten[IDs[i]].__repr__() \
        + '\t' + str(board.scores[IDs[i]]) + '\t' + str(oneround[IDs[i]])
    print s




