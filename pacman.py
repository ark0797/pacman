import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((0, 0, 0))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.map=map
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()

        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x+self.velocity), self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)

class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0


    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
           if not is_wall(floor(self.x + self.velocity), self.y):
               self.x += self.velocity
           if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction=0
        self.velocity=0

    def game_tick(self):
        super(Wall, self).game_tick()

def create_walls(tile_size, map_size):
    Wall.w = [Wall(1, 1, tile_size, map_size),Wall(5, 5, tile_size, map_size), Wall(13, 1, tile_size, map_size), Wall(7, 4, tile_size, map_size),  Wall(10, 14, tile_size, map_size),  Wall(4, 15, tile_size, map_size),  Wall(2 ,13, tile_size, map_size),  Wall(15, 12, tile_size, map_size),  Wall(9, 8, tile_size, map_size)]

def is_wall(x, y):
    for w in Wall.w:
        if (int(w.x), int(w.y)) == (int(x), int(y)):
            return True
    return False

def draw_walls(screen):
    for w in Wall.w:
        GameObject.draw(w, screen)


class Map:
     def __init__(self, w, h):
         self.map = [ [list()]*x for i in range(y) ]
         '''txt=open('./resources/map.txt', 'r')
         for x in range (h):
                 a=txt.readline()
                 a=a.rstrip()
                 self.map[x]=list(a.split('.'))'''

     txt=open('./resources/map.txt', 'r')
     A=txt.readlines()
     h=len(A)
     w=len(A[0])

     def get(self, x, y):
         return self.map[x][y]



def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    ghost = Ghost(0, 0, tile_size, map_size)
    ghost1= Ghost(1, 1, tile_size, map_size)
    pacman = Pacman(2, 1, tile_size, map_size)
    '''wall = []
    wall.append(Wall(1, 1, tile_size, map_size))
    wall.append(Wall(5, 5, tile_size, map_size))
    wall.append(Wall(9, 9, tile_size, map_size))
    wall.append(Wall(2, 7, tile_size, map_size))
    wall.append(Wall(8, 6, tile_size, map_size))
    wall.append(Wall(13, 1, tile_size, map_size))
    wall.append(Wall(10, 4, tile_size, map_size))'''
    create_walls(tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()
    

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        ghost1.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        ghost.draw(screen)
        ghost1.draw(screen)
        '''for w in wall:
            w.draw(screen)'''
        draw_walls(screen)
        pygame.display.update()
