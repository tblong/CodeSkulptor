# @author TBLong
# @creation Jun 21, 2015
# @version Jun 21, 2015
#
# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_WH = PAD_DIM_ORIG = (PAD_WIDTH, PAD_HEIGHT)
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD1_X = HALF_PAD_WIDTH
PAD2_X = WIDTH - HALF_PAD_WIDTH
PAD_LEFT_RADS = 0.0 # radians for rotating paddle image
PAD_RIGHT_RADS = math.pi # radians for rotating paddle image
PAD_CEN_SRC_ORIG = (4, 40)
LEFT = False
RIGHT = True
PAD_VEL = 5 # paddle velocity inc/dec value
BALL_VEL_INC = 1.10 # ball velocity increment 10%

# paddle images are the same, just rotated differently
# so we only have to load a single image
paddle = simplegui.load_image('http://googledrive.com/host/0B7WqYiJ6vJk7fi1YVFlpbS1KQjRIMUZ4WXRHSjFUeFhXMEp1bERfQ2ExczJGYWdaOW1IRmM/paddle_left.png')
background = simplegui.load_image('http://googledrive.com/host/0B7WqYiJ6vJk7fi1YVFlpbS1KQjRIMUZ4WXRHSjFUeFhXMEp1bERfQ2ExczJGYWdaOW1IRmM/matrix_bground.png')

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    ball_vel[0] = random.randrange(120, 240) / 60.0
    ball_vel[1] = -(random.randrange(60, 180) / 60.0)
    
    if not direction: # LEFT
        ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_vel = paddle2_vel = 0
    paddle1_pos = paddle2_pos = HEIGHT / 2
    score1 = score2 = 0
    spawn_ball(random.choice([RIGHT, LEFT]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw background image first so its on the bottom
    canvas.draw_image(background, (300, 200), (600, 400), (300, 200), (600, 400))
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ball horizontal wall collision detection
    if ball_pos[1] <= BALL_RADIUS or (ball_pos[1] + BALL_RADIUS) >= (HEIGHT -1):
        ball_vel[1] = -ball_vel[1]
       
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # pad 1 position test
    paddle1_pos_new = paddle1_pos + paddle1_vel
    if paddle1_pos_new >= HALF_PAD_HEIGHT and paddle1_pos_new <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = paddle1_pos_new
    
    # pad 2 position test
    paddle2_pos_new = paddle2_pos + paddle2_vel
    if paddle2_pos_new >= HALF_PAD_HEIGHT and paddle2_pos_new <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = paddle2_pos_new
        
    # draw paddles
    canvas.draw_image(paddle, PAD_CEN_SRC_ORIG, PAD_DIM_ORIG, [PAD1_X, paddle1_pos], PAD_WH, PAD_LEFT_RADS)
    canvas.draw_image(paddle, PAD_CEN_SRC_ORIG, PAD_DIM_ORIG, [PAD2_X, paddle2_pos], PAD_WH, PAD_RIGHT_RADS)
    
    # determine whether paddle and ball collide    
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH: # left side collision
        ball_pad_diff = abs(ball_pos[1] - paddle1_pos)
        if ball_pad_diff <= HALF_PAD_HEIGHT:
            # reflect, increase velocity of ball by 10%
            ball_vel[0] = -ball_vel[0] * BALL_VEL_INC           
        else:
            #pad 2 wins
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH: # right side collision
        ball_pad_diff = abs(ball_pos[1] - paddle2_pos)
        if ball_pad_diff <= HALF_PAD_HEIGHT:
            # reflect, increase velocity of ball by 10%
            ball_vel[0] = -ball_vel[0] * BALL_VEL_INC
        else:
            #pad 1 wins
            score1 += 1
            spawn_ball(LEFT)
            
    # draw scores
    canvas.draw_text(str(score1), (WIDTH * 0.25, HEIGHT * 0.15), 40, "White")
    canvas.draw_text(str(score2), (WIDTH * 0.75, HEIGHT * 0.15), 40, "White")

def keydown(key):
    global paddle1_vel, paddle2_vel
    #PAD_VEL constant
    # pad1 checks
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += PAD_VEL
        
    # pad2 checks
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_VEL
              
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # pad1 checks
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += PAD_VEL
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel -= PAD_VEL
        
    # pad2 checks
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel -= PAD_VEL
        
def restart():
    new_game()
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart)

# start frame
new_game()
frame.start()