import math
from random import randint, choice
import time


"""
Define the object class attributes
"""
obj_radius: int = 30  # size of balls in pixels
num_distractor = 6  # number of distractor objects
num_targ = 4  # number of target objects

"""
Define the times and durations in SECONDS
"""
fix_draw_time = Tfix = 1.5 # time to present fixation cross and objects

flash_time = Tfl = fix_draw_time + 1  # time for targets to flash

animation_time = Tani = flash_time + 8  # time for objects to move around in seconds

answer_time = Tans = animation_time + 60  # time limit to make answer

feedback_time = 1
"""
Define the project display window
"""
title = "Multiple Object Tracking Experiment"
win_width, win_height = 1600, 900  # pixels; width of screen
win_dimension = (win_width, win_height)

"""
Define instruction texts
"""
welcome_text = "Welcome! Thank you for participating in this experiment. You can stop at any time; " \
               "just let the experimentor know!\n\nIn this experiment, you'll first see a cross at the center " \
               "of the screen. Please focus your gaze to that cross at all times. \nThen, {:d} balls will appear " \
               "around the screen, and some balls will start blinking. Pay attention to which balls have blinked. " \
               "All balls will start moving, and you need to keep track of the blinked balls. \nWhen the balls " \
               "stop moving, select which balls you think have blinked earlier. \nAfter you've selected {:d} balls, " \
               "press the space bar to submit your selection.\n\nThere is a lot of information here, so next, " \
               "there will be a step-by-step guide of what to do.\n\n" \
               "Press F to progress.".format((num_targ+num_distractor), num_targ)

fix_text = "First, you will see this cross. Please focus onto the cross and fix your gaze to where the cross is. \n\n" \
           "Press F to continue."

present_text = "Then, {:d} balls will appear randomly. Please focus your gaze to the cross. {:d} random " \
               "balls will blink briefly. Remember the balls that blinked. All balls will start moving when the " \
               "blinking stops.\n\nPress F to continue.".format((num_targ+num_distractor), num_targ)

submit_ans_txt = "When the balls stop moving, select the balls that you've been tracking.\nYou will have {:d} seconds " \
                 "to make your choice.\n\nPress space to submit your answer.".format(int(answer_time-animation_time))

# == Font size ==
large_font = 72
med_font = 42
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
