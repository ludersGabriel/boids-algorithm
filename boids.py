import pygame
import random
import math

class coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, c):
        return coord(self.x + c.x, self.y + c.y)
    
    def __sub__(self, c):
        return coord(self.x - c.x, self.y - c.y)

    def __floordiv__(self, num):
        return coord(self.x//num, self.y//num)

    def __truediv__(self, num):
        return coord(self.x/num, self.y/num)

    def __eq__(self, c):
        return self.x == c.x and self.y == c.y

    def __mul__(self, num):
        return coord(self.x*num, self.y*num)

    def t(self):
        return (int(self.x), int(self.y))

    def distance(self, c):
        return math.sqrt((self.x - c.x)**2 + (self.y - c.y)**2)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

class game_screen():
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(name)

class boids():
    def __init__(self, color, xpos, ypos, radius, xvel, yvel, surface):
        self.color = color
        self.pos = coord(xpos, ypos)
        self.radius = radius
        self.vel = coord(xvel, yvel)
        self.surface = surface

    def draw_boid(self):
        pygame.draw.circle(self.surface.screen, self.color, self.pos.t(), self.radius)

    #related to the center of mass of the flock
    def rule1(self, flock):
        center = coord(0, 0)
        for boid in flock:
            if boid != self: 
                center += boid.pos
        center = center/(len(flock) - 1)
        v1 = (center - self.pos)/50
        return v1

    #related to the distance to other boids
    def rule2(self, flock):
        v2 = coord(0, 0)
        for boid in flock:
            if boid != self:
                if (boid.pos - self.pos).magnitude() < 10:
                    v2 = v2 - (boid.pos - self.pos)
        return v2


    #related to average speed
    def rule3(self, flock):
        av = coord(0,0)
        for boid in flock:
            if boid != self:
                av += boid.vel
        av = av/(len(flock) - 1)
        v3 = (av - self.vel)/20
        return v3

    def speed_limit(self):
        vlim = 10

        speed = self.vel.magnitude()
        if speed > vlim:
            self.vel = (self.vel/speed) * vlim

    def move(self, flock):
        v1 = self.rule1(flock)
        v2 = self.rule2(flock)
        v3 = self.rule3(flock)
        self.vel += v1

        self.speed_limit()
        self.pos += self.vel
        
        if self.pos.x < 0: 
            self.vel.x = 10
        elif self.pos.x > self.surface.width:
            self.vel.x = -10
        if self.pos.y < 0:
            self.vel.y = 10
        elif self.pos.y > self.surface.height:
            self.vel.y = -10         

class boids_list():
    def __init__(self, numBoids, screen):
        self.list =[]
        xvel = random.randint(0, 6)
        yvel = random.randint(0, 6)
        radius = 5

        for i in range(numBoids):
            xpos = random.randint(0, screen.width + 1)
            ypos = random.randint(0, screen.height + 1)
            self.list.append(boids((200, 23, 255), xpos, ypos, radius, xvel, yvel, screen))

    def draw_boids(self):
        for boid in self.list:
            boid.draw_boid()

    def move_boids(self):
        for boid in self.list:
            boid.move(self.list)

def main():
    pygame.init()
    screen = game_screen(1600, 900, "boid simulation")
    
    pygame.display.set_caption("boid simulation")

    clock = pygame.time.Clock()
    flock = boids_list(100, screen)
    frameTime = 60
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.screen.fill((0,0,0))
        flock.draw_boids()
        flock.move_boids()
        pygame.display.update()
        clock.tick(frameTime)

if __name__ == "__main__":
    main()