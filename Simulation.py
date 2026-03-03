from MLModel import Date_Weather
# Import the pygame library and initialise the game engine
import pygame
pygame.init()


# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop
 
     # --- Game logic should go here
     # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Weather', True, GREEN, RED)
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
     
    # set the center of the rectangular object.
    textRect.center = (700 // 2, 500 // 2)
     # --- Drawing code should go here
     # First, clear the screen to white. 
    screen.fill(WHITE)
    
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(text, textRect)
 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
     # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
