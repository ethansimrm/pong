# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    horizontal = random.randrange(2,4) #120 pixels per second divided by the refresh rate. 
    vertical = random.randrange(1,3)
    if direction:
        ball_vel = [horizontal,-vertical]
    else:
        ball_vel = [-horizontal,-vertical]
        
# define event handlers
def new_game(): #this spawns our paddles, resets scores, and spawns a ball with random direction
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]
    score1 = 0
    score2 = 0
    randomdirection = random.randrange(0,2) #implemented random initial direction
    if randomdirection == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # reflect ball if hit top and bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # update ball position implicitly using refresh rate
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] < 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] > HEIGHT-PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT-PAD_HEIGHT
    else:
        paddle1_pos[1] += paddle1_vel[1]
        
    if paddle2_pos[1] < 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] > HEIGHT-PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT-PAD_HEIGHT
    else:
        paddle2_pos[1] += paddle2_vel[1]
    
    # draw paddles
    canvas.draw_line(paddle1_pos, [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos, [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide and add 10% to ball velocity on collision   
    if ball_pos[0] <= PAD_WIDTH+BALL_RADIUS:
        if paddle1_pos[1] - BALL_RADIUS <= ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT + BALL_RADIUS:
            ball_vel[0] = -ball_vel[0]*1.1
        else: # if ball ends up in gutter, award 1 point to other player and respawn ball
            spawn_ball(RIGHT) #Ball travels towards the player who won the last point
            score2 += 1
    if ball_pos[0] >= WIDTH-PAD_WIDTH-BALL_RADIUS:
        if paddle2_pos[1] - BALL_RADIUS <= ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT + BALL_RADIUS:
            ball_vel[0] = -ball_vel[0]*1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    
    # draw scores
    canvas.draw_text(str(score1), [175, 100], 50, "Green")
    canvas.draw_text(str(score2), [400, 100], 50, "Green")
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += 4
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= 4
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += 4
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= 4
        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -= 4
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += 4
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -= 4
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += 4

        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
