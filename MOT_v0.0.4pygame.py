import pygame as pg
import sys, math, os, time
import psychopy as psy
# from random import choice
from MOT_constants import *

x, y = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption(title)

background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW
#
# # ===== Four possible states an object can be in =====
# possible_states = ["neutral", "hovered", "clicked", "selected"]

FPS = 60
total_trials = total_trials


class MOTobj():
    def __init__(self, default_color=WHITE):
        # -- Radius of the circle objects
        self.radius = obj_radius

        # -- Object positions and velocity attributes
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

        self.animation_state = False

        self.timer = 0
        self.flash = True

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
        if state == "neutral":
            self.color = self.default_color
            self.state = "neutral"
            self.isClicked = self.isSelected = False
        if state == "hovered":
            self.color = hover_col
            self.state = "hovered"
            self.isClicked = self.isSelected = False
        if state == "clicked":
            self.color = click_col
            self.state = "clicked"
            self.isClicked = True
            self.isSelected = False
        if state == "selected":
            self.color = select_col
            self.state = "selected"
            self.isClicked = False
            self.isSelected = True

    def detect_collision(self, mlist):
        # state: bool = False
        self.animation_state = True
        # -- Turn animation on if "state" is True
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
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)

    def flash_color(self):
        if self.timer == (FPS/3):
            self.timer = 0
            self.flash = not self.flash

        self.timer += 1

        if self.flash:
            self.color = background_col
        else:
            self.color = self.default_color

        # print(self.timer)


def msg_to_screen(message_text, color):
    msg = pg.font.SysFont("arial", 24)
    msg.render(message_text, True, color)


def delay(t):
    pg.time.delay(t)


def wait_keypress(key, tstamp):
    psy.event.waitKeys(maxWait=float('inf'), keyList=[key], timeStamped=tstamp)


def flash_targets(distractor_list, target_list):
    pg.time.Clock().tick(FPS)
    for d in distractor_list:
        for t in target_list:
            d.draw_circle(win)
            t.flash_color()
            t.draw_circle(win)
    pg.display.update()


def animate(distractor_list, target_list, master_list):
    for d in distractor_list:
        for t in target_list:
            d.detect_collision(master_list)
            t.detect_collision(master_list)
            d.draw_circle(win)
            t.draw_circle(win)
    pg.display.update()


def answer_time(master_list):
    for obj in master_list:
        obj.draw_circle()
    pg.display.update()


def reset_color(master_list):
    for obj in master_list:
        obj.change_color(obj.default_color)


def generate_list(dist_list, targ_list):
    for nd in range(num_distractor):
        d = MOTobj()
        dist_list.append(d)

    for nt in range(num_targ):
        t = MOTobj(DARKKHAKI)
        targ_list.append(t)


def reset():
    # == Reset the loop, or trial ==
    pass


def main():
    # - Generate a list of lists of objects
    list_dstr = []
    list_targ = []
    generate_list(list_dstr, list_targ)
    list_master = list_dstr + list_targ

    done = False

    pg.init()  # -- Initiate pygame module
    # t0 = time.time()
    t0 = pg.time.get_ticks()
    reset = 0

    # ===== Main loop =====
    while not done:
        pg.time.Clock().tick(FPS)

        win.fill(background_col)  # =fill background with background color

        mx, my = pg.mouse.get_pos()  # =get x and y coord of mouse cursor on window

        # -- Quit control
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True  # close window to quit
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                done = True  # press escape key to quit

            # -- Set the mouse control for master list
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
                            print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
                elif not obj.in_circle(mx, my):
                    if event.type == pg.MOUSEMOTION:
                        if not obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")
                    if event.type == pg.MOUSEBUTTONUP:
                        if obj.isClicked and not obj.isSelected:
                            obj.state_control("neutral")

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    print("Spacebar has been pressed")
                    reset = 1
                    obj.state_control("neutral")

        # == Timer ==
        # t1 = time.time()
        # dt = t1-t0
        t1 = pg.time.get_ticks()  # pygame version for timer
        dt = (t1-t0)/1000
        # print("{:2.2f}".format(dt))
        ntrial = 0
        # == Trial loops ==
        if ntrial <= 2:
            if dt <= Tf:
                flash_targets(list_dstr, list_targ)
            elif Tf < dt <= Ta:
                animate(list_dstr, list_targ, list_master)
            else:
                answer_time(list_master)
                if reset == 1:
                    t0 = t1
                    ntrial += 1
                    reset = 0

        else:
            # show end screen
            print("trials over")

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
