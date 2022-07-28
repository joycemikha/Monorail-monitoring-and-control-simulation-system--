import pygame
from pygame.locals import *
import time

class train:
      
    def __init__(self, id,screen,newx,newy,x,y,start_time):
        self.id = id
        self.k=1
        self.k2=1
        self.screen = screen
        self.newx=newx
        self.newy=newy
        self.accelerationx=0
        self.accelerationy=0
        self.flagspeed = 1 #whyyy
        self.speed=1
        self.x = x 
        self.y = y 
        self.start_time=start_time 
        self.xflage=None #start engines
        self.flag1=0    #flag for transfering to the other lane
        self.flagStop=0 #flag for when the train stop at emergency lane
        self.end_time=0
        self.Ex1=0      #coordinate x when the train called for emergency
        self.flagE=0    #flag for emergency
        self.Ey1=0      #coordinate y when the train called for emergency
        self.flagcx=0   #flag to make other trains move if it enters first emergency lane
        self.flagcontinue = 0 #continue if first train didnot pass third station however it got into first emergency lane
        self.flagx = 0   
        self.flagmov = 0 #flag for every train when to start moving
        self.endprocess=0#flag for ending the day and getting back to start stations
        self.backward=0
        self.f=0
        self.positionflg=0
        self.fl=1
        self.history=0
        self.trips=0
        
    def west_move(self):
        if (self.xflage == 'start' and self.flag1 == 0 and self.x < 1470 and self.flagStop == 0 and self.flagmov == 1):
            self.end_time = time.time()
            #print(self.id,self.flagspeed)
            if self.end_time - self.start_time >= 1:
                if self.backward==0:
                    self.accelerationx=1*(self.speed)
                    self.x = self.x + self.accelerationx
                if (self.Ex1 > 0 and self.Ex1 < 386 and self.flagE == 1 and self.backward==0):
                    if (self.x >= 386 and self.backward==0):
                        if (self.y >= 280):
                            self.accelerationy=1.4*(self.speed)
                            self.y = self.y - self.accelerationy
                        self.accelerationx=0.5*(self.speed)
                        self.x = self.x - self.accelerationx
                        if (self.y < 280 and self.x > 450 and self.backward==0):
                            self.flagStop = 1
                            self.flagcx = 1
                if (self.Ex1 > 386 and self.Ex1 < 790 and self.flagE == 1 and self.backward==0):
                    if (self.x >= 790 and self.backward==0):
                        if (self.y >= 280 and self.backward==0):
                            self.accelerationy=1.4*(self.speed)
                            self.y= self.y- self.accelerationy
                        self.accelerationx=0.5*(self.speed)
                        self.x= self.x- self.accelerationx
                        if (self.y < 280 and self.x> 840 and self.backward==0):
                            self.flagStop = 1
                            self.flagcx = 1
                if (self.x < 111 and self.y >= 214 and self.backward==0):
                    self.accelerationy=0.16*(self.speed)
                    self.y = self.y - self.accelerationy
                if (self.y < 213 and self.backward==0):
                    self.accelerationy=0.08*(self.speed)
                    self.y = self.y + self.accelerationy
                if (self.y > 211 and self.y < 310 and self.x > 110 and self.x < 250 and self.backward==0):
                    self.accelerationy=0.70*(self.speed)
                    self.y = self.y + self.accelerationy
                if (self.x > 250 and self.x < 450 and self.backward==0):
                    self.accelerationy=0.048*(self.speed)
                    self.y = self.y + self.accelerationy
                if (self.x > 1270 and self.x < 1470 and self.backward==0):
                    self.accelerationy=0.6*(self.speed)
                    self.y = self.y - self.accelerationy 
                if self.endprocess == 1:
                    if (self.x < 112 and self.x > 15 )  and (self.y < 216):
                        
                        self.accelerationx=1*(self.speed)
                        self.x = self.x - self.accelerationx
                        self.accelerationy=0.1*(self.speed)
                        self.y = self.y - self.accelerationy
                        self.backward=1
                        if self.x <= 15:
                            if self.fl==0:
                                    self.flagmov=0
            if ((self.x > 111 and self.x < 113) or (self.x > 250 and self.x < 252) or (self.x > 450 and self.x < 452) or (self.x > 650 and self.x < 652) or (self.x > 850 and self.x < 852) or (self.x > 1050 and self.x < 1052) or (self.x > 1269 and self.x < 1271)  or (self.x > 1369 and self.x < 1371) or (self.x > 1469 and self.x < 1471)):
                self.start_time = time.time()
                self.accelerationx=1*(self.speed)
                self.x += self.accelerationx
        if (self.x > 1470 and self.x < 1472):
            self.flag1 = 1

        if (self.xflage == 'start' and self.flag1 == 1 and self.flagStop == 0):
            if (self.x > 13):
                self.end_time = time.time()
                if self.end_time - self.start_time >= 1:
                    self.accelerationx=1*(self.speed)
                    self.x= self.x- self.accelerationx
                    if (self.x < 1773 and self.x> 1376):
                        self.accelerationy=0.23*(self.speed)
                        self.y= self.y+ self.accelerationy
                    if (self.x <= 110):
                        self.accelerationy=0.10*(self.speed)
                        self.y= self.y- self.accelerationy
                    if (self.x > 110 and self.x< 250):
                        self.accelerationy=0.74*(self.speed)
                        self.y= self.y- self.accelerationy
                    if (self.x > 1275 and self.x< 1050):
                        self.accelerationy=0.048*(self.speed)
                        self.y= self.y+ self.accelerationy
                    if (self.x > 1275 and self.x< 1473):
                        self.accelerationy=0.61*(self.speed)
                        self.y= self.y+ self.accelerationy
                    if (self.x <= 15):
                        self.flag1 = 0

                    if ((self.Ex1 < 1500 and self.Ex1 > 1113 and self.flagE == 1 ) or (self.Ex1 > 890 and self.Ey1 <= 321  and self.flagE == 1)):
                        if (self.x <= 1113):
                            if (self.y <= 378):
                                self.accelerationy=1.4*(self.speed)
                                self.y= self.y+ self.accelerationy
                            self.accelerationx=0.5*(self.speed)
                            self.x= self.x+ self.accelerationx
                            if (self.y >= 378 and self.x< 1060):
                                self.flagStop = 1
                                self.flagcx = 1
                    if (self.Ex1 < 1113 and self.Ex1 > 710 and self.Ey1 > 325 and self.flagE == 1):
                        if (self.x <= 710):
                            if (self.y <= 378):
                                self.accelerationy=1.4*(self.speed)
                                self.y= self.y+ self.accelerationy
                            self.accelerationx=0.5*(self.speed)
                            self.x= self.x+ self.accelerationx
                            if (self.y >= 378 and self.x< 660):
                                self.flagStop = 1

                if ((self.x > 1373 and self.x < 1375) or (self.x > 1274 and self.x < 1276) or (self.x > 1049 and self.x < 1051) or (self.x > 849 and self.x < 851) or (self.x > 649 and self.x < 651) or (self.x > 449 and self.x < 451)  or (self.x > 249 and self.x < 251) or (self.x > 109 and self.x < 111) or (self.x > 14 and self.x < 16)):
                    self.start_time = time.time()
                    self.accelerationx=1*(self.speed)
                    self.x-= self.accelerationx
    def west_implement(self):
        self.west_move()
        return pygame.draw.circle(self.screen, 	(0,0,0), (self.x*self.newx, self.y*self.newy),5, 0)
    def east_move(self):
        
        if (self.xflage == 'start' and self.flag1 == 0 and self.x > 15 and self.flagStop == 0 and self.flagmov ==1):
            self.end_time = time.time()
            if self.end_time - self.start_time >= 1:
                if self.backward==0:
                    self.accelerationx=1*(self.speed)
                    self.x = self.x - self.accelerationx
                if ((self.Ex1 < 1500 and self.Ex1 > 1113 and self.flagE == 1) or (self.Ex1 > 890 and self.Ey1 <= 321 and self.flagE == 1)):
                    if  (self.x <= 1113 and self.backward==0):
                        if (self.y <= 378):
                            self.accelerationy=1.4*(self.speed)
                            self.y = self.y + self.accelerationy
                        self.accelerationx=0.5*(self.speed)
                        self.x = self.x + self.accelerationx
                        if (self.y >= 378 and self.x < 1060 and self.backward==0):
                            self.flagStop = 1
                            self.flagcx = 1
                if (self.Ex1 < 1113 and self.Ex1 > 710 and self.Ex1 > 325 and self.flagE == 1 and self.backward==0):
                    if  (self.x <= 710):
                        if (self.y <= 378):
                            self.accelerationy=1.4*(self.speed)
                            self.y = self.y + self.accelerationy
                        self.accelerationx=0.5*(self.speed)
                        self.x = self.x + self.accelerationx
                        if (self.y >= 378 and self.x < 660):
                            self.flagStop = 1
                            self.flagcx = 1
                if  (self.x <= 110 and self.backward==0):
                    self.accelerationy=0.10*(self.speed)
                    self.y = self.y - self.accelerationy
                if  (self.x > 110 and self.x < 250 and self.backward==0):
                    self.accelerationy=0.74*(self.speed)
                    self.y = self.y - self.accelerationy
                if  (self.x > 1275 and self.x < 1050 and self.backward==0):
                    self.accelerationy=0.048*(self.speed)
                    self.y = self.y + self.accelerationy
                if  (self.x > 1275 and self.x < 1473 and self.backward==0):
                    self.accelerationy=0.61*(self.speed)
                    self.y = self.y + self.accelerationy
                if  (self.x <= 1300 and self.backward==0):
                    self.flagx = 1
                if (self.flagx == 1 and self.backward==0):
                    if  (self.x >= 1376 and self.y < 281):
                        self.accelerationy=0.23*(self.speed)
                        self.y = self.y + self.accelerationy
                        self.flagx == 0
                if self.endprocess == 1:
                    if (self.x > 1373 and self.x < 1375 ):
                        self.f=1
                    if(self.f==1 and self.x < 1473):
                        self.accelerationx=1*(self.speed)
                        self.x = self.x + self.accelerationx
                        self.accelerationy=0.64*(self.speed)
                        self.y = self.y - self.accelerationy
                        self.backward=1 
                        self.flagx = 0
                        if self.x >= 1473:
                            if self.fl==0:
                                    self.flagmov=0    
            if ((self.x > 1373 and self.x < 1375) or (self.x > 1274 and self.x < 1276) or (self.x > 1049 and self.x < 1051) or (self.x > 849 and self.x < 851) or (self.x > 649 and self.x < 651) or (self.x > 449 and self.x < 451)  or (self.x > 249 and self.x < 251) or (self.x > 109 and self.x < 111) or (self.x > 14 and self.x < 16)):
                self.start_time = time.time()
                self.accelerationx=1*(self.speed)
                self.x -= self.accelerationx
        if  (self.x > 13 and self.x <15):
            self.flag1 = 1

        if (self.xflage == 'start' and self.flag1 == 1 and self.flagStop == 0):
            if  (self.x < 1473):
                self.end_time = time.time()
                if self.end_time - self.start_time >= 1:
                    self.accelerationx=1*(self.speed)
                    self.x = self.x + self.accelerationx
                    if ((self.Ex1 > 0 and self.Ex1 < 386 and self.flagE == 1) or (self.Ex1 < 710 and self.Ey1 > 325 and self.flagE == 1)):
                        if  (self.x >= 386):
                            if (self.y >= 280):
                                self.accelerationy=1.4*(self.speed)
                                self.y = self.y - self.accelerationy
                            self.accelerationx=0.5*(self.speed)
                            self.x = self.x - self.accelerationx
                            if (self.y < 280 and self.x > 450):
                                self.flagStop = 1

                    if (self.Ex1 > 386 and self.Ex1 < 790 and self.flagE == 1):
                        if  (self.x >= 790):
                            if (self.y >= 280):
                                self.accelerationy=1.4*(self.speed)
                                self.y = self.y - self.accelerationy
                            self.accelerationx=0.5*(self.speed)
                            self.x = self.x - self.accelerationx
                            if (self.y < 280 and self.x > 840):
                                self.flagStop = 1
                    if  (self.x > 14 and self.x < 111):
                        self.accelerationy=0.15*(self.speed)
                        self.y = self.y - self.accelerationy
                    if (self.y < 213):
                        self.accelerationy=0.08*(self.speed)
                        self.y = self.y + self.accelerationy
                    if (self.y > 211 and self.y < 310 and self.x > 110 and self.x < 250):
                        self.accelerationy=0.70*(self.speed)
                        self.y = self.y + self.accelerationy
                    if  (self.x > 250 and self.x < 450):
                        self.accelerationy=0.048*(self.speed)
                        self.y = self.y + self.accelerationy
                    if  (self.x > 1270 and self.x < 1470):
                        self.accelerationy=0.6*(self.speed)
                        self.y = self.y - self.accelerationy
                    if  (self.x >= 1473):
                        self.flag1 = 0
                        
                if ((self.x > 111 and self.x < 113) or (self.x > 250 and self.x < 252) or (self.x > 450 and self.x < 452) or (self.x > 650 and self.x < 652) or (self.x > 850 and self.x < 852) or (self.x > 1050 and self.x < 1052) or (self.x > 1269 and self.x < 1271)  or (self.x > 1369 and self.x < 1371) or (self.x > 1469 and self.x < 1471)):
                    self.start_time = time.time()
                    self.accelerationx=1*(self.speed)
                    self.x += self.accelerationx
                        
    def east_implement(self):# train EastBound
        self.east_move()
        return pygame.draw.circle(self.screen, (51,51,255), (self.x*self.newx, self.y*self.newy), 5, 0)