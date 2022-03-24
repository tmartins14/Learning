# implementation of card game - Memory

import simplegui
import random

CANVAS_W = 800
CANVAS_H = 100
NUM_SIZE = 50

mem_deck = range(0, 8)
list2 = range(0, 8)
mem_deck.extend(list2)

exposed = [False]*16
state = 0
sel1 = -1
sel2 = -1
turns = 0

# helper function to initialize globals
def new_game():
    global mem_deck
    global state
    global exposed
    global turns
    
    turns = 0
    random.shuffle(mem_deck)
    exposed = [False]*16
    state = 0
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed
    global state
    global sel1
    global sel2
    global turns
    
    card_index = pos[0]/50
    
    
    if exposed[card_index]:
        return
    
    if state == 0:
        state = 1
        exposed[card_index] = True
        sel1 = card_index
        
    elif state == 1:
        state = 2
        exposed[card_index] = True
        sel2 = card_index
        turns += 1
        
    else:
        state = 1
        if mem_deck[sel1]!=mem_deck[sel2]:
            exposed[sel1]=False
            exposed[sel2]=False
        sel1 = card_index
        exposed[card_index] = True
    
    
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(mem_deck)):
        canvas.draw_text(str(mem_deck[i]),
                        (NUM_SIZE*i+10, NUM_SIZE+15),
                         NUM_SIZE,
                         'White')
        if not exposed[i]:
            canvas.draw_polygon([(CANVAS_W/16*i, 0), (CANVAS_W/16*(i+1), 0),
                                 (CANVAS_W/16*(i+1), CANVAS_H), (CANVAS_W/16*i, CANVAS_H)],
                                     3, 'Red', 'Green') 
    
    label.set_text("Turns = "+str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_W, CANVAS_H)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric