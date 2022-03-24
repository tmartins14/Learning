# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = True
outcome = ""
score = 0
busted = False


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        #print card_loc
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        
    def __str__(self):
        # return a string representation of a hand
        hand_str = "Hand contains "
        
        for i in self.hand:
            hand_str += i.__str__() +" "
            
        return hand_str
        
        
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.hand_value = 0
        ace = 0
        
        for c in self.hand:
            self.hand_value += VALUES.get(c.get_rank())
            if c.get_rank() == 'A':
                ace = 10
                
        if self.hand_value + ace <= 21:
            self.hand_value += ace
         
        return self.hand_value
            
        
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0;
        for c in self.hand:
            c.draw(canvas,[pos[0]+80*i, pos[1]])
            i += 1

    
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(s,r) for s in SUITS for r in RANKS]

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)
        
        return self.deck
        
    def deal_card(self):
        # deal a card object from the deck
        
        return self.deck.pop(0)
    
    def __str__(self):
        # return a string representing the deck
        deck_str = "Deck contains "
        
        for i in self.deck:
            deck_str += i.__str__() +" "
            
        return deck_str

# Define global variables for Classes
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()



#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, player_hand, dealer_hand, busted, outcome
    # your code goes here
    
    outcome = ""
    busted = False
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    
    deck.shuffle()
    # Dealing hands should go player, dealer, player, dealer
    # Deal First Card to Player
    player_hand.add_card(deck.deal_card())
    
    # Deal Second Card to Dealer
    dealer_hand.add_card(deck.deal_card())
    
    # Deal Third Card to Player
    player_hand.add_card(deck.deal_card())
    
    # Deal Fourth Card to Dealer
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True
    
#    print "Player",player_hand, player_hand.get_value()
#    print "Dealer",dealer_hand, dealer_hand.get_value()

def hit(): 
    # if the hand is in play, hit the player
    global player_hand, deck, score, outcome, in_play, busted
    
    if busted:
        pass
    else:
        player_hand.add_card(deck.deal_card())
    #    print "Player",player_hand, player_hand.get_value()

        if player_hand.get_value() > 21:
            outcome = "You have busted"
            score -= 1
            in_play = False
            busted = True
        
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global dealer_hand, player_hand, deck, in_play, score, outcome
    
    in_play = False
    
    if busted:
        pass
    else:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "Dealer",dealer_hand, dealer_hand.get_value()

        # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() >= player_hand.get_value() and dealer_hand.get_value() <= 21:
            outcome = "Dealer wins"
            score -= 1
        else:
            outcome = "Player wins"
            score += 1


# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, score
    
    canvas.draw_text('BlackJack', (60, 40), 30, 'White')
    canvas.draw_text('Dealer', (80, 85), 25, 'White')
    canvas.draw_text('You', (80, 305), 25, 'White')
    canvas.draw_text('Score '+str(score), (380, 40), 30, 'White')
    canvas.draw_text(outcome, (250, 305), 30, 'White')
       
    player_hand.draw(canvas, [80, 400])
    dealer_hand.draw(canvas, [300, 100])
    
    if in_play :
        card_loc = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [300 + CARD_CENTER[0], 100 + CARD_CENTER[1]], CARD_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
deal()
frame.start()


# remember to review the gradic rubric