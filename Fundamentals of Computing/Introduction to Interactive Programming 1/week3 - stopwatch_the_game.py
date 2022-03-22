# template for "Stopwatch: The Game"
import simplegui


# GLOBAL VARIABLES
counterX = 0
positionX = [150, 25]
counterY = 0
positionY = [175, 25]
clock = 0
interval = 100
timer_running = False
width = 200
height = 200
position = [50, 110]


# HELPER FUNCTIONS
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    
    A = int(t/60000)
    B = (t/10000) % 6
    C = int((t % 10000)/1000)
    D = (t % 1000)/100
    
    clock_str = str(A)+":"+str(B)+str(C)+"."+str(D)
    
    return clock_str


# EVENT HANDLERS
# Event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
    global timer_running
    timer_running = True
    
def stop():
    timer.stop()
    
    global clock
    global timer_running
    global counterY 
    global counterX
    
    if timer_running:
        if timer_running:
            counterY += 1
        
        if (clock % 1000)/100 == 0:
            counterX += 1
        
    timer_running = False
        
    
def reset():
    global clock
    clock = 0
    
    global counterX
    counterX = 0
    
    global counterY
    counterY = 0
    

# Event handler for timer with 0.1 sec interval
def stop_watch():
    global clock
    clock += interval

    
# Draw handler
def draw(canvas):
    canvas.draw_text(format(clock), position, 40, "White")
    
    canvas.draw_text(str(counterX)+"/", positionX, 30, "Green")
    canvas.draw_text(str(counterY), positionY, 30, "Green")

    
# CREATE A FRAME
frame = simplegui.create_frame("Stopwatch: The Game", width, height)


# REGISTER EVENT HANDLERS
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, stop_watch)
frame.add_button("Start", start, 50)
frame.add_button("Stop", stop, 50)
frame.add_button("Reset", reset, 50)


# START FRAME AND TIMERS
frame.start()






