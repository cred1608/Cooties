#import our files
from MLModel import Date_Weather
import Cootie as CT
# Import the pygame library and initialise the game engine
import datetime
from threading import Thread
import random
import pygame
pygame.init()

WIDTH = 800
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
#set the window size name and icon
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cooties")
CootiesIcon = pygame.image.load("Ui_sprites/CootiesIcon.PNG")
pygame.display.set_icon(CootiesIcon)
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

#Three Game States
global GetDates
GetDates = True
global carryOn
carryOn = False
global simOver
simOver = False

#starting variables to pick cooties
global startingcootie1
startingcootie1 = True
global startingcootie2
startingcootie2 = False 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
global spite_spd
sprite_spd = clock.tick(60)
global CootieCount
global ShowSight
ShowSight = False

#set todays date to start the next 30 years
base = datetime.datetime.today().date()
#make a list of dates for everyday for the next 30 years so 9624 samples
date_list = [base + datetime.timedelta(days=x) for x in range(9624)]
#turn the list into a list of strings to feed into the model
date_list_string = [d.strftime('%m%d') for d in date_list]
global Days
Days = date_list_string;
#Loading Game Background
BackGround = pygame.image.load("Ui_sprites/CootieBoard.png")
BackGroundRect = BackGround.get_rect()
BackGroundRect.center = (WIDTH/2, HEIGHT/2)
BackGroundAlpha = 0
#Ui Tools for selecting and viewing Cooties
detailFrame = pygame.image.load("Ui_sprites/cootieDetails.png")
detailFramerect = detailFrame.get_rect()
detailFramerect.center = (350,250)
Dfont = pygame.font.Font('freesansbold.ttf', 16)
Cootie1Frame = pygame.image.load("Ui_sprites/Cootie1picked.png")
Cootie2Frame = pygame.image.load("Ui_sprites/Cootie2picked.png")
Cootie1FrameRect = Cootie1Frame.get_rect()
Cootie2FrameRect = Cootie2Frame.get_rect()
Cootie1Frame = Cootie1Frame.convert_alpha()
Cootie2Frame = Cootie2Frame.convert_alpha()
global cootiedetails



#create a sprite class to hold our bg sprites
class BG_Weather(pygame.sprite.Sprite):
   #making a function in the class that runs when a new instance of this class is called
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       #create the image that will be drawn when the sprite is drawn  
       self.image = pygame.Surface((800, 500))
       #loading two images for the sprite
       self.RainSheet = pygame.image.load("weathersprites/RainSheet.png")
       self.DrySheet = pygame.image.load("weathersprites/DrySheet.png")
       self.HotSheet = pygame.image.load("weathersprites/SunRays.png")
       self.ColdSheet = pygame.image.load("weathersprites/frosted.png")
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
         if self.frame_time > 2:
            self.frame_time = 0
            self.image.fill(BLACK)
            self.frame += 1
         if self.frame >= 3:
            self.frame = 0
         self.image.blit(self.HotSheet, self.rect, ((WIDTH * self.frame),0, WIDTH, HEIGHT))
         self.image = self.image.convert_alpha()
         self.image.set_alpha(125)
      if Temp == 'Ideal':
         self.image.set_alpha(50)
      elif Temp == 'Cold':
         self.image.blit(self.ColdSheet, self.rect)
         self.image = self.image.convert_alpha()
      elif Temp == 'Hot':

         self.image = self.image.convert_alpha()
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

         

#make a group for the sprites that show the weather effects
Weather_Sprites = pygame.sprite.Group()
cur_weather = BG_Weather()
Weather_Sprites.add(cur_weather)

# make 10 test cootiea each test cootie has 12 inputs
                       #hardiness____________#leanness_____________#hottempered__________#coldTempered_________#Aquatic_______________#weight______________#size__________________#Maturity_____________#Appeal_________________#Gender_______________#Sight______________#X__#Y
testCootie = [CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),60,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),140,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),220,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),300,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),380,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),460,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),540,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),620,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),700,100, False, False),
              CT.Cootie(random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(0, 10),random.randint(5, 10),random.randint(0, 10),random.randint(1, 2),random.randint(100, 200),780,100, False, False)]
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
      WT.append(Date_Weather(int('2024' + Day)))
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
   global selectedCootie1
   global selectedCootie2
    # --- Limit to 60 frames per second
   clock.tick(60)
   oncootie = False
   for cootie in testCootie:
      if cootie.rect.collidepoint(pygame.mouse.get_pos()):
         cootiedetails = cootie
         oncootie = True
         #checks events and user input
   for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
            GetDates = False
            carryOn = False # Flag that we are done so we can exit the while loop
      if event.type == pygame.MOUSEBUTTONDOWN:
         for cootie in testCootie:
            if cootie.rect.collidepoint(pygame.mouse.get_pos()):
               if clickwait <=0:
                  if startingcootie2:
                     clickwait = 10
                     selectedCootie2 = cootie 
                     print(selectedCootie2)
                     startingcootie2 = False
                  if startingcootie1:
                     clickwait = 10
                     selectedCootie1 = cootie
                     print(selectedCootie1)                     
                     startingcootie1 = False
                     startingcootie2 = True

                     
   if startingcootie1 == False:
       for cootie in testCootie:
           if (cootie.gender == selectedCootie1.gender) and (cootie != selectedCootie1):
                 testCootie.remove(cootie)
                 cootie.die()
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
   if startingcootie1 == False:
        Cootie1FrameRect.bottomright = selectedCootie1.rect.center
        screen.blit(Cootie1Frame, Cootie1FrameRect)
   if startingcootie2 == False and startingcootie1 == False:
        Cootie2FrameRect.bottomright = selectedCootie2.rect.center
        screen.blit(Cootie2Frame, Cootie2FrameRect)
   Cooties.draw(screen)
   Licons.draw(screen)
   #draw detail frame and details
   if oncootie == True:
      screen.blit(detailFrame, detailFramerect)
      HTemperment = Dfont.render(("Hot Weather: " + str(cootiedetails.hot)),True,(0,0,0))
      HTemperRect = HTemperment.get_rect()
      HTemperRect.center = (350,175) 
      screen.blit(HTemperment, HTemperRect)
      CTemperment = Dfont.render(("Cold Weather: " + str(cootiedetails.cold)),True,(0,0,0))
      CTemperRect = CTemperment.get_rect()
      CTemperRect.center = (350,190)
      screen.blit(CTemperment, CTemperRect)
      Hardyness = Dfont.render(("Hardyness: " + str(cootiedetails.hardy)),True,(0,0,0))
      HardynessRect = Hardyness.get_rect()
      HardynessRect.center = (350,205)
      screen.blit(Hardyness, HardynessRect)
      Leanness = Dfont.render(("Leanness: " + str(cootiedetails.lean)),True,(0,0,0))
      LeannessRect = Hardyness.get_rect()
      LeannessRect.center = (350,220)
      screen.blit(Leanness, LeannessRect)
      CSize = Dfont.render(("Size: " + str(cootiedetails.size)),True,(0,0,0))
      CSizeRect = CSize.get_rect()
      CSizeRect.center = (350,235)
      screen.blit(CSize, CSizeRect)
      Adult = Dfont.render(("Adulthood: " + str(cootiedetails.maturity)),True,(0,0,0))
      AdultRect = Adult.get_rect()
      AdultRect.center = (350,250)
      screen.blit(Adult, AdultRect)
      Water = Dfont.render(("Aquatic: " + str(cootiedetails.aquatic)),True,(0,0,0))
      WaterRect = Water.get_rect()
      WaterRect.center = (350,265)
      screen.blit(Water, WaterRect)
      Cute = Dfont.render(("Appeal: " + str(cootiedetails.appeal)),True,(0,0,0))
      CuteRect = Cute.get_rect()
      CuteRect.center = (350,280)
      screen.blit(Cute, CuteRect)
      Sight = Dfont.render(("Vision: " + str(cootiedetails.sight)),True,(0,0,0))
      SightRect = Sight.get_rect()
      SightRect.center = (350, 295)
      screen.blit(Sight, SightRect)
      Old = Dfont.render(("Age: " + str(cootiedetails.age)),True,(0,0,0))
      OldRect = Old.get_rect()
      OldRect.center = (350, 310)
      screen.blit(Old, OldRect)
      Gen = Dfont.render(("Gender: " + str(cootiedetails.gender)),True,(0,0,0))
      GenRect = Gen.get_rect()
      GenRect.center = (350, 325)
      screen.blit(Gen, GenRect)
   #--- Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
   
# -------- Main Program Loop -----------
# The loop will carry on until the user exits the game (e.g. clicks the close button)
while carryOn:
    # --- Limit to 60 frames per second
    clock.tick(60)
    global CootieCount
    oncootie = False
    # --- Main event loop
    CootieCount = len(testCootie)
    if CootieCount == 1:
       carryOn = False
       simOver = True
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
           carryOn = False # Flag that we are done so we can exit the while loop

    for cootie in testCootie:
      if cootie.rect.collidepoint(pygame.mouse.get_pos()):
         cootiedetails = cootie
         oncootie = True
# --- Game logic should go here
# --- Update
    if dayindex < 99:
       framesss += 1
       if framesss >= 60:
           dayindex += 1
           framesss = 0
    elif dayindex == 99:
       dayindex = 0
    print(dayindex)
    #get the average temperature for the date we predicted
    #add the high and low of the day together
    if (WT[dayindex][1] - 75) > (75 - WT[dayindex][2]):
       Avg_WT = WT[dayindex][1]
    elif (WT[dayindex][1] - 75) < (75 - WT[dayindex][2]):
       Avg_WT = WT[dayindex][2]
    else:
       Avg_WT = WT[dayindex][1] + WT[dayindex][2]
       
       
    #take the result and divide it by two for the average
    #Avg_WT = Avg_WT/2    
    # create a text surface object,
    # on which text is drawn on it.
    # deciding the text based on the input from the
    #machine learning model we made.
    if(Avg_WT >= 80):
        Temp = font.render('Hot', True, GREEN, RED)
        currentW = 'Hot'
    elif(Avg_WT > 70 and Avg_WT < 80):
        Temp = font.render('Ideal',True, GREEN, RED)
        currentW = 'Ideal'
    elif(Avg_WT <= 70):
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
    
    #for loop to go though the cooties
    for cootie in testCootie:
       cootie.populationcontrol(CootieCount)
       if cootie.dead == True:
          testCootie.remove(cootie)

      #check cootie to see if they mate   
       if cootie.mate == True:
          CootiesChecked = 0
          tempCootie = None
          tempFound = False
          #looking at all other cooties in their sight range
          for mate in testCootie:
            CootiesChecked += 1

            if cootie.sightrect.colliderect(mate.rect) and CootiesChecked  > 1 and tempFound == True:
                 #making sure they didnt find themsekve and that are the opposite gender 
                if cootie != mate and (cootie.gender != mate.gender):
                   #looking for the best looking cootie that hasnt already mated with someone else  
                   if mate.appeal > tempCootie.appeal and mate.taken == False:
                      tempCootie = mate
            else:
                if cootie != mate and (cootie.gender != mate.gender):              
                  tempCootie = mate
                  tempFound = True
            if CootiesChecked >= CootieCount:
                   cootie.cootieMate = tempCootie
                   if cootie.pregnant == False:
                      cootie.ismate()
                      mate.taken = True
       if cootie.deliver == True:
          while cootie.birthed < cootie.numoospring:
             cootie.birthed += 1
             HLCH = cootie.Inheretence(mate)
                                           #0_______1_______2______3_________4_____________________5____________________6_________7______8__________9_____10_________________+____11__________12
             testCootie.append(CT.Cootie(HLCH[0],HLCH[1],HLCH[2],HLCH[3],HLCH[7],random.randint(0, 10),HLCH[6],HLCH[10],HLCH[9],random.randint(1, 2),HLCH[8],cootie.x,cootie.y,HLCH[4],HLCH[5]))
             Cooties.add(testCootie)
          cootie.deliver = False   
          mate.taken = False
 # --- Drawing code should go here
    # First, clear the screen to black
    screen.fill(BLACK)
    #draw the background
    if (BackGroundAlpha < 255):
       BackGroundAlpha += 1
       BackGround.set_alpha(BackGroundAlpha)
    screen.blit(BackGround, BackGroundRect)
    #draw test cootie
    Cooties.draw(screen)
    # draw all sprites in the weather group to the screen
    Weather_Sprites.draw(screen)
    
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(Temp, textRect)
    screen.blit(Rain, rainRect)

    if oncootie == True:
      screen.blit(detailFrame, detailFramerect)
      HTemperment = Dfont.render(("Hot Weather: " + str(cootiedetails.hot)),True,(0,0,0))
      HTemperRect = HTemperment.get_rect()
      HTemperRect.center = (350,175) 
      screen.blit(HTemperment, HTemperRect)
      CTemperment = Dfont.render(("Cold Weather: " + str(cootiedetails.cold)),True,(0,0,0))
      CTemperRect = CTemperment.get_rect()
      CTemperRect.center = (350,190)
      screen.blit(CTemperment, CTemperRect)
      Hardyness = Dfont.render(("Hardyness: " + str(cootiedetails.hardy)),True,(0,0,0))
      HardynessRect = Hardyness.get_rect()
      HardynessRect.center = (350,205)
      screen.blit(Hardyness, HardynessRect)
      Leanness = Dfont.render(("Leanness: " + str(cootiedetails.lean)),True,(0,0,0))
      LeannessRect = Hardyness.get_rect()
      LeannessRect.center = (350,220)
      screen.blit(Leanness, LeannessRect)
      CSize = Dfont.render(("Size: " + str(cootiedetails.size)),True,(0,0,0))
      CSizeRect = CSize.get_rect()
      CSizeRect.center = (350,235)
      screen.blit(CSize, CSizeRect)
      Adult = Dfont.render(("Adulthood: " + str(cootiedetails.maturity)),True,(0,0,0))
      AdultRect = Adult.get_rect()
      AdultRect.center = (350,250)
      screen.blit(Adult, AdultRect)
      Water = Dfont.render(("Aquatic: " + str(cootiedetails.aquatic)),True,(0,0,0))
      WaterRect = Water.get_rect()
      WaterRect.center = (350,265)
      screen.blit(Water, WaterRect)
      Cute = Dfont.render(("Appeal: " + str(cootiedetails.appeal)),True,(0,0,0))
      CuteRect = Cute.get_rect()
      CuteRect.center = (350,280)
      screen.blit(Cute, CuteRect)
      Sight = Dfont.render(("Vision: " + str(cootiedetails.sight)),True,(0,0,0))
      SightRect = Sight.get_rect()
      SightRect.center = (350, 295)
      screen.blit(Sight, SightRect)
      Old = Dfont.render(("Age: " + str(cootiedetails.age)),True,(0,0,0))
      OldRect = Old.get_rect()
      OldRect.center = (350, 310)
      screen.blit(Old, OldRect)
      Gen = Dfont.render(("Gender: " + str(cootiedetails.gender)),True,(0,0,0))
      GenRect = Gen.get_rect()
      GenRect.center = (350, 325)
      screen.blit(Gen, GenRect)


    #show how many cooties we have
    CCShow = Dfont.render(("Cooties: " + str(CootieCount)),True,(0,0,0), WHITE)
    CCSRect = CCShow.get_rect()
    CCSRect.center = (750,15)
    screen.blit(CCShow, CCSRect)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
 
#Once we have exited the main program loop we can stop the game engine:
while simOver:
   
    oncootie = False
             #checks events and user input
    for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
            simOver = False # Flag that we are done so we can exit the while loop  
    for cootie in testCootie:
      if cootie.rect.collidepoint(pygame.mouse.get_pos()):
         cootiedetails = cootie
         oncootie = True  
    # First, clear the screen to black
    screen.fill(BLACK)
    # Draw Background again.
    screen.blit(BackGround, BackGroundRect)
    #draw test cootie
    Cooties.draw(screen)  
    if oncootie == True:
      screen.blit(detailFrame, detailFramerect)
      HTemperment = Dfont.render(("Hot Weather: " + str(cootiedetails.hot)),True,(0,0,0))
      HTemperRect = HTemperment.get_rect()
      HTemperRect.center = (350,175) 
      screen.blit(HTemperment, HTemperRect)
      CTemperment = Dfont.render(("Cold Weather: " + str(cootiedetails.cold)),True,(0,0,0))
      CTemperRect = CTemperment.get_rect()
      CTemperRect.center = (350,190)
      screen.blit(CTemperment, CTemperRect)
      Hardyness = Dfont.render(("Hardyness: " + str(cootiedetails.hardy)),True,(0,0,0))
      HardynessRect = Hardyness.get_rect()
      HardynessRect.center = (350,205)
      screen.blit(Hardyness, HardynessRect)
      Leanness = Dfont.render(("Leanness: " + str(cootiedetails.lean)),True,(0,0,0))
      LeannessRect = Hardyness.get_rect()
      LeannessRect.center = (350,220)
      screen.blit(Leanness, LeannessRect)
      CSize = Dfont.render(("Size: " + str(cootiedetails.size)),True,(0,0,0))
      CSizeRect = CSize.get_rect()
      CSizeRect.center = (350,235)
      screen.blit(CSize, CSizeRect)
      Adult = Dfont.render(("Adulthood: " + str(cootiedetails.maturity)),True,(0,0,0))
      AdultRect = Adult.get_rect()
      AdultRect.center = (350,250)
      screen.blit(Adult, AdultRect)
      Water = Dfont.render(("Aquatic: " + str(cootiedetails.aquatic)),True,(0,0,0))
      WaterRect = Water.get_rect()
      WaterRect.center = (350,265)
      screen.blit(Water, WaterRect)
      Cute = Dfont.render(("Appeal: " + str(cootiedetails.appeal)),True,(0,0,0))
      CuteRect = Cute.get_rect()
      CuteRect.center = (350,280)
      screen.blit(Cute, CuteRect)
      Sight = Dfont.render(("Vision: " + str(cootiedetails.sight)),True,(0,0,0))
      SightRect = Sight.get_rect()
      SightRect.center = (350, 295)
      screen.blit(Sight, SightRect)
      Old = Dfont.render(("Age: " + str(cootiedetails.age)),True,(0,0,0))
      OldRect = Old.get_rect()
      OldRect.center = (350, 310)
      screen.blit(Old, OldRect)
      Gen = Dfont.render(("Gender: " + str(cootiedetails.gender)),True,(0,0,0))
      GenRect = Gen.get_rect()
      GenRect.center = (350, 325)
      screen.blit(Gen, GenRect)  
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
   
pygame.quit()
