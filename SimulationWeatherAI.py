from MLModel import Date_Weather
# Import the pygame library and initialise the game engine
import datetime
import pygame
pygame.init()


# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
#frames we will count
framesss = 0
dayindex = 0
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cooties")
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

#set todays date to start the next 30 years
base = datetime.datetime.today().date()
#make a list of dates for everyday for the next 30 years so 9624 samples
date_list = [base + datetime.timedelta(days=x) for x in range(9624)]
#turn the list into a list of strings to feed into the model
date_list_string = [d.strftime('%m%d') for d in date_list]
Days = date_list_string;
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop
    framesss += 1
    if framesss >= 60:
        framesss = 0
    dayindex += 1
    Day = Days[dayindex]
    print(Day)
  

    WT = Date_Weather(int('1990' + Day))
    print(WT)
    #get the average temperature for the date we predicted
    #add the high and low of the day together
    Avg_WT = WT[1] + WT[2]
    #take the result and divide ir by two for the average
    Avg_WT = Avg_WT/2
    # --- Game logic should go here
    # create a text surface object,
    # on which text is drawn on it.
    if(Avg_WT >= 80):
        Temp = font.render('Hot', True, GREEN, RED)
    elif(Avg_WT > 60 and Avg_WT < 80):
        Temp = font.render('Ideal',True, GREEN, RED)
    elif(Avg_WT <= 60):
        Temp = font.render('Cold', True, GREEN, RED)

    if(WT[0] > 0.00 and Avg_WT < 32):
        Rain = font.render('Snow', True, RED, GREEN)
    elif(WT[0] > 0.50):
        Rain = font.render('Storm', True, RED, GREEN)
    elif(WT[0] < 0.50 and WT[0] > 0.15):
        Rain = font.render('Wet', True, RED, GREEN)
    elif(WT[0] <= 0.15):
        Rain = font.render('Dry', True, RED, GREEN)
    # create a rectangular object for the
    # text surface object
    textRect = Temp.get_rect()
    rainRect = Rain.get_rect() 
    # set the bottom right of the rectangular object.
    textRect.bottomright = (700, 500)
    rainRect.bottomright = (700, 450)
     # --- Drawing code should go here
     # First, clear the screen to white. 
    screen.fill(WHITE)
    
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(Temp, textRect)
    screen.blit(Rain, rainRect)
 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
     # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
