import pygame as pg
import sys, math, os
# from random import randint, choice
from MOT_constants import *


win = pg.display.set_mode((win_width, win_height))
pg.display.set_caption(title)

background_col = GREY
hover_col = SLATEGREY
click_col = GREENYELLOW
select_col = RED

FPS = 60


class MOTobj():
    def __init__(self, default_color):
        # -- Object positions and velocity attributes
        self.x, self.y = choice([n for n in range(int(boundary["left"]), int(boundary["right"]))
                                 if n not in range(x - obj_radius, x + obj_radius)]), \
                         choice([n for n in range(int(boundary["up"]), int(boundary["down"]))
                                 if n not in range(y - obj_radius, y + obj_radius)])
        # -- Velocity set so that it's random within a range but not zero
        self.dx, self.dy = choice([dx for dx in range(min_spd, max_spd) if dx not in [0]]), \
                           choice([dy for dy in range(min_spd, max_spd) if dy not in [0]])

        # -- Radius of the circle objects
        self.radius = obj_radius

        self.mouse_enabled = False
        # -- Set the self.color attribute while drawing a circle, and the self.default_color as the original color
        # when the circle isn't clicked, hovered etc.
        self.color = WHITE
        # -- Default color of circle, usually white
        self.default_color = default_color
        # -- Object color when mouse hovers over
        self.hovered_col = hover_col
        # -- Mouse down color
        self.clicked_col = click_col
        # -- Mouse release color, used to select answers
        self.selected_col = select_col

        self.isSelected = False
        self.isClicked = False

        self.state = ""

    def change_color(self, color):
        self.color = color

    def m_hover(self, mouse_x, mouse_y):
        # sqx, sqy = (m_x - self.x) ** 2, (m_y - self.y) ** 2
        if math.sqrt(((mouse_x - self.x) ** 2)+((mouse_y - self.y) ** 2)) < self.radius:
            if self.color == self.default_color:
                self.color = self.hovered_col
        elif self.color == self.selected_col:
            self.color = self.selected_col
        else:
            self.color = self.default_color

    def m_click(self, mouse_x, mouse_y):
        # sqx, sqy = (m_x - self.x) ** 2, (m_y - self.y) ** 2
        if math.sqrt(((mouse_x - self.x) ** 2)+((mouse_y - self.y) ** 2)) < self.radius:
            # self.color = self.clicked_col
            if self.color == self.hovered_col:
                self.color = self.clicked_col
                self.isClicked = True
                self.isSelected = False
        else:
            pass

    def m_change(self, mouse_x, mouse_y):
        if self.color == self.clicked_col:
            self.isSelected = True

    def m_select(self):
        if self.isClicked is True and self.isSelected is False:
            self.isSelected = True
        if self.isClicked and self.isSelected:
            self.color = self.selected_col
            self.isClicked = False
            self.isSelected = True
        elif self.isClicked is False and self.isSelected:
            self.isSelected = False
            self.color = self.default_color

        while self.isClicked and self.isSelected:
            self.color = self.selected_col
        else:
            self.color = self.default_color


    def m_deselect(self):
        if self.isClicked and self.isSelected:
            self.isSelected = False
            self.isClicked = False

    def detect_collision(self, mlist):
        # -- Change the position of the circle
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

    def draw_circle(self, display):
        pg.draw.circle(display, self.color, (int(self.x), int(self.y)), self.radius)


def main():
    # -- Create a dictionary of objects for distractors and targets
    index_d = []
    index_t = []
    for nd in range(num_distractor):
        index_d.append(nd)
    for nt in range(num_targ):
        index_t.append(nt)
    index_m = index_d + index_t

    list_dstr = []
    list_targ = []
    for nd in range(num_distractor):
        d = MOTobj(WHITE)
        list_dstr.append(d)
    for nt in range(num_targ):
        t = MOTobj(YELLOW)
        list_targ.append(t)
    list_master = list_dstr + list_targ

    dict_dstr = dict(zip(index_d, list_dstr))
    dict_targ = dict(zip(index_t, list_targ))
    dict_master = dict(zip(index_m, list_master))

    done = False

    pg.init()  # -- Initiate pygame module
    t0 = pg.time.get_ticks()  # start counting

    # == Main loop ==
    while not done:
        runtime = (pg.time.get_ticks()-t0)/1000  # measure runtime since loop began
        win.fill(background_col)  # fill background with background color
        m_x, m_y = pg.mouse.get_pos()  # get x and y coord of mouse cursor on window

        # -- Quit control
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True  # close window to quit
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                done = True  # press escape key to quit

            # -- Set the mouse control for master list
            for obj in list_master:
                if event.type == pg.MOUSEMOTION:
                    obj.m_hover(m_x, m_y)
                if event.type == pg.MOUSEBUTTONDOWN:
                    obj.m_click(m_x, m_y)
                if event.type == pg.MOUSEBUTTONUP:
                    obj.m_select()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    print("click state %s" % obj.isClicked)
                    print("select state %s" % obj.isSelected)

        # -- Animate objects on each separate list
        for d in list_dstr:
            for t in list_targ:
                if runtime <= aniT:
                    d.detect_collision(list_master)
                    d.draw_circle(win)
                    t.detect_collision(list_master)
                    t.draw_circle(win)
                    print(runtime)
                else:
                    d.draw_circle(win)
                    t.draw_circle(win)

        # # -- Animate objects on master list
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
