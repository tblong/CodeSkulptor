# @author TBLong
# @creation May 31, 2015
# @version May 31, 2015

# Rock-paper-scissors-lizard-Spock
#
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "Invalid name argument"


def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "Number arg out of range (0-4) inclusive."
    

def rpsls(player_choice): 
    print ""
    
    print "Player chooses " + player_choice
    player_number = name_to_number(player_choice)
    
    comp_number = random.randrange(0, 5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + comp_choice
    
    mod = (player_number - comp_number) % 5   
    
    # test for winner
    if mod >= 3:
        print "Computer wins!"
    elif mod >= 1:
        print "Player wins!"
    else:
        print "Player and computer tie!"
    

# test
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
