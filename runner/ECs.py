import pygame
from pygame.locals import *

class ec:
      
    def __init__(self,screen, r,h,newx,newy,ex,ey,ex1,ey1,ex2,ey2,yl,ys):
        self.screen = screen
        self.r=r
        self.h=h
        self.newx=newx
        self.newy=newy
        self.ex=ex
        self.ey=ey
        self.ex1=ex1
        self.ey1=ey1
        self.ex2=ex2
        self.ey2=ey2
        self.yl=yl
        self.ys=ys
    def impEC(self):
        pygame.draw.polygon(self.screen, (self.r, self.h, 0), [[self.newx*self.ex, self.newy*self.ey], [self.newx*self.ex1, self.newy*self.ey1], [self.newx*self.ex2, self.newy*self.ey2]])
        pygame.draw.line(self.screen, (0, 0, 0), (self.newx*self.ys, self.newy*self.yl),(self.newx*self.ys, self.newy*self.yl+10), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (self.newx*self.ys, self.newy*self.yl+14),(self.newx*self.ys, self.newy*self.yl+16), 2)
        return pygame.draw.polygon(self.screen, (0, 0, 0), [[self.newx*self.ex, self.newy*self.ey], [self.newx*self.ex1, self.newy*self.ey1], [self.newx*self.ex2, self.newy*self.ey2]], 3)
        