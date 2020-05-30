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
    turnFactor = 0.5
    margin = 100
    fov = 75
    minDistance = 20

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
        centeringFactor = 0.008
        numNeighbors = 0

        for boid in flock:
            if boid != self:
                if self.pos.distance(boid.pos) < self.fov: 
                    center += boid.pos
                    numNeighbors +=1
        if numNeighbors:
            center = center/numNeighbors
            v1 = center - self.pos
            return v1 * centeringFactor
        else:
            return coord(0, 0)

    #related to the distance to other boids
    def rule2(self, flock):
        v2 = coord(0, 0)
        avoidFactor = 0.05

        for boid in flock:
            if boid != self:
                if self.pos.distance(boid.pos) < self.minDistance:
                    v2 = v2 - (boid.pos - self.pos)
        return v2 * avoidFactor


    #related to average speed
    def rule3(self, flock):
        av = coord(0,0)
        matchingFactor = 0.05
        numNeighbors = 0

        for boid in flock:
            if boid != self:
                if self.pos.distance(boid.pos) < self.fov:
                    av += boid.vel
                    numNeighbors += 1
        if numNeighbors:
            av = av/numNeighbors
            v3 = av - self.vel
            return v3 * matchingFactor
        else:
            return coord(0, 0)

    def speed_limit(self):
        vlim = 10

        speed = self.vel.magnitude()
        if speed > vlim:
            self.vel = (self.vel/speed) * vlim


    def control_boundaries(self):
            if self.pos.x < self.margin: 
                self.vel.x += self.turnFactor
            elif self.pos.x > self.surface.width - self.margin:
                self.vel.x -= self.turnFactor
            if self.pos.y < self.margin:
                self.vel.y += self.turnFactor
            elif self.pos.y > self.surface.height - self.margin:
                self.vel.y -= self.turnFactor

    def move(self, flock):
        v1 = self.rule1(flock)
        v2 = self.rule2(flock)
        v3 = self.rule3(flock)
        self.vel += v1 + v2 + v3
        self.speed_limit()
        self.control_boundaries()
        
        self.pos += self.vel
              

class boids_list():
    def __init__(self, numBoids, screen):
        self.list =[]
        radius = 5

        for i in range(numBoids):

            r = random.randint(120, 200)
            b = random.randint(0, 255)
            g = random.randint(0, 24)

            xvel = random.randint(-2, 3)
            yvel = random.randint(-2, 3)
            xpos = random.randint(0, screen.width + 1)
            ypos = random.randint(0, screen.height + 1)
            vel = coord(xpos, ypos) 
            self.list.append(boids((r, g, b), xpos, ypos, radius, xvel, yvel, screen))

    def draw_boids(self):
        for boid in self.list:
            boid.draw_boid()

    def move_boids(self):
        for boid in self.list:
            boid.move(self.list)

def main():
    pygame.init()
    screen = game_screen(1700, 1000, "boid simulation")
    
    pygame.display.set_caption("boid simulation")

    clock = pygame.time.Clock()
    flock = boids_list(75, screen)
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