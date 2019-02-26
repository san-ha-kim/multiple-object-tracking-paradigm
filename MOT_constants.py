import math
from random import randint, choice
import time


"""
Define the object class attributes
"""
obj_radius: int = 20  # size of balls in pixels
num_distractor = 6  # number of distractor objects
num_targ = 4  # number of target objects

"""
Define the times and durations in SECONDS
"""
# fix_time = Tfix = 1  # time to present fixation cross
fix_draw_time = Tfix = 1.5 # time to present fixation cross and objects
flash_time = Tfl = fix_draw_time + 1  # time for targets to flash
animation_time = Tani = flash_time + 1 # time for objects to move around in seconds
answer_time = Tans = animation_time + 5  # time limit to make answer

feedback_time = 1
"""
Define the project display window
"""
title = "Multiple Object Tracking Experiment"
win_width, win_height = 800, 600  # pixels; width of screen
win_dimension = (win_width, win_height)

"""
Define instruction texts
"""
submit_ans_txt = "Press space to submit answer"

# == Font size ==
large_font = 54
med_font = 24
small_font = 12

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
Generate random x and y coordinates within the window boundary
"""
boundary_location = ['up', 'down', 'left', 'right']
boundary_coord = [obj_radius, (win_height - obj_radius + 1), obj_radius, (win_width - obj_radius + 1)]
boundary = dict(zip(boundary_location, boundary_coord))

x_range, y_range = range(int(boundary["left"]), int(boundary["right"])), range(int(boundary["up"]), int(boundary["down"]))

# print(randint(x_range))

min_spd, max_spd = -2, 2

"""
Define session information for recording purposes
"""
session_info = {'Observer': 'Type observer initials', 'Participant': 'Type participant ID'}
date_string = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time


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
