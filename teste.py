import pygame
import random

def main():
    pygame.init()

    #screen initialization
    #size is a tuple
    width, height = 1600, 900
    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("boid simulation")
    black = 0, 0, 0



    #character characteristics
    #position
    x = width//2
    y = height//2
    #size
    charWidth = 40
    charHeight = 60
    charRadius = 5
    #velocity
    vel = 5
    
    #main loop
    run = True
    frameTime = 10

    while run:
        #checking for every person-game interation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        #moving, keys is a dict
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x - vel - charRadius > 0:
            x -= vel
        if keys[pygame.K_RIGHT] and x + vel + charRadius < width:
            x += vel
        if keys[pygame.K_DOWN] and y + vel + charRadius < height:
            y += vel
        if keys[pygame.K_UP] and y - vel - charRadius > 0:
          y -= vel
        



        #drawing character screen, color, tuple 
        screen.fill(black)
        objrect = pygame.draw.circle(screen, (200, 23, 255), (x, y), charRadius)
        if keys[pygame.K_q]:
            pygame.transfom.rotate(objrect.rect, 10)
        #clock in ms and screen refresh
        pygame.display.update()
        pygame.time.delay(frameTime)

    #ball = pygame.image.load("birbplane.png")
    #ballrect = ball.get_rect()
    #
    
    #speed = [2, 2]
    #frames = 0
    #while 1:
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT: 
    #            pygame.quit()
    #            quit()
    #
    #    ballrect = ballrect.move(speed)
    #    if ballrect.left < 0 or ballrect.right > width:
    #        speed[0] = -speed[0]
    #    if ballrect.top < 0 or ballrect.bottom > height:
    #        speed[1] = -speed[1]
    #            
    #    screen.fill(black)
    #    screen.blit(ball, ballrect)
    #    pygame.display.flip()
    #    frames += 1
if __name__ == "__main__":
    main()