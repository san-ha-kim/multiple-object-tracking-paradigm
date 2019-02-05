import pygame, math, sys, os
pygame.init()
"""
width  = 400
height = 400
screen = pygame.display.set_mode((width, height))
surf1 = pygame.Surface((width,height))
surf1.fill((0,255,0))
pygame.draw.circle(surf1, (0,0,0), (200,200), 5)
screen.blit(surf1, (0,0))
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()

start_ticks=pygame.time.get_ticks() #starter tick
done = False
while not done:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT():
    #         done=True
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if seconds>3: # if more than 10 seconds close the game
        break
    print(seconds) #print how many seconds

scr = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Box Test')

################################################################################
# Game Loop ####################################################################
################################################################################

while True:
    pygame.display.update(); scr.fill((200, 200, 255))
    pygame.time.Clock().tick(20)
    pygame.draw.circle(scr, (0, 0, 0), (400, 300), 100)

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    sqx = (x - 400)**2
    sqy = (y - 300)**2
    print(pygame.mouse.get_pos())
    if math.sqrt(sqx + sqy) < 100:
        print('inside')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

for i in range(10):
    print(i)
    if i > 1:
        print("%s i is bigger than 1" % i)
    elif i > 5:
        print("%s i is bigger than 5" % i)


white = 255,255,255
cyan = 0,255,255

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Circle Click Test')

rectangle = pygame.Rect(400,300,200,200)

stop = False

while not stop:
    gameDisplay.fill(white)

    pygame.draw.rect(gameDisplay, cyan,rectangle,4)

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = rectangle.collidepoint(pygame.mouse.get_pos())

            if click == 1:
                print("clicked")

        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create the surface, give dimensions and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        # this rect determinies the position the ball is drawn
        self.rect = self.image.get_rect()
        # Draw the ellipse onto the surface
        pygame.draw.ellipse(self.image, (255, 0, 0), [0, 0, width, height], 10)


# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False

# --- Create sprites and groups
ball = Ball(100,100)
g = pygame.sprite.Group(ball)

# -------- Main Program Loop -----------
while not done:
    # --- Events code goes here (mouse clicks, key hits etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Clear the screen
    screen.fill((255,255,255))

    # --- Draw all the objects
    g.draw(screen)

    # --- Update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)


state1 = True
state2 = True
state3 = True
state4 = False

for i in range(24):
    if state1 is True and state2 is True:
        print("Condition passed: i is %s" % i)
        if state3==state4:
            print("Passed")
        else: print("not passed")
    else: #if state1 is True or state2 is True:
        print("-------: i is %s" % i)
"""
data = ("John", "Doe", 53.44)
format_string = "Hello"

print(format_string % data)

pygame.quit()
