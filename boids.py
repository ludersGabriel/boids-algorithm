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
    turnFactor = 1
    margin = 100
    fov = 100
    centeringFactor = 0.005
    avoidCollisionFactor = 0.05
    matchingSpeedFactor = 0.05
    avoidPredatorFactor = 0.05
    speedLimit = 10
    minDistance = 20
    safeDistance = 50
    m1 = 1

    def __init__(self, color, xpos, ypos, radius, xvel, yvel, isPredator, surface):
        self.color = color
        self.pos = coord(xpos, ypos)
        self.radius = radius
        self.vel = coord(xvel, yvel)
        self.surface = surface
        self.isPredator = isPredator

    def draw_boid(self):
        pygame.draw.circle(self.surface.screen, self.color, self.pos.t(), self.radius)

    #related to the center of mass of the flock
    def rule1(self, flock):
        center = coord(0, 0)
        numNeighbors = 0

        for boid in flock:
            if boid != self and (not boid.isPredator):
                if self.pos.distance(boid.pos) < self.fov: 
                    center += boid.pos
                    numNeighbors +=1
        if numNeighbors:
            center = center/numNeighbors
            v1 = center - self.pos
            return v1 * self.centeringFactor
        else:
            return coord(0, 0)

    #related to the distance to other boids
    def rule2(self, flock):
        v2 = coord(0, 0)

        for boid in flock:
            if boid != self:
                if self.pos.distance(boid.pos) < self.minDistance:
                    v2 = v2 - (boid.pos - self.pos)
        return v2 * self.avoidCollisionFactor

    #related to average speed
    def rule3(self, flock):
        av = coord(0,0)
        numNeighbors = 0

        for boid in flock:
            if boid != self and (not boid.isPredator):
                if self.pos.distance(boid.pos) < self.fov:
                    av += boid.vel
                    numNeighbors += 1
        if numNeighbors:
            av = av/numNeighbors
            v3 = av - self.vel
            return v3 * self.matchingSpeedFactor
        else:
            return coord(0, 0)

    #movin away from predator
    def rule4(self, flock):
        v4 = coord(0, 0)

        for boid in flock:
            if boid != self and boid.isPredator:
                if self.pos.distance(boid.pos) < self.safeDistance:
                    v4 = v4 - (boid.pos - self.pos)
        return v4 * self.avoidPredatorFactor

    def speed_limit(self):

        speed = self.vel.magnitude()
        if speed > self.speedLimit:
            self.vel = (self.vel/speed) * self.speedLimit

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.m1 = -(self.m1 * 300)

        v1 = self.rule1(flock) * self.m1
        v2 = self.rule2(flock)
        v3 = self.rule3(flock)
        v4 = self.rule4(flock)

        self.vel += v1 + v2 + v3 + v4
        self.speed_limit()
        self.control_boundaries()
        
        self.pos += self.vel
        self.m1 = 1
              
class predator(boids):
    fov = 120
    centeringFactor = 0.005
    avoidCollisionFactor = 0.05
    matchingSpeedFactor = 0.05
    avoidPredatorFactor = 0.1
    speedLimit = 20

    def rule4(self, flock):
        return coord(0, 0)

class boids_list():
    def __init__(self, numBoids, screen):
        self.list = []
        self.radius = 5
        self.screen = screen

        for i in range(numBoids):

            r = random.randint(120, 200)
            b = random.randint(0, 255)
            g = random.randint(0, 24)

            xvel = random.randint(-5, 5) + 1
            yvel = random.randint(-5, 5) + 1
            xpos = random.randint(0, screen.width + 1)
            ypos = random.randint(0, screen.height + 1)
            self.list.append(boids((r, g, b), xpos, ypos, self.radius, xvel, yvel, False, screen))
        
        xvel = random.randint(-5, 5) + 1
        yvel = random.randint(-5, 5) + 1
        xpos = random.randint(0, screen.width + 1)
        ypos = random.randint(0, screen.height + 1)
        self.list.append(predator((255,255,255), xpos, ypos, self.radius, xvel, yvel, True, screen))

    def add_predator(self):
        self.list.append(predator((255,255,255), self.screen.width/2, self.screen.height/2, self.radius, 0, 0, True, self.screen))

    def draw_boids(self):
        for boid in self.list:
            boid.draw_boid()

    def move_boids(self):
        for boid in self.list:
            boid.move(self.list)

def main():
    pygame.init()
    screen = game_screen(1700, 1000, "boid simulation")
    
    clock = pygame.time.Clock()
    flock = boids_list(50, screen)
    frameTime = 60
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.screen.fill((0,0,0))
        flock.draw_boids()
        flock.move_boids()        
        print(pygame.version.ver)
        pygame.display.update()
        clock.tick(frameTime)

if __name__ == "__main__":
    main()