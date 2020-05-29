import pygame
import random

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
        self.xpos = xpos
        self.ypos = ypos
        self.pos = xpos, ypos
        self.radius = radius
        self.xvel = xvel
        self.yvel = yvel
        self.surface = surface

    def draw_boid(self):
        pygame.draw.circle(self.surface.screen, self.color, self.pos, self.radius)

    def move(self):
        keys = pygame.key.get_pressed()
        
        self.xpos += self.xvel
        self.ypos += self.yvel
        self.pos = self.xpos, self.ypos
        if self.xpos < 0 or self.xpos  > self.surface.width: 
            self.xvel = -self.xvel
        if self.ypos < 0 or self.ypos > self.surface.height:
            self.yvel = -self.yvel
    
class boids_list():
    def __init__(self, numBoids, screen):
        self.list =[]
        xvel = 5
        yvel = 5
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
            boid.move()

def main():
    pygame.init()
    screen = game_screen(1600, 900, "boid simulation")
    
    pygame.display.set_caption("boid simulation")

    flock = boids_list(10, screen)
    frameTime = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.screen.fill((0,0,0))
        flock.draw_boids()
        flock.move_boids()
        pygame.display.update()
        pygame.time.delay(frameTime)

if __name__ == "__main__":
    main()