# @author TBLong
# @creation Jun 14, 2015
# @version Jun 14, 2015
#
# Stopwatch: The Game

# imports
import simplegui

# globals
time = 0  # time in tenths of seconds
success = 0
num_tries = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    min = get_minute(t)
    sec = get_seconds(t)
    tenths = get_tenths(t)
    return min + ":" + sec + "." + tenths

def get_minute(t):
    return str(t / 600)

def get_seconds(t):
    wholeSeconds = t / 10
    seconds = wholeSeconds % 60
    tens = seconds / 10
    ones = seconds % 10
    return str(tens) + str(ones)

def get_tenths(t):
    return str(t % 10)
    
# buttons
def start():
    timer.start()

def stop():
    global success, num_tries
    was_running = timer.is_running()
    timer.stop()
    
    if was_running:
        num_tries += 1
        if time % 10 == 0:
            success += 1
        

def reset():
    global time, success, num_tries
    timer.stop()
    time = 0
    success = 0
    num_tries = 0

# define event handler for timer with 0.1 sec interval
def timer():
    global time
    time += 1

# define draw handler
def draw_time(canvas):
    canvas.draw_text(format(time),[100, 90], 40, "White")
    draw_score(canvas)
    
def draw_score(canvas):
    score = str(success) + "/" + str(num_tries)
    canvas.draw_text(score, [250, 25], 24, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 150)
frame.set_draw_handler(draw_time)
frame.add_button("Start", start, 50)
frame.add_button("Stop", stop, 50)
frame.add_button("Reset", reset, 50)

# register event handlers
timer = simplegui.create_timer(100, timer)

# start frame
frame.start()
