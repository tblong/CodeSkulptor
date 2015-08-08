# @author TBLong
# @creation Jul 15, 2015
# @version Jul 15, 2015
#
# Memory

import simplegui
import random

#globals
CARD_COUNT = range(16)
card_list = []
exposed_list = []
CARD_WH = (50, 100) # card image dimensions
CARD_CENT = (CARD_WH[0] / 2, CARD_WH[1] / 2) # card image center source
selected_cards = {"current": None, "previous": None}

# helper function to initialize globals
def new_game():
    global card_list, exposed_list, state, num_turns
    state = 0
    num_turns = 0
    
    # init exposed list
    exposed_list = [] # blanks the list
    for i in CARD_COUNT:
        exposed_list.append(False)
        
    card_list = range(8)
    card_list.extend(range(8))
    random.shuffle(card_list)

# define event handlers
def mouseclick(pos):
    STATE_LOOKUP[state](pos[0] // 50)
    
def state_0(i):
    """ start of game state, no cards selected yet """
    global state
    exposed_list[i] = True
    selected_cards["current"] = i
    state = 1
    
def state_1(i):
    """ single card selected state """
    global state, num_turns
    if not exposed_list[i]:
        exposed_list[i] = True
        selected_cards["previous"] = selected_cards["current"]
        selected_cards["current"] = i
        num_turns += 1
        state = 2
    
def state_2(i):
    """ two cards selected state """
    global state
    
    if not exposed_list[i]:
        #determine if the previous two cards are paired or unpaired
        if not (card_list[selected_cards["current"]] == card_list[selected_cards["previous"]]):
            exposed_list[selected_cards["current"]] = False
            exposed_list[selected_cards["previous"]] = False            
        
        # expose state 2 card
        exposed_list[i] = True
        selected_cards["current"] = i
        state = 1

# cards are logically 50x100 pixels in size    
def draw(canvas):

    # draw numbers under cards
    num_loc = [16, 65]
    # wait for card image to be valid before drawing numbers
    if card_image.get_width() > 0:
        for num in card_list:
            canvas.draw_text(str(num), num_loc, 48, "White")
            num_loc[0] += 50
    
    # draw cards
    card_dest = [25, 50] # card placement
    for exposed in exposed_list:
        if not exposed:
            canvas.draw_image(card_image, CARD_CENT, CARD_WH, card_dest, CARD_WH)
        card_dest[0] += 50 # for drawing next card
        
    label.set_text("Turns = " + str(num_turns))

# state lookup dictionary, simplifies mouse handler code
STATE_LOOKUP = {0: state_0, 1: state_1, 2: state_2}

# create frame and add a button and labels
card_image = simplegui.load_image('http://googledrive.com/host/0B7WqYiJ6vJk7fi1YVFlpbS1KQjRIMUZ4WXRHSjFUeFhXMEp1bERfQ2ExczJGYWdaOW1IRmM/card.png')
    
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()