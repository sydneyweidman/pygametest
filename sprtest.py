import random
import math
import pygame
import pygame.locals
from optparse import OptionParser
from pygame.sprite import Sprite

WIDTH = 1024
HEIGHT = 768
FPS = 60
STEP = 1
drag = 0.999
elasticity = 0.80
gravity = (-math.pi/2, 0.2)
bgcolor = pygame.Color('light grey')

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

class Particle(Sprite):

    radius = 20
    diameter = 2*radius
    refcount = 0
    
    def __init__(self, screen, color=None, pos=None, speed=0, direction=0):
        Sprite.__init__(self)
        self.color = self._randcolor()
        self.screen = screen
        self.image = pygame.Surface((self.diameter,self.diameter))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = direction
        if pos:
            self.x, self.y = [int(i) for i in pos]
        else:
            self.x, self.y = [random.randint(0,i) for i in screen.get_size()]

    def _get_x(self):
        return self.rect.centerx

    def _set_x(self, x):
        self.rect.centerx = x
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.rect.centery

    def _set_y(self, y):
        self.rect.centery = y
    y = property(_get_y, _set_y)
    
    def display(self):
        self.image.fill(bgcolor)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, 0)

    def _randcolor(self):
        return random.randint(0,255), random.randint(0,255), random.randint(0,255)
    
    def draw(self):
        self.display()

    def update(self):
        self.draw()

    def move(self):
        """Move distance per TICK in direction given in degrees"""
        (self.direction, self.speed) = addVectors((self.direction, self.speed), gravity)
        self.y -= math.sin(self.direction) * self.speed
        self.x += math.cos(self.direction) * self.speed
        self.y = int(self.y)
        self.x = int(self.x)
        self.speed *= drag
        
    def bounce(self):
        if self.x > WIDTH - self.radius:
            self.direction = math.pi - self.direction
            self.x = self.x - self.radius
            self.speed *= elasticity
        elif self.x < self.radius:
            self.direction = math.pi - self.direction
            self.x = self.radius
            self.speed *= elasticity
        if self.y > HEIGHT + self.radius:
            self.direction = - self.direction
            self.y = self.y - self.radius
            self.speed *= elasticity
        elif self.y < self.radius:
            self.direction = - self.direction
            self.y = self.radius
            self.speed *= elasticity

class App(object):

    WIDTH = WIDTH
    HEIGHT = HEIGHT
    FPS = FPS
    STEP = STEP
    parser = OptionParser(usage="%prog [OPTIONS]")
    parser.add_option('-r', '--random', help="Random motion", default=False, action='store_true')
    parser.add_option('-c', '--create', help="Create N sprites", default=4, metavar='N', type='int',
                      action='store')
    parser.add_option('-f', '--framerate', help="Set the frame rate", type='int', default=FPS)
    
    def on_execute(self):
        self.opts, self.args = self.parser.parse_args()
        self.FPS = self.opts.framerate
        selected_particle = None
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        background = pygame.Surface(screen.get_size())
        background.fill(bgcolor)
        font = pygame.font.Font(None,36)
        text = font.render('Bubbles', 1, (10,10,10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        screen.blit(background, (0,0))
        pygame.display.update()
        lastpos = None
        running = True
        loopcount = 0
        array = pygame.sprite.Group()

        for i in range(self.opts.create):
            array.add(Particle(screen))
        for idx, sp in enumerate(array):
            sp.speed = random.randint(1,50)
            sp.direction = random.uniform(0, math.pi*2)
            sp.id = idx
            print "Particle %d has speed %s and direction %s" % (sp.id, sp.speed, math.degrees(sp.direction),)
            
        while running:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_q):
                    running = False
                if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_a:
                    array.add(Particle(screen))
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    lastpos = pygame.mouse.get_pos()
                    for sp in array:
                        if sp.rect.collidepoint(lastpos):
                            selected_particle = sp
                elif event.type == pygame.MOUSEBUTTONUP:
                    selected_particle = None
            background.fill(bgcolor)
            screen.blit(background, (0,0))
            array.clear(screen,background)
            for sp in array:
                if not sp is selected_particle:
                    sp.move()
                    sp.bounce()
                    if self.opts.random and loopcount % 500:
                        sp.speed += random.randint(-self.STEP,self.STEP)
                        sp.direction += random.randint(-self.STEP,self.STEP)
            loopcount += 1
            pygame.display.set_caption('Running at %s FPS' % (self.FPS,))
            array.draw(screen)
            array.update()
            pygame.display.flip()
            clock.tick(self.FPS)
        pygame.quit()

if __name__ == '__main__':
    theApp = App()
    theApp.on_execute()

