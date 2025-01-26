import pygame
import os
import time
import random
pygame.font.init()

width, height = 600,500
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Invaders Game")

redENEMY = pygame.image.load(os.path.join("assets","red.png"))
greenENEMY = pygame.image.load(os.path.join("assets","green.png"))
yellowENEMY = pygame.image.load(os.path.join("assets","yellow.png"))
playerSHIP1 = pygame.image.load(os.path.join("assets","Space-Invadrs-ship.png"))
playerSHIP2 = pygame.image.load(os.path.join("assets","Space-Invaders-ship2.png"))
redLASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
greenLASER= pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
yellowLASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
blueLASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","download.jpg")),(width,height))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img) 
        pass
    def draw(self, window):
        window.blit(self.img,(self.x,self.y))  
    def move(self, vel):
        self.y += vel
    def offscreen(self,height): 
        return not(self.y <= height  and self.y >= 0) 
    def collision(self, obj):
        return collide(self,obj)
class Ship:
        CoolDown = 30
        def __init__(self, x, y, health=100): 
            self.x = x
            self.y = y
            self.health = health 
            self.shipimg = None
            self.laserimg =None
            self.lasers = []
            self.cooldowncounter = 0
            pass
        def draw(self, window):
            window.blit(self.shipimg,(self.x,self.y))
            for laser in self.lasers:
                laser.draw(window)
        def movelasers(self, vel, obj):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.offscreen(height):
                    self.lasers.remove(laser)
                elif laser.collision(obj):
                    obj.health -= 10
                    self.lasers.remove(laser)


        def cooldown(self):
            if self.cooldowncounter >= self.CoolDown:
                self.cooldowncounter = 0
            elif self.cooldowncounter > 0:
                self.cooldowncounter += 1
        def shoot(self, o=0):
            if self.cooldowncounter == 0:
               laser = Laser(self.x-o,self.y,self.laserimg)
               self.lasers.append(laser)
               self.cooldowncounter = 1
        def get_width(self):
            return self.shipimg.get_width()
        def get_height(self):
            return self.shipimg.get_height()   
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.shipimg = playerSHIP1
        self.laserimg = blueLASER
        self.mask = pygame.mask.from_surface(self.shipimg)
        self.mxhealth = health
    def movelasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.offscreen(height):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collision(obj):
                           objs.remove(obj)
                           if laser in self.lasers:
                              self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    def healthbar(self, window):
        pygame.draw.rect(window,(255,50,0),(self.x,self.y + self.shipimg.get_height()+10, self.shipimg.get_width(),10))
        pygame.draw.rect(window,(50,255,0),(self.x,self.y + self.shipimg.get_height()+10, self.shipimg.get_width()* (self.health/self.mxhealth), 10))
 
class Enemy (Ship):
    colormap = {
         "red" : (redENEMY,redLASER),
         "green" : (greenENEMY,greenLASER),
         "yellow" : (yellowENEMY,yellowLASER)
    }
    def __init__(self, x, y, color,  health=100): 
        super().__init__(x, y, health)
        self.shipimg,self.laserimg  = self.colormap[color]
      #  self.laserimg =blueLASER
        self.mask = pygame.mask.from_surface(self.shipimg)
      #  self.mxhealth = health
    def move(self, vel):
        self.y += vel  

def collide(obj1,obj2):
    offsetx = obj2.x -obj1.x
    offsety = obj2.y -obj1.y
    return obj1.mask.overlap(obj2.mask,(offsetx,offsety)) != None

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    enemies = []
    wavelength = 5
    enemyvel = 1
    playersp = 5
    lasersp = 5
    b = 125
    mainfont = pygame.font.SysFont("comicsans", 30)
    lostfont = pygame.font.SysFont("comicsans", 60)
    player = Player(260,370)
    clock = pygame.time.Clock()
    lost = False
    lostcount = 0
    bb =0

    def redrawwindow():
        win.blit(bg,(0,0))
        liveslabel = mainfont.render(f"Lives: {lives}", 1,(255,255,255))
        levellabel = mainfont.render(f"Level: {level}", 1,(255,255,255))
        win.blit(liveslabel,(10,8))
        win.blit(levellabel,(width - levellabel.get_width()- 10,8))
        for enemy in enemies:
            enemy.draw(win)
        player.draw(win)
        if lost:
            lostlabel = lostfont.render("You Lost!!", 1,(255,255,255))
            win.blit(lostlabel, (width/2-lostlabel.get_width()/2,190))
        pygame.display.update()
        

    while run:
        clock.tick(FPS)
        redrawwindow()      
        if lives <= 0 or player.health <=0:
          lost = True  
          lostcount += 1 
        if lost:
            if lostcount >  FPS * 3:
                run = False
        if len(enemies) == 0:
            level += 1
            wavelength += 5
            for i in range(wavelength):
                enemy = Enemy(random.randrange(50,width-100),random.randrange(-1500,-100), random.choice(["red", "green", "yellow"]))
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                run == True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - playersp > 15:
            player.x -= playersp  
        if keys[pygame.K_RIGHT] and player.x + playersp + b  < width:
            player.x += playersp
        if keys[pygame.K_UP] and player.y - playersp > 15:
            player.y -= playersp   
        if keys[pygame.K_DOWN] and player.y + playersp + b < height:
            player.y += playersp  
        if keys[pygame.K_SPACE ]:
            player.shoot()
        if keys[pygame.K_x ]:
            bb += 3
            if bb%2 == 1:
                player.shipimg = playerSHIP2
            else :
                player.shipimg = playerSHIP1  
        for enemy in enemies[:]:
            enemy.move(enemyvel)
            enemy.movelasers(lasersp,player)
            if random.randrange(0,2*60) == 1 :
                enemy.shoot(30)
            if enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)
            if collide(enemy,player):
                player.health -= 10
                enemies.remove(enemy)
        player.movelasers(-lasersp, enemies)
def mainmenu():
    titlefont = pygame.font.SysFont("comicsans", 30)
   
    run = True
    while run:
        win.blit(bg,(0,0))
        titlelabel = titlefont.render(f"Press on the Mouse to begin",1,(255,255,255))
        win.blit(titlelabel,(width/2 - titlelabel.get_width()/2, 220))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False   
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()    
    pygame.quit()           


mainmenu()