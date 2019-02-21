import pygame as pg
import sys, math, os, time
import psychopy as psy
import random
from MOT_constants import *

# == Trial variables ==
real_trials = 2
practice_trials = 1

# == Set window ==
x, y = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
win = pg.display.set_mode((win_width, win_height)) #, pg.FULLSCREEN)
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
        # -- Objects need to be from the same list, otherwise the objects
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
        if self.timer == (FPS):
            self.timer = 0
            self.flash = not self.flash

        self.timer += 4

        if self.flash:
            self.color = background_col
        else:
            self.color = self.default_color

        # print(self.timer)

    def shuffle_position(self):
        """Shuffle the position of circles"""
        self.x = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                         if n not in range(x - self.radius, x + self.radius)])
        self.y = choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                         if n not in range(y - self.radius, y + self.radius)])


def text_objects(text, color):
    """text object defining text"""
    msg = pg.font.SysFont("arial", fontsize)
    text_surf = msg.render(text, True, color)
    return text_surf, text_surf.get_rect()


def msg_to_screen(text, textcolor):
    """function to render message to screen centered"""
    text_surface, text_rect = text_objects(text, textcolor)
    text_rect.center = (win_w/2), (win_h/2)
    win.blit(text_surface, text_rect)


def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay(t*1000)  # multiply by a thousand because the delay function takes milliseconds


def generate_list():
    """function to generate new list of objects"""
    distractor_list = []
    for nd in range(num_distractor):
        d = MOTobj()
        distractor_list.append(d)

    target_list = []
    for nt in range(num_targ):
        t = MOTobj(DARKKHAKI)
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


def answer_time(mlist):
    """function for answer submission control"""
    for obj in mlist:
        obj.draw_circle()
    pg.display.update()


def reset_color(master_list):
    """function to reset state"""
    for obj in master_list:
        obj.change_color(obj.default_color)


def fixation_cross():
    start_x, end_x = ((win_width/2)-5, win_height/2) , ((win_width/2)+5, win_height/2)
    start_y, end_y = (win_width/2, (win_height/2)-5), (win_width/2, (win_height/2)+5)
    pg.draw.line(win, WHITE, start_x, end_x)
    pg.draw.line(win, WHITE, start_y, end_y)
    pg.display.flip()


def wait_keypress(key, tstamp):
    """function to STOP ALL PROCESSES until some key is pressed"""
    psy.event.waitKeys(maxWait=float('inf'), keyList=[key], timeStamped=tstamp)


def main():
    """trial loop"""
    total_trials = real_trials
    completed_trials = 0
    reset = 0
    done = False

    # - Generate a list of lists of objects
    distractor_list, target_list = generate_list()
    list_master = target_list + distractor_list

    pg.init()  # -- Initiate pygame module
    t0 = pg.time.get_ticks()

    # ===== Main loop =====
    while not done:
        pg.time.Clock().tick(FPS)  # =Set FPS
        win.fill(background_col)  # =fill background with background color
        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window
        # == Timer ==
        t1 = pg.time.get_ticks()  # pygame version for timer
        dt = (t1 - t0) / 1000

        # == Trial loops ==
        # if completed_trials <= total_trials:
        if dt <= Tf:
            flash_targets(distractor_list, target_list)
        elif Tf < dt <= Ta:
            animate(distractor_list, target_list, list_master)
        else:
            answer_time(list_master)
            if reset == 1:
                t0 = t1
                reset = 0
                completed_trials += 1
        # else:
        #     print("trial loop over")
        #     done = True

        # == Event controller
        for event in pg.event.get():
            # -- Quit control
            if event.type == pg.QUIT:
                done = True  # close window to quit
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                done = True  # press escape key to quit

            # -- Set the mouse control for ALL OBJECTS
            for obj in list_master:
                if obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("hovered")
                            # print("Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("clicked")
                            print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)

                        if not obj.isClicked and obj.isSelected:
                            obj.state_control("neutral")
                            print("Click down; ", "Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("selected")
                            print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ",
                                  obj.isSelected)
                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    # -- Answer submission function
                    print("Spacebar has been pressed")
                    reset = 1
                    obj.state_control("neutral")
                    obj.shuffle_position()
                    if obj.isClicked and obj.isSelected:
                        # == Answer comparison
                        pass


if __name__ == "__main__":
    main()
