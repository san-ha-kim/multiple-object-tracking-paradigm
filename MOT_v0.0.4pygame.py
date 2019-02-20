import pygame as pg
import sys, math, os, time
import psychopy as psy
# from random import choice
from MOT_constants import *

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
    """function to draw message onto window"""
    msg = pg.font.SysFont("arial", 24)
    msg.render(message_text, True, color)


def delay(t):
    """function to stop all processes for a time"""
    pg.time.delay(t)


def wait_keypress(key, tstamp):
    """function to STOP ALL PROCESSES until some key is pressed"""
    psy.event.waitKeys(maxWait=float('inf'), keyList=[key], timeStamped=tstamp)


def flash_targets(distractor_list, target_list):
    """function to flash targets"""
    pg.time.Clock().tick(FPS)
    for d in distractor_list:
        for t in target_list:
            d.draw_circle(win)
            t.flash_color()
            t.draw_circle(win)
    pg.display.update()


def animate(distractor_list, target_list, master_list):
    """function to move or animate objects on screen"""
    for d in distractor_list:
        for t in target_list:
            d.detect_collision(master_list)
            t.detect_collision(master_list)
            d.draw_circle(win)
            t.draw_circle(win)
    pg.display.update()


def answer_time(master_list):
    """function for answer submission control"""
    for obj in master_list:
        obj.draw_circle()
    pg.display.update()


def reset_color(master_list):
    """function to reset state"""
    for obj in master_list:
        obj.change_color(obj.default_color)


def generate_list(dist_list, targ_list):
    """function to generate new list"""
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
    """trial loop"""
    # - Generate a list of lists of objects
    list_dstr = []
    list_targ = []
    generate_list(list_dstr, list_targ)
    list_master = list_dstr + list_targ

    # - state control
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
                            print("Mouse released; ""Clicked state: ", obj.isClicked, "Selected state: ", obj.isSelected)
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
            # --- show end screen
            print("trials over")

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
