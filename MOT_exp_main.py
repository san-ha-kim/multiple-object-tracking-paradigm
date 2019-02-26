import pygame as pg
import sys, os, csv
from MOT_constants import *
from psychopy.gui import DlgFromDict

# == Trial variables ==
n_real = 2
n_prac = 1

# == Set window ==
x, y = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption(title)

# == Define colors ==
background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW

# == Processing power or frames per second ==
FPS = 60

dlg_box = DlgFromDict(session_info, title="Multiple Object Tracking", fixed=["date"])
info_entered = False
if dlg_box.OK:
    print(session_info)
    info_entered = True
else:
    print("User has cancelled")
    pg.quit()
    sys.exit()

# == Prepare a CSV file ==
mot_log = date_string + ' pcpnt_' + session_info['Participant'] + '_obsvr_'+session_info['Observer']
log = open(mot_log + '.csv', 'w')
header = ["response_time", "response_score"]
delim = ",".join(header)
delim += "\n"
log.write(delim)


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
    return text_surf, text_surf.get_rect()


def msg_to_screen(text, textcolor, textsize, display=win):
    """function to render message to screen centered"""
    text_surface, text_rect = text_objects(text, textcolor, textsize)
    text_rect.center = (win_width/2), (win_height/2)
    display.blit(text_surface, text_rect)


def message_screen(message, display=win):
    if message == "4":
        msg_to_screen("Select 4 circles!", BLACK, med_font)
    if message == "NR":
        display.fill(background_col)
        msg_to_screen("Time's up! Now resetting", BLACK, large_font)
        pg.display.flip()
    if message == "finished":
        display.fill(background_col)
        msg_to_screen("Experiment has finished!", BLACK, large_font)
        pg.display.flip()
    if message == "prac_finished":
        display.fill(background_col)
        msg_to_screen("Practice trials are over!", BLACK, large_font)
        pg.display.flip()


def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay(t*1000)  # multiply by a thousand because the delay function takes milliseconds


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
    pg.time.Clock().tick(FPS)
    for d in dlist:
        for t in tlist:
            d.draw_circle(win)
            t.flash_color()
            t.draw_circle(win)
    pg.display.update()


def animate(dlist, tlist, mlist):
    """function to move or animate objects on screen"""
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


def fixation_cross(color):
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


def record_response(response_time, response_score):
    # record the responses
    header_list = [response_time, response_score]
    # convert to string
    header_str = map(str, header_list)
    # convert to a single line, separated by tabs
    header_line = ','.join(header_str)
    header_line += '\n'
    log.write(header_line)


def wait():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                return


def main():
    """trial loop"""
    # == Number of trials ==
    completed_trials = 0
    completed_trials_p = 0
    finished_practice = False

    reset = 0  # - reset loop control
    timeup = 0  # - variable control when subject doesn't answer
    submitted = 0  # - variable control for answer submission
    select4 = 0  # - variable control when less or more than 4 objects are selected

    done = False

    # - Generate a list of lists of objects
    distractor_list, target_list = generate_list(DARKKHAKI)
    list_master = target_list + distractor_list

    pg.init()  # -- Initiate pygame module
    t0 = pg.time.get_ticks()

    # ===== Main loop =====
    while not done:
        pg.time.Clock().tick(FPS)  # =Set FPS
        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        selected_list = []  # - list for all selected objects
        selected_targ = []  # - list for all SELECTED TARGETS

        # == Event controller ==
        for event in pg.event.get():

            # -- Quit control --
            if event.type == pg.QUIT:
                done = True  # close window to quit
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                done = True  # press escape key to quit

            # -- Answer submission control --
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:  # if spacebar is pressed
                if reset == 0:  # and if the reset condition is met
                    t2 = pg.time.get_ticks()  # -- time when spacebar is pressed
                    Tsub = (t2-t0)/1000
                    # - Concern with the distractor and target objects separately
                    for target in target_list:
                        if target.isSelected and not target.isClicked:
                            selected_list.append(target)
                            selected_targ.append(target)
                    for distractor in distractor_list:
                        if distractor.isSelected and not distractor.isClicked:
                            selected_list.append(distractor)

                    if len(selected_list) == num_targ:  # - if the subject successfully selected only 4 objects
                        submitted = 1  # - move on with the trial process
                    else:
                        select4 = 1  # - otherwise remind them

            # -- Set the mouse control for ALL OBJECTS --
            for obj in list_master:
                if obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                            # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("clicked")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)

                        if not obj.isClicked and obj.isSelected:
                            obj.state_control("neutral")
                            # print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                            # print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)

                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")



        # welcome = True
        #
        # # == Practice trial loops ==
        # if completed_trials_p < n_prac and finished_practice is False:
        #     if welcome is True:
        #         win.fill(background_col)
        #         msg_to_screen("Practice round start. Press F to continue", BLACK, large_font)
        #         pg.display.flip()
        #         wait_key()
        #         welcome = False
        #     else:
        #         print("Pract over")
        #         pg.quit()
        #         sys.exit()
        # else:
        #     finished_practice = True

        # == Timer ==
        t1 = pg.time.get_ticks()  # pygame version for timer
        dt = (t1 - t0) / 1000  # total time elapsed

        # == Trial loops ==
        if completed_trials < n_real:# and finished_practice is True:
            if reset == 0:
                # print("Time elapsed: {:2.2f} seconds".format(dt))
                if dt <= Tfix:
                    fixation_screen(list_master)
                elif Tfix < dt <= Tfl:
                    fixation_cross(BLACK)
                    flash_targets(distractor_list, target_list)
                elif Tfl < dt <= Tani:
                    for targ in target_list:
                        targ.state_control("neutral")
                    fixation_cross(BLACK)
                    animate(distractor_list, target_list, list_master)
                elif Tani < dt <= Tans:
                    if select4 == 1:
                        message_screen("4")
                    static_draw(list_master)
                    pg.display.flip()
                elif Tans < dt:
                    print("Timed out")
                    timeup = 1

            if submitted == 1:
                record_response(Tsub, len(selected_targ))
                print("Reset loop RT: {:2.3f}".format(Tsub))
                win.fill(GREY)

                print("Correct number: {:d}".format(len(selected_targ)))
                print("Selected object count: {:d}".format(len(selected_list)))

                msg_to_screen("{:d} out of {:d} correct".format(len(selected_targ), len(selected_list)), BLACK, large_font)
                pg.display.flip()
                print("Submission loop RT: {:2.3f}".format(Tsub))

                delay(feedback_time)
                reset = 1
                submitted = 0

            if timeup == 1:
                record_response("timed_out", Tans)
                message_screen("NR")

                delay(feedback_time)
                reset = 1
                timeup = 0
                print("Timeup loop over")

            if reset == 1:
                for obj in list_master:
                    obj.shuffle_position()
                    obj.state_control("neutral")
                print("Shuffle complete")

                completed_trials += 1
                print("Completed {:d} trials".format(completed_trials))

                select4 = 0
                reset = 0
                Tsub = t1
                t0 = t1
                print("Reset complete")
        else:
            message_screen("finished")
            delay(2)
            print("trial complete")
            log.close()
            done = True

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
