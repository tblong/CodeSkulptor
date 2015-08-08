# @author TBLong
# @creation Jul 19, 2015
# @version Jul 19, 2015
#
# Blackjack

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
in_play = False
outcome = ""
prompt = ""
score = 0
NOT_IN_PLAY_MESSAGE = "Press Deal to begin a new game."

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
        
# define hand class
class Hand:
    def __init__(self):
        self.__cards = []

    def __str__(self):
        result = "Hand -> "
        for card in self.__cards:
            result += str(card) + ":"
        return result.rstrip(":") + " Value -> " + str(self.get_value())
        
    def add_card(self, card):
        self.__cards.append(card)
            
    def get_value(self):
        has_ace = False
        result = 0
        for card in self.__cards:
            value = VALUES[card.get_rank()]
            result += value
            if value == 1:
                has_ace = True
                
        if has_ace and result + 10 <= 21:
            result += 10
        
        return result
   
    def draw(self, canvas, pos):
        offset = 10 + CARD_SIZE[0]
        for card in self.__cards:
            card.draw(canvas, pos)
            pos[0] += offset

# define deck class 
class Deck:
    def __init__(self):
        self.__deck = [Card(s, r) for s in SUITS for r in RANKS]

    def shuffle(self):
        random.shuffle(self.__deck)

    def deal_card(self):
        return self.__deck.pop()
    
    def __str__(self):
        result = "Deck -> "
        for card in self.__deck:
            result += str(card) + ":"
        return result.rstrip(":")

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, prompt
    if in_play:
        dealer_wins("You have lost.")
    
    outcome = ""
    deck = Deck()
    deck.shuffle()
    dealer, player = Hand(), Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    prompt = "Hit or Stand?"
    in_play = True

def hit():
    global outcome
    if not in_play:
        outcome = NOT_IN_PLAY_MESSAGE
        return
    
    # hit player condition
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
        
    # check if player busted
    if player.get_value() > 21:
        dealer_wins("You have busted.")
        return

def stand():
    global outcome
    if in_play:
        # dealer's turn to hit
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

        # check if dealer busted
        if dealer.get_value() > 21:
            player_wins("You have won! Dealer busted!")
            return
        
        # nobody busted, test remaining conditions
        if dealer.get_value() >= player.get_value():
            dealer_wins("You have lost.")
        else: 
            player_wins("You have won!")
        
    else:
        outcome = NOT_IN_PLAY_MESSAGE
    
def player_wins(reason):
    global outcome, score, in_play, prompt 
    outcome = reason
    score += 1
    in_play = False
    prompt = "New Deal?"
    win_sound.play()

def dealer_wins(reason):
    global outcome, score, in_play, prompt
    outcome = reason
    score -= 1
    in_play = False
    prompt = "New Deal?"
    lose_sound.play()
    
# draw handler   
def draw(canvas):
    canvas.draw_text("Blackjack", (42, 82), 52, "#34495e", "sans-serif")
    canvas.draw_text("Blackjack", (40, 80), 52, "#7f8c8d", "sans-serif")
    canvas.draw_text("Score: " + str(score), (400, 80), 28, "black", "sans-serif")
    canvas.draw_text("Dealer", (40, 140), 24, "black", "sans-serif")
    canvas.draw_text(outcome, (200, 140), 24, "black", "sans-serif")
    canvas.draw_text("Player", (40, 340), 24, "black", "sans-serif")
    canvas.draw_text(prompt, (200, 340), 24, "black", "sans-serif")
    
    # wait for images to be properly loaded
    if card_images.get_width() > 0 and card_back.get_width() > 0:
        dealer.draw(canvas, [40, 150])
        player.draw(canvas, [40, 350])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (76, 198), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# sounds
win_sound = simplegui.load_sound("http://www.wavsource.com/snds_2015-07-19_1628654123857389/video_games/duke/come_get_some_x.wav")
lose_sound = simplegui.load_sound("http://www.wavsource.com/snds_2015-07-19_1628654123857389/video_games/duke/game_over.wav")

# get things rolling
deal()
frame.start()
