#import our files
from MLModel import Date_Weather
import Cootie as CT
# Import the pygame library and initialise the game engine
import datetime
from threading import Thread
import random
import pygame
pygame.init()

WIDTH = 700
HEIGHT = 500

#Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (  0,  0,  255)
#frames we will count
framesss = 0
global dayindex
dayindex = 0
currentW = 'Base'
currentT = 'Empty'
# Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cooties")
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
# The loop will carry on until the user exits the game (e.g. clicks the close button).
global GetDates
GetDates = True
global carryOn
carryOn = False
global startingcootie1
startingcootie1 = True
global startingcootie2
startingcootie2 = False 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
global spite_spd
sprite_spd = clock.tick(60)

#set todays date to start the next 30 years
base = datetime.datetime.today().date()
#make a list of dates for everyday for the next 30 years so 9624 samples
date_list = [base + datetime.timedelta(days=x) for x in range(9624)]
#turn the list into a list of strings to feed into the model
date_list_string = [d.strftime('%m%d') for d in date_list]
global Days
Days = date_list_string;



#create a sprite class to hold our bg sprites
class BG_Weather(pygame.sprite.Sprite):
   #making a function in the class that runs when a new instance of this class is called
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       #create the iamge that will be drawn when the sprite is drawn  
       self.image = pygame.Surface((700, 500))
       #loading two images for the sprite
       self.RainSheet = pygame.image.load("weathersprites/RainSheet.png")
       self.DrySheet = pygame.image.load("weathersprites/DrySheet.png")
       #making a rect that is used to move and set the location of the sprite
       self.rect = self.image.get_rect()
       #setting the location of the rects topleft corner
       self.rect.topleft = (0,0)
       #making a frame variable that changes the what part of the images we are looking at
       self.frame = 0
       #making a counter for the the frames to change
       self.frame_time = 0
      ##setting a color to ignore in the images
       self.image.set_colorkey(BLACK)
   #making an update function for the class it takes three things when you call it
   #self just means it will effect itself, weather Rain,snow,dry,etc...
   def update(self,weather,Temp):
      if weather == 'Wet':
         self.image.set_alpha(255)
         if self.frame_time > 2:
            self.frame_time = 0
            self.image.fill(BLACK)
            self.frame += 1
         if self.frame >= 16:
            self.frame = 0
         self.image.set_colorkey(BLACK)
         self.image.blit(self.RainSheet, self.rect, ((WIDTH * self.frame),0, WIDTH, HEIGHT))
         self.frame_time += 1
      elif weather == 'Dry':
         self.image.blit(self.DrySheet, self.rect)
         self.image = self.image.convert_alpha()
         self.image.set_alpha(125)
      if Temp == 'Ideal':
         self.image.set_alpha(50)

         

#create a class for the loading logo
class Loading_screen(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.inSprite = pygame.image.load("Ui_sprites/loading.png")
      self.rect = self.inSprite.get_rect()
      self.rect.topleft = (0, 0)
      self.angle = 0

   def update(self):
      #rotate the loading icon
      self.angle -= 1
      self.angle % 360
      self.image = pygame.transform.rotate(self.inSprite, self.angle)
      self.rect = self.image.get_rect(center = (25, 25))

#sample cootie sprite object

         

#make a group for the sprites that show the weather effects
Weather_Sprites = pygame.sprite.Group()
cur_weather = BG_Weather()
Weather_Sprites.add(cur_weather)

#test cootie 11 inputs
                    #hardiness____________#leanness_____________#hottempered__________#coldTempered_________#Aquatic_______________#weight______________#size__________________#Maturity_____________#Appeal_________________#Gender_______________#X_#Y
testCootie = [CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,100),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,140),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,180),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,220),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,260),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,300),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,340),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,380),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,420),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(1, 2),50,460)]
Cooties = pygame.sprite.Group()
Licons = pygame.sprite.Group()
#creating the loading icon
loadingI = Loading_screen()
Licons.add(loadingI)
Cooties.add(testCootie)
global WT
WT = []


def date_setup():
   global Days
   global dayindex
   global GetDates
   global carryOn
   global WT
   global startingcootie1 
   global startingcootie2 
   while GetDates:
      Day = Days[dayindex]
      print(Day)
      WT.append(Date_Weather(int('1990' + Day)))
      dayindex += 1
      if dayindex >= 100:
         dayindex = 0
         if (startingcootie1 == False and startingcootie2 == False):
            GetDates = False
            carryOn = True
      print(dayindex)

#create a new thread to some parts separate
futureweatherprediction = Thread(target = date_setup)
global selectedCootie1
global selectedCootie2
#launch the new thread to get the weather data while the game continues
futureweatherprediction.start()
mx = 0
my = 0
#make a variable that stops from reading a mouse click to many times
clickwait = 0
while GetDates:
   for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we can exit the while loop
      if event.type == pygame.MOUSEBUTTONDOWN:
         mx,my = event.pos        
         for cootie in testCootie:
            if cootie.rect.collidepoint(mx,my):
               if clickwait <=0:
                  if startingcootie2:
                     clickwait = 20
                     selectedCootie2 = cootie
                     print(selectedCootie2)
                     startingcootie2 = False
                  if startingcootie1:
                     clickwait = 20
                     selectedCootie1 = cootie
                     print(selectedCootie1)
                     startingcootie1 = False
                     startingcootie2 = True                     
   if clickwait > 0:
      clickwait -= 1
   if (startingcootie1 == False and startingcootie2 == False):
      for cootie in testCootie:
         if (cootie != selectedCootie1 and cootie != selectedCootie2):
            testCootie.remove(cootie)
            cootie.die()
   Cooties.update(False,0,0)
   Licons.update()
   

   #draw a loading screen   
   screen.fill(BLACK)
   Cooties.draw(screen)
   Licons.draw(screen)

   #--- Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
   

# -------- Main Program Loop -----------
while carryOn:
    # --- Limit to 60 frames per second
    clock.tick(60)
    print(clock)
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop 
# --- Game logic should go here
# --- Update
    if dayindex < 99:
       framesss += 1
       if framesss >= 60:
           dayindex += 1
           framesss = 0
    print(dayindex)
    #get the average temperature for the date we predicted
    #add the high and low of the day together
    Avg_WT = WT[dayindex][1] + WT[dayindex][2]
    #take the result and divide ir by two for the average
    Avg_WT = Avg_WT/2    
    # create a text surface object,
    # on which text is drawn on it.
    # deciding the text based on the input from the
    #machine learning model we made.
    if(Avg_WT >= 80):
        Temp = font.render('Hot', True, GREEN, RED)
        currentW = 'Hot'
    elif(Avg_WT > 60 and Avg_WT < 80):
        Temp = font.render('Ideal',True, GREEN, RED)
        currentW = 'Ideal'
    elif(Avg_WT <= 60):
        Temp = font.render('Cold', True, GREEN, RED)
        currentW = 'Cold'

    if(WT[dayindex][0] > 0.00 and Avg_WT < 32):
        Rain = font.render('Snow', True, RED, GREEN)
        currentT = 'Snow'
    elif(WT[dayindex][0] > 0.80):
        Rain = font.render('Storm', True, RED, GREEN)
        currentT = 'Storm'
    elif(WT[dayindex][0] < 0.80 and WT[dayindex][0] > 0.30):
        Rain = font.render('Wet', True, RED, GREEN)
        currentT = 'Wet'
    elif(WT[dayindex][0] <= 0.30):
        Rain = font.render('Dry', True, RED, GREEN)
        currentT = 'Dry'
    # create a rectangular object for the
    # text surface object
    textRect = Temp.get_rect()
    rainRect = Rain.get_rect() 
    # set the bottom right of the rectangular object.
    textRect.bottomright = (700, 500)
    rainRect.bottomright = (700, 450)
    #update all sprite in the weather group
    Weather_Sprites.update(currentT, currentW)
    Cooties.update(True,currentT, currentW)  
    
# --- Drawing code should go here
    # First, clear the screen to white.
    screen.fill(BLACK)
    #draw test cootie
    Cooties.draw(screen)
    # draw all sprites in the weather group to the screen
    Weather_Sprites.draw(screen)
    
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(Temp, textRect)
    screen.blit(Rain, rainRect)
 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
