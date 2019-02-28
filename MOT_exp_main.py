import pygame as pg
import sys, os, csv
from MOT_constants import *
from psychopy.gui import DlgFromDict

# == Trial variables ==
n_real = 50
n_prac = 10

# == Set window ==
x, y = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
win = pg.display.set_mode((win_width, win_height))  #, pg.FULLSCREEN)
pg.display.set_caption(title)

# == Define colors ==
background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW

# == Processing power or frames per second ==
FPS = 60



class MOTobj():
    def __init__(self, default_color=WHITE):
        # -- Radius of the circle objects
        self.radius = obj_radius

        # -- Object positions attributes
        self.x, self.y = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                                 if n not in range(x - self.radius, x + self.radius)]), \
                         choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                                 if n not in range(y - self.radius, y + self.radius)])
        # -- Velocity set so that it's random within a range but NOT ZERO
        self.dx, self.dy = choice([dx for dx in range(min_spd, max_spd) if dx not in [0]]), \
                           choice([dy for dy in range(min_spd, max_spd) if dy not in [0]])

        # -- Set the circle object neutral state color
        self.color = default_color
        self.default_color = default_color

        # -- Timer attributes
        self.timer = 0
        self.flash = True

        # -- State attributes for mouse selection control
        self.state = ""
        self.isClicked = False
        self.isSelected = False

    def change_color(self, color):
        self.color = color

    def in_circle(self, mouse_x, mouse_y):
        # -- Return boolean value whether mouse position is in circle or not
        if math.sqrt(((mouse_x - self.x) ** 2) + ((mouse_y - self.y) ** 2)) < self.radius:
            return True
        else:
            return False

    def state_control(self, state):
        # -- Neutral or default state with no form of mouse selection
        if state == "neutral":
            self.color = self.default_color
            self.state = "neutral"
            self.isClicked = self.isSelected = False
        # -- Hovered state if mouse is hovering over circle object
        if state == "hovered":
            self.color = hover_col
            self.state = "hovered"
            self.isClicked = self.isSelected = False
        # -- Clicked state if mouse click DOWN while in object
        if state == "clicked":
            self.color = click_col
            self.state = "clicked"
            self.isClicked = True
            self.isSelected = False
        # -- Selected state if mouse click UP on a "clicked" object
        if state == "selected":
            self.color = select_col
            self.state = "selected"
            self.isClicked = False
            self.isSelected = True

    def detect_collision(self, mlist):
        # -- Object positions in x and y coordinates change in velocity value
        self.x += self.dx
        self.y += self.dy
        # -- If the object reaches the window boundary, bounce back
        if self.x < self.radius or self.x > win_width-self.radius:
            self.dx *= -1
        if self.y < self.radius or self.y > win_height-self.radius:
            self.dy *= -1
        # -- If the object bounces off each other, run the Brownian motion physics
        # objects need to be from the same list, otherwise the objects
        # can pass through each other if they're from a different list
        for a in mlist:
            for b in mlist:
                if a != b:
                    if math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2)) <= (a.radius + b.radius):
                        brownian_motion(a, b)

    def draw_circle(self, display=win):
        # -- Function to draw circle onto display
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

    def flash_color(self):
        # -- Function to flash color
        if self.timer == FPS:
            self.timer = 0
            self.flash = not self.flash

        self.timer += 3
        # print("Timer: {:d}".format(self.timer))

        if self.flash:
            self.color = self.default_color
        else:
            self.color = background_col

    def shuffle_position(self):
        """Shuffle the position of circles"""
        self.x = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                         if n not in range(x - self.radius, x + self.radius)])
        self.y = choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                         if n not in range(y - self.radius, y + self.radius)])


def text_objects(text, color, textsize):
    """text object defining text"""
    msg = pg.font.SysFont("arial", textsize)
    text_surf = msg.render(text, True, color)
    return text_surf, text_surf.get_rect()  # - Returns the text surface and rect object


def msg_to_screen(text, textcolor, textsize, pos, display=win):
    """function to render message to screen centered"""
    text_surface, text_rect = text_objects(text, textcolor, textsize)  # - set variable for text rect object
    text_rect.center = pos
    display.blit(text_surface, text_rect)


def msg_to_screen_centered(text, textcolor, textsize, display=win):
    """function to render message to screen centered"""
    text_surface, text_rect = text_objects(text, textcolor, textsize)  # - set variable for text rect object
    text_rect.center = (win_width/2), (win_height/2)
    display.blit(text_surface, text_rect)


def multi_line_message(text, textsize, pos=((win_width-(win_width/10)), win_height), color=BLACK, display=win):
    """function to split text message to multiple lines and blit to display window"""
    # -- Make a list of strings split by the "\n", and each list contains words of that line as elements
    font = pg.font.SysFont("arial", textsize)
    words = [word.split(" ") for word in text.splitlines()]

    # -- Get the width required to render an empty space
    space_w = font.size(" ")[0]  # .size method returns dimension in width and height. [0] gets the width
    max_w, max_h = ((win_width-(win_width/10)), win_height)
    text_x, text_y = pos

    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)  # get surface for each word
            word_w, word_h = word_surface.get_size()  # get size for each word
            if text_x + word_w >= max_w:  # if the a word exceeds the line length limit
                text_x = (win_width/10)  # reset the x
                text_y += word_h  # start a new row
            display.blit(word_surface, (text_x, text_y))  # blit the text onto surface according to pos
            text_x += word_w + space_w  # force a space between each word
        text_x = (win_width/10)  # reset the x
        text_y += word_h  # start a new row
    pg.display.flip()


def center_message_screen(message, display=win):
    if message == "4":
        msg_to_screen_centered("Select 4 circles!", BLACK, med_font)
    if message == "NR":
        display.fill(background_col)
        msg_to_screen_centered("Time's up! Now resetting", BLACK, large_font)
        pg.display.flip()
    if message == "finished":
        display.fill(background_col)
        msg_to_screen_centered("Experiment has finished!", BLACK, large_font)
        pg.display.flip()
    if message == "prac_finished":
        display.fill(background_col)
        msg_to_screen_centered("Practice trials are over! Press F to continue to move to real trials", BLACK, med_font)
        pg.display.flip()


def guide_screen(call, mlist, selected_targets_list):
    if call == "welcome":
        win.fill(background_col)
        multi_line_message(welcome_text, med_font, ((win_width - (win_width / 10)), 120))
        pg.display.flip()
    if call == "focus":
        win.fill(background_col)
        fixation_cross()
        multi_line_message(fix_text, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "present":
        win.fill(background_col)
        fixation_cross()
        static_draw(mlist)
        multi_line_message(present_text, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "answer":
        static_draw(mlist)
        multi_line_message(submit_ans_txt, med_font, ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "timeup":
        static_draw(mlist)
        multi_line_message("Time is up! For the purpose of this guide, you need to make your selection!", med_font,
                           ((win_width - (win_width / 10)), (win_height / 2 + 30)))
        pg.display.flip()
    if call == "finished":
        win.fill(background_col)
        multi_line_message("You've selected {:d} balls correctly.\n\nThe guide is now "
                           "complete, and will move to practice rounds, where you will go through the experiment "
                           "in normal order, but your answers will not be recorded.\n\nPress F to move to the "
                           "practice rounds.".format(len(selected_targets_list)), med_font,
                           ((win_width - (win_width / 10)), 120))
        pg.display.flip()


def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay((t*1000))  # multiply by a thousand because the delay function takes milliseconds


def wait_key():
    """function to wait key press"""
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                return


def generate_list(color):
    """function to generate new list of objects"""
    distractor_list = []
    for nd in range(num_distractor):
        d = MOTobj()
        distractor_list.append(d)

    target_list = []
    for nt in range(num_targ):
        t = MOTobj(color)
        target_list.append(t)

    return distractor_list, target_list


def flash_targets(dlist, tlist):
    """function to flash targets"""
    # pg.time.Clock().tick(FPS)
    fixation_cross()
    for d in dlist:
        for t in tlist:
            d.draw_circle(win)
            t.flash_color()
            t.draw_circle(win)
    pg.display.update()


def animate(dlist, tlist, mlist):
    """function to move or animate objects on screen"""
    fixation_cross()
    for d in dlist:
        for t in tlist:
            d.detect_collision(mlist)
            t.detect_collision(mlist)
            d.draw_circle(win)
            t.draw_circle(win)
    pg.display.update()


def static_draw(mlist):
    """function for static object draw"""
    for obj in mlist:
        obj.draw_circle()


def fixation_cross(color=BLACK):
    """function to draw fixation cross"""
    start_x, end_x = ((win_width/2)-7, (win_height/2)) , ((win_width/2)+7, (win_height/2))
    start_y, end_y = (win_width/2, (win_height/2)-7), (win_width/2, (win_height/2)+7)
    pg.draw.line(win, color, start_x, end_x, 3)
    pg.draw.line(win, color, start_y, end_y, 3)


def fixation_screen(mlist):
    """function to present the fixation cross and the objects"""
    fixation_cross(BLACK)
    for obj in mlist:
        obj.draw_circle()
    pg.display.update()


def record_response(response_time, response_score, time_out_state, log):
    # record the responses
    header_list = [response_time, response_score, time_out_state]
    # convert to string
    header_str = map(str, header_list)
    # convert to a single line, separated by tabs
    header_line = ','.join(header_str)
    header_line += '\n'
    log.write(header_line)


def mouse_control(running_state, submit_state, sel4_state, t0, LM, LD, LT):

    selected_targets_list, selected_objects_list = [], []
    mx, my = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_SPACE:
                if running_state:
                    t2 = pg.time.get_ticks()
                    for target in LT:
                        if target.isSelected and not target.isClicked:
                            selected_targets_list.append(target)
                            selected_objects_list.append(target)
                    for distractor in LD:
                        if distractor.isSelected and not distractor.isClicked:
                            selected_objects_list.append(distractor)

                    if len(selected_objects_list) == num_targ:
                        submit_state = True
                        print("Answer submitted")
                    else:
                        sel4_state = True

        for obj in LM:
            if obj.in_circle(mx, my):
                if event.type == pg.MOUSEMOTION:
                    if not obj.isClicked and not obj.isSelected:
                        obj.state_control("hovered")
                        # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if not obj.isClicked and not obj.isSelected:
                        obj.state_control("clicked")
                        # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                        #       obj.isSelected)

                    if not obj.isClicked and obj.isSelected:
                        obj.state_control("neutral")
                        # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                        #       obj.isSelected)
                if event.type == pg.MOUSEBUTTONUP:
                    if obj.isClicked and not obj.isSelected:
                        obj.state_control("selected")
                        # print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ",
                        #       obj.isSelected)

            elif not obj.in_circle(mx, my):
                if event.type == pg.MOUSEMOTION:
                    if not obj.isClicked and not obj.isSelected:
                        obj.state_control("neutral")
                if event.type == pg.MOUSEBUTTONUP:
                    if obj.isClicked and not obj.isSelected:
                        obj.state_control("neutral")


def guide_user(master_list, distractor_list, target_list):

    timeup = False
    submitted = False
    need_to_select_4 = False
    guiding = True
    animating = True
    Tsub = 0

    STL = []
    # -- Welcome message --
    guide_screen("welcome", master_list, STL)
    wait_key()

    # -- Fixation cross screen
    guide_screen("focus", master_list, STL)
    wait_key()
    print("inst pass")

    # -- Present cross and balls screen
    guide_screen("present", master_list, STL)
    wait_key()

    t0 = pg.time.get_ticks()

    while True:
        pg.time.Clock().tick(FPS)  # =Set FPS

        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_SPACE:
                    if guiding:
                        t2 = pg.time.get_ticks()
                        tsub = (t2-t0)/1000
                        for target in target_list:
                            if target.isSelected and not target.isClicked:
                                selected_targ.append(target)
                                selected_list.append(target)
                        for distractor in distractor_list:
                            if distractor.isSelected and not distractor.isClicked:
                                selected_list.append(distractor)

                        if len(selected_list) == num_targ:
                            submitted = True
                            print("Answer submitted")
                        else:
                            need_to_select_4 = True

            for obj in master_list:
                if obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                            # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("clicked")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)

                        if not obj.isClicked and obj.isSelected:
                            obj.state_control("neutral")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                            # print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)

                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

        t1 = pg.time.get_ticks()
        dt = (t1 - t0)/1000

        if animating:
            if dt < Tfl - Tfix:
                flash_targets(distractor_list, target_list)
            elif Tfl - Tfix <= dt < Tani - Tfl:
                for t in target_list:
                    t.state_control("neutral")
                animate(distractor_list, target_list, master_list)
            elif Tani - Tfl <= dt < Tans - Tani:
                if need_to_select_4:
                    center_message_screen("4")
                guide_screen("answer", master_list, selected_targ)
            elif Tans - Tani < dt:
                guide_screen("timeup", master_list, selected_targ)
        if submitted:
            guide_screen("finished", master_list, selected_targ)
            for obj in master_list:
                obj.shuffle_position()
                obj.state_control("neutral")
            wait_key()
            break


def practice_trials(master_list, distractor_list, target_list, CPT):
    """function for practice trials; goes through all the protocols but does not record subject responses"""
    completed_practice_trial_count = CPT

    # == Variables for controlling protocols ==
    reset = False
    submitted = False
    need_to_select_4 = False
    timeup = False

    # == Timer
    t0 = pg.time.get_ticks()

    # == Main loop
    while True:
        pg.time.Clock().tick(FPS)  # =Set FPS

        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        # -- Quit controller
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                # -- Answer submission controller
                if event.key == pg.K_SPACE:
                    if not reset:  # -- If the loop is not in the reset state
                        # -- Add selected distractors and targets separately to compare answers
                        for target in target_list:
                            if target.isSelected and not target.isClicked:
                                selected_targ.append(target)  # separate list for selected targets
                                selected_list.append(target)  # common list for both targ and dist
                        for distractor in distractor_list:
                            if distractor.isSelected and not distractor.isClicked:
                                selected_list.append(distractor)

                        if len(selected_list) == num_targ:  # if user selects the same number as there are targets
                            submitted = True  # allow for answer submission
                            print("Answer submitted")
                        else:  # if user selects more or less than there are targets,
                            need_to_select_4 = True  # remind them to select the same number as there are targets

            for obj in master_list:
                if obj.in_circle(mx, my):  # -- If the mouse is within the circle
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                            # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("clicked")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)
                        if not obj.isClicked and obj.isSelected:
                            obj.state_control("neutral")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                            # print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)

                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

        # == Timer to calculate elapsed time ==
        t1 = pg.time.get_ticks()
        dt = (t1 - t0)/1000

        if completed_practice_trial_count < n_prac:  # if the completed trial count is less than total trial count
            if not reset:  # normal state; return to this state if reset is passed, or is supposed to run
                if dt <= Tfix:  # fixation time
                    fixation_screen(master_list)
                elif Tfix < dt <= Tfl:  # flash targets
                    flash_targets(distractor_list, target_list)
                elif Tfl < dt <= Tani:  # animate/move the balls around the screen
                    for targ in target_list:
                        targ.state_control("neutral")
                    animate(distractor_list, target_list, master_list)
                elif Tani < dt <= Tans:  # stop moving the balls
                    if need_to_select_4:
                        center_message_screen("4")
                    static_draw(master_list)
                    pg.display.flip()
                    print(dt)
                elif Tans < dt:  # timed out
                    print("Timed out")
                    timeup = True

            if submitted:  # if user successfully submits answer
                win.fill(background_col)
                msg_to_screen_centered("{:d} out of {:d} correct".format(len(selected_targ), len(selected_list)), BLACK, large_font)
                pg.display.flip()
                delay(feedback_time)
                reset = True

            if timeup:  # if timed out, run this protocol
                center_message_screen("NR")
                delay(feedback_time)
                reset = True

            if reset:  # reset state to reset the whole trial
                for obj in master_list:
                    obj.shuffle_position()
                    obj.state_control("neutral")
                completed_practice_trial_count += 1
                submitted = False
                timeup = False
                t0 = t1
                reset = False
        else:  # if the user completes all the intended trial number
            win.fill(background_col)
            center_message_screen("prac_finished")
            pg.display.flip()
            wait_key()
            break


def real_trials(master_list, distractor_list, target_list, CRT, recorder):
    """function for real trials to record answer score, time and timed out state; same as practice trial except
    the user responses are recorded"""

    completed_practice_trial_count = CRT

    reset = False
    submitted = False
    need_to_select_4 = False
    timeup = False

    t0 = pg.time.get_ticks()
    while True:
        pg.time.Clock().tick(FPS)  # =Set FPS

        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_SPACE:
                    if not reset:
                        t2 = pg.time.get_ticks()  # -- time when spacebar is pressed
                        Tsub = (t2 - t0) / 1000
                        for target in target_list:
                            if target.isSelected and not target.isClicked:
                                selected_targ.append(target)
                                selected_list.append(target)
                        for distractor in distractor_list:
                            if distractor.isSelected and not distractor.isClicked:
                                selected_list.append(distractor)

                        if len(selected_list) == num_targ:
                            submitted = True
                            print("Answer submitted")
                        else:
                            need_to_select_4 = True

            for obj in master_list:
                if obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                            # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("clicked")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)

                        if not obj.isClicked and obj.isSelected:
                            obj.state_control("neutral")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                            # print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ",
                            #       obj.isSelected)

                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

        t1 = pg.time.get_ticks()
        dt = (t1 - t0)/1000

        if completed_practice_trial_count < n_real:
            if not reset:
                if dt <= Tfix:
                    fixation_screen(master_list)
                elif Tfix < dt <= Tfl:
                    flash_targets(distractor_list, target_list)
                elif Tfl < dt <= Tani:
                    for targ in target_list:
                        targ.state_control("neutral")
                    animate(distractor_list, target_list, master_list)
                elif Tani < dt <= Tans:
                    if need_to_select_4:
                        center_message_screen("4")
                    static_draw(master_list)
                    pg.display.flip()
                    print(dt)
                elif Tans < dt:
                    print("Timed out")
                    timeup = True

            if submitted:
                record_response(Tsub, len(selected_targ), False, recorder)
                win.fill(background_col)
                msg_to_screen_centered("{:d} out of {:d} correct".format(len(selected_targ), len(selected_list)), BLACK, large_font)
                pg.display.flip()
                delay(feedback_time)
                reset = True

            if timeup:
                record_response("timed out", "timed out", True, recorder)
                center_message_screen("NR")
                delay(feedback_time)
                reset = True

            if reset:
                for obj in master_list:
                    obj.shuffle_position()
                    obj.state_control("neutral")
                completed_practice_trial_count += 1
                submitted = False
                timeup = False
                t0 = t1
                reset = False
        else:
            win.fill(background_col)
            center_message_screen("finished")
            pg.display.flip()
            wait_key()
            recorder.close()
            break


def main():
    """Main loop"""

    # == Variables to count how many trials have been completed ==
    completed_real_trials = 0
    completed_practice_trials = 0

    # == Generate a list of objects ==
    list_d, list_t = generate_list(WHITE)
    list_m = list_d + list_t

    # == Dialogue box to enter participant information ==
    dlg_box = DlgFromDict(session_info, title="Multiple Object Tracking", fixed=["date"])
    if dlg_box.OK:  # - If participant information has been entered
        print(session_info)

        # == Prepare a CSV file ==
        mot_log = date_string + ' pcpnt_' + session_info['Participant'] + '_obsvr_' + session_info['Observer']
        log = open(mot_log + '.csv', 'w')
        header = ["response_time", "response_score", "timed_out"]
        delim = ",".join(header)
        delim += "\n"
        log.write(delim)

        # == Initiate pygame ==
        pg.init()

        # == Start guide ==
        guide_user(list_m, list_d, list_t)

        # == Start practice ==
        practice_trials(list_m, list_d, list_t, completed_practice_trials)

        # == Start real trials, recording responses ==
        real_trials(list_m, list_d, list_t, completed_real_trials, log)

        pg.quit()
        sys.exit()

    else:  # - If the user has not entered the participant information
        print("User has cancelled")
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    main()
