import pygame as pg
import sys, math, os
# from random import randint, choice
from MOT_constants import *


win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption(title)

background_col = GREY
hover_col = DARKSLATEGREY
click_col = GREENYELLOW
select_col = YELLOW

# ===== Four possible states an object can be in =====
possible_states = ["neutral", "hovered", "clicked", "selected"]

FPS = 60


class MOTobj():
    def __init__(self, default_color=WHITE):
        # -- Object positions and velocity attributes
        self.x, self.y = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                                 if n not in range(x - obj_radius, x + obj_radius)]), \
                         choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                                 if n not in range(y - obj_radius, y + obj_radius)])
        # -- Velocity set so that it's random within a range but NOT ZERO
        self.dx, self.dy = choice([dx for dx in range(min_spd, max_spd) if dx not in [0]]), \
                           choice([dy for dy in range(min_spd, max_spd) if dy not in [0]])

        # -- Radius of the circle objects
        self.radius = obj_radius

        # -- Set the circle object neutral state color
        self.color = default_color
        self.default_color = default_color

        self.animation_state = False

        self.state = ["neutral", "hovered", "clicked", "selected"]
        # self.isSelected = False

    def in_circle(self, mouse_x, mouse_y):
        # -- Return boolean value whether mouse position is in circle or not
        if math.sqrt(((mouse_x - self.x) ** 2) + ((mouse_y - self.y) ** 2)) < self.radius:
            return True
        else:
            return False

    def state_control(self):
        if self.state == "neutral" or "n":
            self.color = self.default_color
        if self.state == "hovered" or "h":
            self.color = hover_col
        if self.state == "clicked" or "c":
            self.color = click_col
        if self.state == "selected" or "s":
            self.color = select_col
            # self.isSelected = True
        # else:
        #     self.isSelected = False

    def detect_collision(self, mlist, state):
        # state: bool = False
        if state is True:
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
            return self.animation_state
        else:
            self.animation_state = False
            return self.animation_state

    def draw_circle(self, display):
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)


def main():
    list_dstr = []
    list_targ = []
    for nd in range(num_distractor):
        d = MOTobj()
        list_dstr.append(d)
    for nt in range(num_targ):
        t = MOTobj(DARKKHAKI)
        list_targ.append(t)
    list_master = list_dstr + list_targ

    done = False

    pg.init()  # -- Initiate pygame module
    t0 = pg.time.get_ticks()  # start counting

    # ===== Main loop =====
    while not done:
        runtime = (pg.time.get_ticks()-t0)/1000  # =measure runtime since loop began
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
                # - If mouse is over a circle
                if event.type == pg.MOUSEMOTION:
                    print(obj.in_circle(mx, my))
                    if obj.in_circle(mx, my):
                        obj.state = "hovered"
                        obj.state_control()
                        # obj.color = hover_col
                    else:
                        obj.state = "neutral"
                        # obj.color = obj.default_color
                # if event.type == pg.MOUSEBUTTONDOWN:
                #     if obj.in_circle(mx, my):
                #         obj.state = "clicked"
                #         obj.state_control()
                #     else:
                #         obj.state = "neutral"
                # if event.type == pg.MOUSEBUTTONUP:
                #     pass
            # if (event.type == pg.KEYDOWN) and (event.type == pg.K_SPACE):
            #         print("test", obj.state)
                # - If mouse click down over a circle
                # - If mouse click released while over a circle

        # -- Animate objects on each separate list
        for d in list_dstr:
            for t in list_targ:
                if runtime <= aniT:
                    d.detect_collision(list_master, True)
                    t.detect_collision(list_master, True)
                    d.draw_circle(win)
                    t.draw_circle(win)
                else:
                    d.detect_collision(list_master, False)
                    t.detect_collision(list_master, False)
                    d.draw_circle(win)
                    t.draw_circle(win)
                    # print(d.animation_state, t.animation_state)

        # -- Animate objects on master list
        # for obj in list_master:
        #     if runtime <= aniT:
        #         obj.detect_collision(list_master)
        #         obj.draw_circle(win)
        #     else:
        #         obj.draw_circle(win)

        pg.display.flip()
        pg.time.Clock().tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
