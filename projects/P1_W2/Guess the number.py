# @author TBLong
# @creation Jun 7, 2015
# @version Jun 7, 2015
#
# Guess the number

#imports
import simplegui
import random
import math

#globals
secret_number = 0
max_range = 100
num_guesses = 7

# helper function to start and restart the game
def new_game():
    global secret_number
    set_guesses()
    secret_number = random.randrange(0, max_range)
    print "New game. Range is from 0 to " + str(max_range)
    print "Number of remaining guesses is " + str(num_guesses)
    print ""
    
# End game and start a new one
def end_game():
    print "You ran out of guesses.  The number was " + str(secret_number)
    print ""
    new_game()
    

# Initialize number of guesses based upon binary search algorithm
def set_guesses():
    global num_guesses
    num_guesses = int(math.ceil(math.log(max_range, 2)))
    

# define event handlers for control panel
def range100():
    global max_range
    max_range = 100
    new_game()

def range1000():
    global max_range
    max_range = 1000
    new_game()
    
def input_guess(guess):
    global num_guesses
    
    num = int(guess)
    print "Guess was " + str(num)
    
    num_guesses -= 1
    print "Number of remaining guesses is " + str(num_guesses)
    
    if num > secret_number:
        if num_guesses > 0:
            print "Lower!"
            print ""
        else:
            end_game()
    elif num < secret_number:
        if num_guesses > 0:
            print "Higher!"
            print ""
        else:
            end_game()
    else:
        print "Correct!"
        print ""
        new_game()

    
# create frame
frame = simplegui.create_frame('Guess the number', 150, 150)

# register event handlers for control elements and start frame
frame.add_input('Guess:', input_guess, 50)
frame.add_button('Range: 0 - 100', range100)
frame.add_button('Range: 0 - 1000', range1000)
frame.start()

# call new_game 
new_game()
