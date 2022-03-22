# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 700
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 100
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [-2,  1]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    #ball_vel = [0, 0]
    
    ball_vel_h = random.randrange(2, 4)
    ball_vel_v = random.randrange(2, 4)
    #ball_vel_v = 0
    
    if direction == LEFT:
        ball_vel = [-ball_vel_h, -ball_vel_v]
    elif direction == RIGHT:
        ball_vel = [ball_vel_h, -ball_vel_v]
    #else:
     #   ball_val = [ball_vel_w, ball_vel_h]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global scoreL, scoreR  # these are ints
    
    score1 = 0
    score2 = 0
    
    #spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
     
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    
    # collide and reflect off of borders
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] + HALF_PAD_HEIGHT or ball_pos[1] <= paddle1_pos[1] - HALF_PAD_HEIGHT:
            spawn_ball(RIGHT)
            score2 += 1
            
        else:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += 1
            if ball_vel[1] < 0:
                ball_vel[1] += -1
            else:
                ball_vel[1] += 1

            
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos[1] + HALF_PAD_HEIGHT or ball_pos[1] <= paddle2_pos[1] - HALF_PAD_HEIGHT:
            spawn_ball(LEFT)
            score1 += 1
            
        else:   
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += -1
            
            if ball_vel[1] < 0:
                ball_vel[1] += -1
            else:
                ball_vel[1] += 1

        
    elif ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    elif ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = - ball_vel[1]
        
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos[1]+paddle1_vel <= HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    if paddle2_pos[1] + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos[1] + paddle2_vel <= HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    
    
    # draw paddles
    canvas.draw_line((paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT), (paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
    canvas.draw_line((paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT), (paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
    
    
    # determine whether paddle and ball collide    
        # Added to the collision with gutters code
    
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH // 4, 70), 40, 'White')
    canvas.draw_text(str(score2), ((WIDTH // 4) * 3, 70), 40, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

   

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game)


# start frame
new_game()
frame.start()
