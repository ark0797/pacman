import sys
import pygame
from pygame.locals import *
from math import floor
import random

map_size=16
tile_size=32

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
    def __init__(self, img, x, y, map_size, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.map_size=map_size
        self.tile_size=tile_size
        self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) *tile_size, floor(y) * tile_size, tile_size, tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    def __init__(self, x, y, map_size, tile_size):
        GameObject.__init__(self, './resources/car.png', x, y, map_size, tile_size)
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
    def __init__(self, x, y, map_size, tile_size):
        GameObject.__init__(self, './resources/android.png', x, y, map_size, tile_size)
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
    def __init__(self, x, y, map_size, tile_size):
        GameObject.__init__(self, './resources/wall.png', x, y, map_size, tile_size)
        self.direction=0
        self.velocity=0

    def game_tick(self):
        super(Wall, self).game_tick()

def create_walls(tile_size, map_size):
    Wall.w = [Wall(1, 1, map_size, tile_size),Wall(5, 5, map_size, tile_size), Wall(13, 1, map_size, tile_size), Wall(7, 4, map_size, tile_size),  Wall(10, 14, map_size, tile_size),  Wall(4, 15, map_size, tile_size),  Wall(2 ,13, map_size, tile_size),  Wall(15, 12, map_size, tile_size),  Wall(9, 8, map_size, tile_size)]

def is_wall(x, y):
    for w in Wall.w:
        if (int(w.x), int(w.y)) == (int(x), int(y)):
            return True
    return False

def draw_walls(screen):
    for w in Wall.w:
        GameObject.draw(w, screen)


class Food(GameObject):
    num=0
    def __init__(self, x, y, map_size, tile_size):
        GameObject.__init__(self,'./resources/Apple Blue.png', x, y, map_size, tile_size)

def is_food(x, y):
    for w in Wall.w:
        if (int(w.x), int(w.y)) == (int(x), int(y)):
            return True
    return False


class Map:
     def __init__(self, filename):
         self.map = []
         f=open('./resources/map.txt', 'r')
         txt=f.readlines()
         f.close()
         for y in range(map_size):
             self.map.append([])
             for x in range(map_size):
                 if '#' in txt[y][x]:
                     self.map[-1].append(Wall(x,y, map_size, tile_size))
                 elif 'f' in txt[y][x]:
                     self.map[-1].append(Food(x,y, map_size, tile_size))
                     Food.num+=1

     def get(self, x, y):
         return self.map[x][y]

     def draw(self, screen):
         for y in range(len(self.map)):
             for x in range(len(self.map[y])):
                 self.map[y][x].draw(screen)



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

    global MAP
    MAP = Map('map.txt')
    ghost = Ghost(0, 0, map_size, tile_size)
    ghost1= Ghost(1, 1, map_size, tile_size)
    ghost2 = Ghost(3,3, map_size, tile_size)
    pacman = Pacman(2, 1, map_size, tile_size)

    create_walls(tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()
    

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        ghost.game_tick()
        ghost1.game_tick()
        ghost2.game_tick()
        pacman.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        ghost.draw(screen)
        ghost1.draw(screen)
        ghost2.draw(screen)
        MAP.draw(screen)
        draw_walls(screen)
        pygame.display.update()
