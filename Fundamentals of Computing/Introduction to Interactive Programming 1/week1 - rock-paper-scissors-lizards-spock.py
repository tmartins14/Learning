# Mini-Project #1: Rock-Paper-Scissors-Lizard-Spock

import random

def name_to_number(name):
    
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3
    elif name == 'scissors':
        number = 4
    else:
        print "name does not match a valid option. Please select one of the following:"
        print "rock"
        print "paper"
        print "scissors"
        print "lizard"
        print "Spock"
    
    return number


def number_to_name(number):

    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        print "number does not match a valid option. Please select a number between 0 and 4"
        
    return name

    

def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print ""
    
    # print out the message for the player's choice
    print "Player chooses", player_choice
    
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,4)
    
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print "Computer chooses", comp_choice
    
    # compute difference of comp_number and player_number modulo five
    #comp_mod = comp_number % 5
    rpsls_diff = (player_number - comp_number)%5
    
    # use if/elif/else to determine winner, print winner message
    if rpsls_diff == 0:
        print "Player and Computer Tie!"
    elif rpsls_diff <= 2:
        print "Player wins!"
    elif rpsls_diff >= 3:
        print "Computer wins!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



