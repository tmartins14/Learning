# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math



# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    print " "
    print "New Game"
    
    
    global secret_number
    secret_number = random.randrange(0,100)
    
    global guess_attempts
    guess_attempts = 7
    
    global guess_count
    guess_count = 0

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    new_game()
    
    
    
    print "Range is [0,100)"

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    new_game()
    global secret_number 
    secret_number = random.randrange(0,1000)
    
    global guess_attempts
    guess_attempts = 10
    
    print "Range is [0,1000)"
    
def input_guess(guess):
    # main game logic goes here	
    guess = int(guess)
    print "Guess was", guess 
    
    global guess_count
    
    
    if guess < secret_number:
        print "Higher"
        guess_count += 1
        print guess_attempts - guess_count, "more attempts!"
        
    elif guess > secret_number:
        print "Lower"
        guess_count += 1
        print guess_attempts - guess_count, "more attempts!"
    
    elif guess == secret_number:
        print "Correct"
        new_game()
        
    
        
    if guess_count == guess_attempts:
        print "You have used up all your tries. Try again!"
        
        new_game()
    
    
    
# create frame
f = simplegui.create_frame("Guess the Number!",300,300)


# register event handlers for control elements and start frame
f.add_input("Enter", input_guess, 100)
f.add_button("Range is [0,100)", range100, 100)
f.add_button("Range is [0,1000)", range1000, 100)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
