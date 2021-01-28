import pygame
import os
from pygame.constants import (QUIT, K_ESCAPE, KEYDOWN, KEYUP, K_SPACE, K_RETURN)
import random

import RPi.GPIO as GPIO
import time

taster= 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(taster, GPIO.IN)

ledblau = 15
ledgruen = 27
ledgelb = 23
ledrot = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledblau,GPIO.OUT)
GPIO.setup(ledgruen,GPIO.OUT)
GPIO.setup(ledgelb,GPIO.OUT)
GPIO.setup(ledrot,GPIO.OUT)

class Settings(object):                                         # Basic Fenster Eistellungen
    def __init__(self):
        self.width = 700
        self.height = 700
        self.fps = 60       
        self.title = "Mensch Ärgere Dich Nicht!" 
        self.images_path = os.path.dirname(os.path.abspath(__file__))

    def get_dim(self):
        return (self.width, self.height)


class PlayerGelb(pygame.sprite.Sprite):                         # Gelber Spieler
    def __init__(self,settings,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "PlayerGelb.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.direction = 0
        self.speed = 5
        self.draging = False

class PlayerBlau(pygame.sprite.Sprite):                         # Blauer Spieler
    def __init__(self,settings,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "PlayerBlau.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.direction = 0
        self.speed = 5
        self.draging = False

class PlayerGruen(pygame.sprite.Sprite):                        # Grüner Spieler
    def __init__(self,settings,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "PlayerGruen.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.direction = 0
        self.speed = 5
        self.draging = False

class PlayerRot(pygame.sprite.Sprite):                          # Roter Spieler
    def __init__(self,settings,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "PlayerRot.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.direction = 0
        self.speed = 5
        self.draging = False

class Würfel(object):                                           # Würfel auf dem Brett, mit neuer zahl und farbwechselndem Hintergrund beim würfeln
    def __init__(self,settings):
        self.settings= settings
        self.color= [0,0,0]
        self.zahl= 0
        self.font = pygame.font.Font(None, 70)
        self.text = self.font.render(str(self.zahl), True, self.color)
        self.textRect = self.text.get_rect()
        self.textRect.center = 330, 330
        self.counter= 0
        self.backcolor = [255,255,255]

    def new_zahl(self):
        self.zahl= random.randint(1,6)
        self.text = self.font.render(str(self.zahl), True, self.color)
        self.counter += 1
        if self.counter == 1 :
            self.backcolor = [135,186,19]
            if self.backcolor == [135,186,19]:
                GPIO.output(ledgruen, True)
                GPIO.output(ledblau, False)
                GPIO.output(ledrot, False)
                GPIO.output(ledgelb, False)
        if self.counter == 2 :
            self.backcolor = [32,154,211]
            if self.backcolor == [32,154,211]:
                GPIO.output(ledgruen, False)
                GPIO.output(ledblau, True)
                GPIO.output(ledrot, False)
                GPIO.output(ledgelb, False)
        if self.counter == 3 :
            self.backcolor = [226,8,74]
            if self.backcolor == [226,8,74]:
                GPIO.output(ledgruen, False)
                GPIO.output(ledblau, False)
                GPIO.output(ledrot, True)
                GPIO.output(ledgelb, False)
        if self.counter == 4 :
            self.backcolor = [254,204,0]
            if self.backcolor == [254,204,0]:
                GPIO.output(ledgruen, False)
                GPIO.output(ledblau, False)
                GPIO.output(ledrot, False)
                GPIO.output(ledgelb, True)
        if self.counter == 5 :
            self.counter = 1
            self.backcolor = [135,186,19]
            if self.backcolor == [135,186,19]:
                GPIO.output(ledgruen, True)
                GPIO.output(ledblau, False)
                GPIO.output(ledrot, False)
                GPIO.output(ledgelb, False)


class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "brettspiel.png"))
        self.background = pygame.transform.scale(self.background, (700, 700))
        self.background_rect = self.background.get_rect()
        self.playerRot1= PlayerRot(settings,558,565)        #spiderman
        self.playerRot2= PlayerRot(settings,617,565)
        self.playerRot3= PlayerRot(settings,558,625)
        self.playerRot4= PlayerRot(settings,617,625)
        self.playerGelb1= PlayerGelb(settings,27,570)      #spongebob
        self.playerGelb2= PlayerGelb(settings,86,570)
        self.playerGelb3= PlayerGelb(settings,27,630)
        self.playerGelb4= PlayerGelb(settings,86,630)
        self.playerGruen1= PlayerGruen(settings,25,30)      #shrek
        self.playerGruen2= PlayerGruen(settings,85,30)
        self.playerGruen3= PlayerGruen(settings,25,90)
        self.playerGruen4= PlayerGruen(settings,85,90)
        self.playerBlau1= PlayerBlau(settings,543,25)      #stitch
        self.playerBlau2= PlayerBlau(settings,603,25)
        self.playerBlau3= PlayerBlau(settings,543,85)
        self.playerBlau4= PlayerBlau(settings,603,85)
        self.dice= Würfel(settings)
        self.clock = pygame.time.Clock()
        self.done = False

        self.playersred = pygame.sprite.Group()
        self.playersred.add(self.playerRot1)
        self.playersred.add(self.playerRot2)
        self.playersred.add(self.playerRot3)
        self.playersred.add(self.playerRot4)

        self.playersyellow = pygame.sprite.Group()
        self.playersyellow.add(self.playerGelb1)
        self.playersyellow.add(self.playerGelb2)
        self.playersyellow.add(self.playerGelb3)
        self.playersyellow.add(self.playerGelb4)

        self.playersgreen = pygame.sprite.Group()
        self.playersgreen.add(self.playerGruen1)
        self.playersgreen.add(self.playerGruen2)
        self.playersgreen.add(self.playerGruen3)
        self.playersgreen.add(self.playerGruen4)

        self.playersblue = pygame.sprite.Group()
        self.playersblue.add(self.playerBlau1)
        self.playersblue.add(self.playerBlau2)
        self.playersblue.add(self.playerBlau3)
        self.playersblue.add(self.playerBlau4)


    def run(self):
        while not self.done:                            
            self.clock.tick(self.settings.fps)
            if GPIO.input(taster) == True:                   # Würfel Aktion
                self.dice.new_zahl()
                time.sleep(0.5)
            for event in self.pygame.event.get():     
                if event.type == QUIT: 
                    self.done = True                    
                if event.type == KEYDOWN:             
                    if event.key == K_ESCAPE:
                        self.done = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN:                      # Anklicken des Sprites
                    if event.button == 1:            
                        
                        if self.playerGruen1.rect.collidepoint(event.pos):      # Für Shrek
                            self.playerGruen1.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGruen1.rect.left - mouse_x
                            offset_y = self.playerGruen1.rect.top - mouse_y
                        if self.playerGruen2.rect.collidepoint(event.pos):
                            self.playerGruen2.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGruen2.rect.left - mouse_x
                            offset_y = self.playerGruen2.rect.top - mouse_y
                        if self.playerGruen3.rect.collidepoint(event.pos):
                            self.playerGruen3.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGruen3.rect.left - mouse_x
                            offset_y = self.playerGruen3.rect.top - mouse_y
                        if self.playerGruen4.rect.collidepoint(event.pos):
                            self.playerGruen4.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGruen4.rect.left - mouse_x
                            offset_y = self.playerGruen4.rect.top - mouse_y

                        if self.playerBlau1.rect.collidepoint(event.pos):           # Für Stitch
                            self.playerBlau1.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerBlau1.rect.left - mouse_x
                            offset_y = self.playerBlau1.rect.top - mouse_y
                        if self.playerBlau2.rect.collidepoint(event.pos):
                            self.playerBlau2.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerBlau2.rect.left - mouse_x
                            offset_y = self.playerBlau2.rect.top - mouse_y
                        if self.playerBlau3.rect.collidepoint(event.pos):
                            self.playerBlau3.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerBlau3.rect.left - mouse_x
                            offset_y = self.playerBlau3.rect.top - mouse_y
                        if self.playerBlau4.rect.collidepoint(event.pos):
                            self.playerBlau4.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerBlau4.rect.left - mouse_x
                            offset_y = self.playerBlau4.rect.top - mouse_y

                        if self.playerRot1.rect.collidepoint(event.pos):            # Für Spidey
                            self.playerRot1.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerRot1.rect.left - mouse_x
                            offset_y = self.playerRot1.rect.top - mouse_y
                        if self.playerRot2.rect.collidepoint(event.pos):
                            self.playerRot2.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerRot2.rect.left - mouse_x
                            offset_y = self.playerRot2.rect.top - mouse_y
                        if self.playerRot3.rect.collidepoint(event.pos):
                            self.playerRot3.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerRot3.rect.left - mouse_x
                            offset_y = self.playerRot3.rect.top - mouse_y
                        if self.playerRot4.rect.collidepoint(event.pos):
                            self.playerRot4.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerRot4.rect.left - mouse_x
                            offset_y = self.playerRot4.rect.top - mouse_y

                        if self.playerGelb1.rect.collidepoint(event.pos):           # Für Spongey
                            self.playerGelb1.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGelb1.rect.left - mouse_x
                            offset_y = self.playerGelb1.rect.top - mouse_y
                        if self.playerGelb2.rect.collidepoint(event.pos):
                            self.playerGelb2.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGelb2.rect.left - mouse_x
                            offset_y = self.playerGelb2.rect.top - mouse_y
                        if self.playerGelb3.rect.collidepoint(event.pos):
                            self.playerGelb3.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGelb3.rect.left - mouse_x
                            offset_y = self.playerGelb3.rect.top - mouse_y
                        if self.playerGelb4.rect.collidepoint(event.pos):
                            self.playerGelb4.draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.playerGelb4.rect.left - mouse_x
                            offset_y = self.playerGelb4.rect.top - mouse_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:            
                        
                        self.playerGruen1.draging = False           # Shrek drop
                        self.playerGruen2.draging = False
                        self.playerGruen3.draging = False
                        self.playerGruen4.draging = False

                        self.playerBlau1.draging = False            # Stitch drop
                        self.playerBlau2.draging = False
                        self.playerBlau3.draging = False
                        self.playerBlau4.draging = False

                        self.playerRot1.draging = False             # Spidey drop
                        self.playerRot2.draging = False
                        self.playerRot3.draging = False
                        self.playerRot4.draging = False

                        self.playerGelb1.draging = False            # Spongey drop
                        self.playerGelb2.draging = False
                        self.playerGelb3.draging = False
                        self.playerGelb4.draging = False

                elif event.type == pygame.MOUSEMOTION:              # Drag vom Sprite

                    if self.playerGruen1.draging:                           # Shrek drag
                        mouse_x, mouse_y = event.pos
                        self.playerGruen1.rect.left = mouse_x + offset_x
                        self.playerGruen1.rect.top = mouse_y + offset_y
                    if self.playerGruen2.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGruen2.rect.left = mouse_x + offset_x
                        self.playerGruen2.rect.top = mouse_y + offset_y
                    if self.playerGruen3.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGruen3.rect.left = mouse_x + offset_x
                        self.playerGruen3.rect.top = mouse_y + offset_y
                    if self.playerGruen4.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGruen4.rect.left = mouse_x + offset_x
                        self.playerGruen4.rect.top = mouse_y + offset_y

                    if self.playerBlau1.draging:                            # Stitch drag
                        mouse_x, mouse_y = event.pos
                        self.playerBlau1.rect.left = mouse_x + offset_x
                        self.playerBlau1.rect.top = mouse_y + offset_y
                    if self.playerBlau2.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerBlau2.rect.left = mouse_x + offset_x
                        self.playerBlau2.rect.top = mouse_y + offset_y
                    if self.playerBlau3.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerBlau3.rect.left = mouse_x + offset_x
                        self.playerBlau3.rect.top = mouse_y + offset_y
                    if self.playerBlau4.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerBlau4.rect.left = mouse_x + offset_x
                        self.playerBlau4.rect.top = mouse_y + offset_y

                    if self.playerRot1.draging:                             # Spidey drag
                        mouse_x, mouse_y = event.pos
                        self.playerRot1.rect.left = mouse_x + offset_x
                        self.playerRot1.rect.top = mouse_y + offset_y
                    if self.playerRot2.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerRot2.rect.left = mouse_x + offset_x
                        self.playerRot2.rect.top = mouse_y + offset_y
                    if self.playerRot3.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerRot3.rect.left = mouse_x + offset_x
                        self.playerRot3.rect.top = mouse_y + offset_y
                    if self.playerRot4.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerRot4.rect.left = mouse_x + offset_x
                        self.playerRot4.rect.top = mouse_y + offset_y

                    if self.playerGelb1.draging:                            # Spongey drag
                        mouse_x, mouse_y = event.pos
                        self.playerGelb1.rect.left = mouse_x + offset_x
                        self.playerGelb1.rect.top = mouse_y + offset_y
                    if self.playerGelb2.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGelb2.rect.left = mouse_x + offset_x
                        self.playerGelb2.rect.top = mouse_y + offset_y
                    if self.playerGelb3.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGelb3.rect.left = mouse_x + offset_x
                        self.playerGelb3.rect.top = mouse_y + offset_y
                    if self.playerGelb4.draging:
                        mouse_x, mouse_y = event.pos
                        self.playerGelb4.rect.left = mouse_x + offset_x
                        self.playerGelb4.rect.top = mouse_y + offset_y

            self.draw()
            self.update()

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        pygame.draw.circle(self.screen, self.dice.backcolor, (345,352), 30)     # Hintergrund vom Würfel
        self.screen.blit(self.dice.text, self.dice.textRect.center)            # Würfel
        self.playersred.draw(self.screen)
        self.playersyellow.draw(self.screen)
        self.playersgreen.draw(self.screen)
        self.playersblue.draw(self.screen)
        self.pygame.display.flip()


    def update(self):
        pass
        

if __name__ == '__main__':      

    pygame.init()    

    settings = Settings()

    game = Game(pygame, settings)

    game.run()
    
    pygame.quit()             
