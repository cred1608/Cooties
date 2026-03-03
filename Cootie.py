import pygame
import random
pygame.init()



# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (  0,  0,  255)


#cootie creature class file
class Cootie(pygame.sprite.Sprite):
   def __init__(self,hardy,lean,hot,cold,aquatic,weight,size,maturity,appeal,gender,sight,x,y,mark1,mark2):      
      pygame.sprite.Sprite.__init__(self)
      #making an empty sprite to draw the cooties on 
      #setting the largest size the cootie will be      
      self.image = pygame.Surface((100, 100))
      self.rect = self.image.get_rect()
      
      #The cooties position on screen 
      self.x = x
      self.y = y
      
      #loading the different Cootie parts
      self.cootieBody = pygame.image.load("Cooties/cootiebody.png")
      self.cootieEyes = pygame.image.load("Cooties/cootieeyes.png")
      self.cootieFinL = pygame.image.load("Cooties/cootiefinl.png")
      self.cootieFinR = pygame.image.load("Cooties/cootiefinr.png")
      self.marking1 = pygame.image.load("Ui_sprites/Cootie1.png")
      self.marking2 = pygame.image.load("Ui_sprites/Cootie2.png")
      #making a directions variable that is used to turn and control
      #the direction the cootie is moving
      self.dir = 0
      self.center = 50
      #setting rect for all the cootie body parts
      self.cootieBodyrect = self.cootieBody.get_rect()
      self.cootieEyesrect = self.cootieEyes.get_rect()
      self.cootieFinLrect = self.cootieFinL.get_rect()
      self.cootieFinRrect = self.cootieFinR.get_rect()
      self.marking1Rect = self.marking1.get_rect()
      self.marking2Rect = self.marking2.get_rect()
      #setting the poistions in respect to the Cootie image surface
      self.cootieBodyrect.center = (self.rect.center)
      self.cootieEyesrect.center = (50, 50)
      self.cootieFinLrect.bottomright = (41,75)
      self.cootieFinRrect.bottomleft = (60,75)
      self.marking1Rect.center = self.rect.center
      self.marking2Rect.center = self.rect.center
      #setting any black parts of the body parts to be clear
      self.cootieBody.set_colorkey(BLACK)
      self.cootieEyes.set_colorkey(BLACK)
      self.cootieFinL.set_colorkey(BLACK)
      self.cootieFinR.set_colorkey(BLACK)
      self.marking1.set_colorkey(BLACK)
      self.marking2.set_colorkey(BLACK)
      #variables used for animating the cooties
      self.contracted = False
      self.aniTimer = 0
      #variable to set whether the cootie is alive or dead
      self.dead = False
      #add the attributes to be passed down
      self.hardy = hardy
      self.lean = lean
      self.hot = hot
      self.cold = cold
      self.aquatic = aquatic
      self.weight = weight
      self.size = size
      self.maturity = maturity
      self.appeal = appeal
      self.gender = gender
      self.marked1 = mark1
      self.marked2 = mark2
      
      #health/age variables
      self.hp = 100
      self.det = 5
      self.age = 0
      self.ageSpeed = 15
     

      #reproduction variables
      self.sight = sight
      self.carrying = 0
      self.mate = False
      self.pregnant = False
      self.deliver = False
      self.gestation = 3
      self.birthed = 0; 
      self.cootieMate = self
      self.numoospring = 0  
      self.sightrect = pygame.Rect(0,0,sight,sight)
      self.pChance = 125
      self.taken = False

      #variables to be passed on
      self.Ohot = 0
      self.Ocold = 0
      self.Osight = 0
      self.Ohardy = 0
      self.Olean = 0
      self.Oaquatic = 0
      self.Oappeal = 0
      self.Osize = 0
      self.Osight = 0
      self.Omaturity = 0
      self.Omarked1 = False
      self.Omarked2 = False
      
      
      
      #create red colored eyes based on sight value
      self.cootieEyes.fill((self.sight,0,0,255),special_flags=pygame.BLEND_MULT)
      #create pink fins depending on the appeal value
      self.cootieFinL.fill((0,255/(11 - self.appeal),0,255),special_flags=pygame.BLEND_SUB)
      self.cootieFinR.fill((0,255/(11 - self.appeal),0,255),special_flags=pygame.BLEND_SUB) 
      #variable to control how long the cootie waits to change direction  
      self.moveWait = 0 
      #variables to control the cooties size         
      sizeChange = 0
      newWidth = 0
      newLength = 0
      movestuff = 0
      Eyex = 0
      Lfinx = 0
      Rfinx = 0

      #use hardy and lean values to determine the width of the Cootie\
      sizeChangel = 0
      sizeChangeh = 0
      if self.hardy > 0:
         sizeChangeh = self.cootieBodyrect.width /(11 - self.hardy)
       
      if self.lean > 0:
         sizeChangel = self.cootieBodyrect.width /(11 - self.lean)
         newWidth = self.cootieBodyrect.width - sizeChange

      newWidth = self.cootieBodyrect.width - sizeChangel
      newWidth = newWidth + sizeChangeh

      if newWidth <= 20:
         newWidth = 20
      #scale the fins based on how aquatic the cootie is.
      finsize = 25-(11 - self.aquatic)
      self.cootieFinL = pygame.transform.scale(self.cootieFinL,(25,finsize))
      self.cootieFinR = pygame.transform.scale(self.cootieFinR,(25,finsize))
      print(newWidth)
      self.cootieBody = pygame.transform.scale(self.cootieBody,(newWidth, 50))
      #adjusting the position of the eyes and flippers to the new cootie size
      if newWidth < 50:
         sizeDif = 50 - newWidth       
         self.cootieEyes = pygame.transform.scale(self.cootieEyes,(newWidth, 50))
         Rfinx = 60 - sizeDif
         Lfinx = 41
         self.cootieFinRrect.bottomleft = (Rfinx - sizeDif,75)
         self.cootieFinLrect.bottomright = (Lfinx,75)
      if newWidth > 50:
         sizeDif = newWidth - 50
         self.cootieEyes = pygame.transform.scale(self.cootieEyes,(newWidth, 50))
         self.center = 40
         self.cootieBodyrect.center = (self.center, 50)
         self.cootieEyesrect.center = (self.center, 50)
         Rfinx = 60 + (sizeDif - 10)
         Lfinx = 41 - 10
         self.cootieFinRrect.bottomleft = (Rfinx ,75)
         self.cootieFinLrect.bottomright = (Lfinx,75)
      if newWidth > 75:
         self.center = 30
         self.cootieBodyrect.center = (self.center, 50)
         self.cootieEyesrect.center = (self.center, 50)
         Rfinx = 60 + (sizeDif - 20)
         Lfinx = 41 - 20
         self.cootieFinRrect.bottomleft = (Rfinx ,75)
         self.cootieFinLrect.bottomright = (Lfinx,75)
      if newWidth == 50:
         Rfinx = 60
         Lfinx = 41
         self.cootieFinRrect.bottomleft = (Rfinx,75)
         self.cootieFinLrect.bottomright = (Lfinx,75)
         
      #use size to determine the length of the cootie
      sizeChange = 0  
      if self.size > 0:  
          sizeChange = self.cootieBodyrect.height/(11 - self.size)
      newLength = self.cootieBodyrect.height + sizeChange    
      self.cootieBody = pygame.transform.scale(self.cootieBody,(newWidth, newLength))  
      #adjusting the position of the fins and eyes to match the new length  
      if newLength > 50:
        sizedif = newLength - 50
        self.cootieBodyrect.center = (self.center,40) 
        self.cootieFinRrect.bottomleft = (Rfinx,65 + sizedif)
        self.cootieFinLrect.bottomright = (Lfinx,65 + sizedif)
        self.cootieEyesrect.center = (self.center, 40 + sizedif)
      if newLength > 60:
        self.cootieBodyrect.center = (self.center,30) 
        self.cootieFinRrect.bottomleft = (Rfinx,55 + sizedif)
        self.cootieFinLrect.bottomright = (Lfinx,55 + sizedif)
        self.cootieEyesrect.center = (self.center, 30 + sizedif)
      if newLength > 70:
        self.cootieBodyrect.center = (self.center,20) 
        self.cootieFinRrect.bottomleft = (Rfinx,45 + sizedif)
        self.cootieFinLrect.bottomright = (Lfinx,45 + sizedif)
        self.cootieEyesrect.center = (self.center, 20 + sizedif)
      #adding all the sprites to the image  
      self.image.blit(self.cootieBody, self.cootieBodyrect)
      self.image.fill(((255/(11 - self.hot)),0,(255/(11 - self.cold)),255),special_flags=pygame.BLEND_RGBA_MULT)
      self.image.blit(self.cootieFinL, self.cootieFinLrect)
      self.image.blit(self.cootieFinR, self.cootieFinRrect)
      self.image.blit(self.cootieEyes, self.cootieEyesrect)
      self.image.set_colorkey(BLACK)
      if self.marked1 == True:
         self.image.blit(self.marking1, self.marking1Rect)
      if self.marked2 == True:
         self.image.blit(self.marking2, self.marking2Rect)
      self.image = pygame.transform.scale(self.image,(50,50))
      self.baseimage = self.image    
      #adjusting the speed of ageing based on stats  
      if self.hardy > 0:
          self.ageSpeed = self.ageSpeed + self.hardy
      if self.lean > 0 :
          self.ageSpeed = self.ageSpeed - self.lean
      #adjusting the amount of health lost do to being hardy or lean
      if self.lean > 0 and self.lean < 5:
         self.det += 2
      elif self.lean > 5:
         self.det += 3
      if self.hardy > 0 and self.hardy < 5:
         self.det -= 2
      elif self.hardy > 5:
         self.det -= 3

         
   def die(self):    
       self.dead = True
       self.kill() 

             
   def ismate(self):
       self.pregnant = True

   def populationcontrol(self,pop):
      if pop < 10:
         self.pChance = 50
      elif pop >= 10 and pop < 200:
         self.pChance = 125
      elif pop >= 200:
         self.pChance = 350
      
   def Inheretence(self,mate):
      #inheretence for hot or cold natured
      if self.hot > self.cold and self.hot > mate.cold:
         temp = self.hot - mate.cold
         self.Ohot = random.randint(temp + mate.hot, self.hot + mate.hot)
         self.Ocold = random.randint(0, temp)
      elif mate.hot > mate.cold and mate.hot > self.cold:
         temp = mate.hot - self.cold
         self.Ohot = random.randint(temp + self.hot, mate.hot + self.hot)
         self.Ocold = random.randint(0, temp)
      if self.cold > self.hot and self.cold > mate.hot:
         temp = self.cold - mate.hot
         self.Ocold = random.randint(temp + mate.cold, self.cold + mate.cold)
         self.Ohot = random.randint(0, temp)
      elif mate.cold > mate.hot and mate.cold > self.hot:
         temp = mate.cold - self.hot
         self.Ocold = random.randint(temp - self.cold, mate.cold + self.cold)
         self.Ohot = random.randint(0, temp)    
      if self.cold == self.hot and self.cold == mate.hot or mate.cold == mate.hot and mate.cold == self.hot:
         self.Ohot = random.randint(0, self.hot)
         self.Ocold = random.randint(0, self.cold)
      if self.Ohot > 10:
         self.Ohot = 10
      if self.Ohot < 0:
         self.Ohot = 0   
      if self.Ocold < 0:
         self.Ocold = 0
      if self.Ocold > 10:
         self.Ocold = 10
      #inheretence for hardy or lean attributes
      if self.hardy > self.lean and self.hardy > mate.lean:
          temp = self.hardy - self.lean
          self.Ohardy = random.randint(temp, self.hardy)
          self.Olean = random.randint(0, temp)
      elif mate.hardy > mate.lean and mate.hardy > self.lean:
         temp = mate.hardy - self.lean
         self.Ohardy = random.randint(temp, mate.hardy)
         self.Olean = random.randint(0, temp)
      if self.lean > self.hardy and self.lean > mate.hardy:
         temp = self.lean - mate.hardy
         self.Olean = random.randint(temp, self.lean)
         self.Ohardy = random.randint(0, temp)
      elif mate.lean > mate.hardy and mate.lean > self.hardy:
         temp = mate.lean - self.hardy
         self.Olean = random.randint(temp, mate.lean)
         self.Ohardy = random.randint(0, temp)    
      elif self.cold == self.hot and self.cold == mate.hot or mate.cold == mate.hot and mate.cold == self.hot:
         self.Ohardy = 5
         self.Olean = 5
      if self.marked1 == True or mate.marked1 == True:
         self.Omarked1 = True
      if self.marked2 == True or mate.marked2 == True:
         self.Omarked2 = True   
      #inheretence for size
      if self.size >= mate.size:
            self.Osize = random.randint(mate.size, self.size)
      elif mate.size > self.size:
            self.Osize = random.randint(self.size, mate.size)
      #inheretence for aquatic amount  
      if self.aquatic >= mate.aquatic:
            self.Oaquatic = random.randint(mate.aquatic, self.aquatic)
      elif mate.aquatic > self.aquatic:
            self.Oaquatic = random.randint(self.aquatic, mate.aquatic)
     #inheretence for the sight of the cootie:
      if self.sight >= mate.sight:
            self.Osight = random.randint(mate.sight, self.sight)
      elif mate.sight > self.sight:
            self.Osight = random.randint(self.sight, mate.sight)
      #inheretence foe appeal of the Cootie
      if self.appeal >= mate.appeal:
            self.Oappeal = random.randint(mate.appeal, self.appeal)
      elif mate.appeal > self.appeal:
            self.Oappeal = random.randint(self.appeal, mate.appeal)
      #inheretence foe Maturity of the Cootie
      if self.maturity >= mate.maturity:
            self.Omaturity = random.randint(mate.maturity, self.maturity)
      elif mate.maturity > self.maturity:
            self.Omaturity = random.randint(self.maturity, mate.maturity)             
               #0____________1_________2____________3____________4____________5_____________6______________7____________8_____________9_____________10_______  
      return self.Ohardy, self.Olean, self.Ohot, self.Ocold, self.Omarked1, self.Omarked2, self.Osize, self.Oaquatic, self.Osight, self.Oappeal, self.Omaturity




   ageTime = 0
   def update(self,ud,weather,temp):         
      self.rect.center = (self.x, self.y)
      OL = self.cootieBodyrect.height
      OW = self.cootieBodyrect.width
      self.aniTimer += 1
      if self.aniTimer >= 10:
           self.aniTimer = 0 
      if ud == False:
         self.x = self.x
         self.y = self.y
      elif ud == True:
        #age and slowly kill the cooties
         self.ageTime += 1
         if self.ageTime > self.ageSpeed:
             self.age += 1
             self.ageTime = 0
             eDmg = 0
             if self.age >= (self.maturity):
                self.hp -= self.det
           #use weather to adjust the rate at which the cooties die     
             if self.cold > 0 and self.cold < 5:
                   if temp == 'Hot':
                      eDmg = 2              
             elif self.cold >= 5:
                   if temp == 'Hot':
                      eDmg = 4
             if eDmg > 0:
                self.hp -= eDmg          
             if self.hot > 0 and self.hot < 5:
                   if temp == 'Cold':
                      eDmg = 2
             elif self.hot >= 5:
                   if temp == 'Cold':
                      eDmg = 4
             if eDmg > 0:
                self.hp -= eDmg 
             if self.aquatic > 0 and self.aquatic < 5:
                if weather == 'Dry':
                   eDmg = 1
             elif  self.aquatic >= 5:
                if weather == 'Dry':
                   eDmg = 2      
             elif self.aquatic <= 0:
                if weather == 'Wet':
                   eDmg = 2
             if eDmg > 0:
                self.hp -= eDmg
         #checks if the health of the cootie is 0 then kills it       
         if self.hp <= 0:
             self.die()
         #checks if a Cootie is old enough to reproduce then gives it a slight random chance to get pregnant
             #only if it is a certain gender
         if self.age >= self.maturity and self.mate == False and self.age < 40 and self.gender == 2:
            mateTime = random.randint(1,self.pChance)
            if mateTime == 2:
               self.mate = True           
            self.sightrect.center = self.rect.center
            #adds time to the pregnancies
         if self.pregnant == True:
            if self.ageTime >= 5:
               self.carrying += 1
            if self.carrying >= self.gestation:
               self.deliver = True
               self.numoospring = random.randint(1, 4)
               self.pregnant = False
               self.carrying = 0

            # the movement direction code
         self.moveWait += 1
         if self.moveWait >= 20:
            self.dir = random.randint(1,4)
            self.moveWait = 0
         if self.dir == 1:
            self.image = pygame.transform.rotate(self.baseimage, 180)
            if self.y <= 50:
                self.dir = 3
            elif self.y > 50:
               self.y -= 1
         elif self.dir == 2:
            self.image = pygame.transform.rotate(self.baseimage, 90)
            if self.x >= 650:
               self.dir = 4
            elif self.x < 650:
               self.x += 1       
         elif self.dir == 3:
            self.image = pygame.transform.rotate(self.baseimage, 360)
            if self.y >=450:
               self.dir = 1
            elif self.y < 450:
               self.y += 1
         elif self.dir == 4:
            self.image = pygame.transform.rotate(self.baseimage, 270) 
            if self.x <= 50:
               self.dir = 2
            elif self.x > 50:
               self.x -= 1
               

