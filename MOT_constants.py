import math
from random import randint, choice

"""
Define number of trials
"""
completed_trials = 0  # how many trials have been completed
total_trials = 50  # how many trials in total
trial_is_running: bool = False

"""
Define the times and durations in MILLISECONDS
"""
flash_time = flashT = 1000  # time for targets to flash
blink_time = 125
targ_pres_time = 250
targ_hold_time = 200

animation_time = aniT = flash_time + 8000 # time for objects to move around in seconds
answer_time = 3000

"""
Define the project display window
"""
title = "Multiple Object Tracking Experiment"
win_width = 1200  # pixels; width of screen
win_height = 675
win_dimension = (win_width, win_height)

"""
Define instruction texts
"""
submit_ans_txt = "Press space to submit answer"

"""
Define some colours
"""
# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]

# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [220, 20, 60]

"""
Define the floating object class attributes
"""
obj_radius: int = 20  # size of balls in pixels
obj_diam: int = obj_radius*2

num_distractor = 6  # number of distractor objects
num_targ = 4  # number of target objects

"""
Generate random x and y coordinates within the window boundary
"""
boundary_location = ['up', 'down', 'left', 'right']
boundary_coord = [obj_radius, (win_height - obj_radius), obj_radius, (win_width - obj_radius)]
boundary = dict(zip(boundary_location, boundary_coord))

range(int(boundary["left"]), int(boundary["right"]))

x = randint(boundary["left"], boundary["right"])
y = randint(boundary["up"], boundary["down"])

min_spd, max_spd = -2, 2
limit_horiz, limit_vert = randint(boundary["left"], boundary["right"]), randint(boundary["up"], boundary["down"])


def brownian_motion(C1, C2):
    """ ===== FUNCTION TO CALCULATE BROWNIAN MOTION ===== """
    c1_spd = math.sqrt((C1.dx ** 2) + (C1.dy ** 2))
    diff_x = -(C1.x - C2.x)
    diff_y = -(C1.y - C2.y)
    vel_x = 0
    vel_y = 0
    if diff_x > 0:
        if diff_y > 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x < 0:
        if diff_y > 0:
            angle = 180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = -180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x == 0:
        if diff_y > 0:
            angle = -90
        else:
            angle = 90
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    elif diff_y == 0:
        if diff_x < 0:
            angle = 0
        else:
            angle = 180
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    C1.dx = vel_x
    C1.dy = vel_y
