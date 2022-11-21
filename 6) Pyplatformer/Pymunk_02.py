import pymunk               # Import pymunk..
import pygame
import pymunk.pygame_util
import sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
pymunk.pygame_util.positive_y_is_up= True # pymunk 5.7에서 6.0 사이 변화로 추가
draw_options = pymunk.pygame_util.DrawOptions(screen)
    
space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0,-100     # Set its gravity

body = pymunk.Body(1, 20)  # Create a Body with mass and moment
body.position = 50,550      # Set the position of the body

shape = pymunk.Circle(body, 10, (120,2)) 
space.add(body, shape)

#


vs = [(-23,26), (23,26), (0,-26)]
moment = pymunk.moment_for_poly(1, vs)
body2 = pymunk.Body(1, moment)
body2.position = 100, 550
shape2 = pymunk.Poly(body2, vs)
shape2.friction  = 0.
shape2.elasticity = 0.5
space.add(body2, shape2)

body3 = pymunk.Body(body_type = pymunk.Body.STATIC)
body3.position = 300, 100
shape3 = pymunk.Poly(body3,
                     [(-300, 0), (300, 0), (300, -2), (-300, -2)])
shape3.friction  = 0.
shape3.elasticity = 0.5
space.add(body3, shape3)
body2.apply_impulse_at_local_point((60, 00), (0, 10))


#

clock = pygame.time.Clock()

for i in range(0,500):
    screen.fill((255,255,255))
    
    space.debug_draw(draw_options)
    space.step(1/50.0)        # Step the simulation one step forward
    pygame.display.flip()
    clock.tick(50)

pygame.quit()