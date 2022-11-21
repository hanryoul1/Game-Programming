# import pymunk
# import pygame
# import pymunk.pygame_util
# import sys

# pygame.init()
# screen = pygame.display.set_mode((600, 600))
# pymunk.pygame_util.positive_y_is_up = True
# draw_options = pymunk.pygame_util.DrawOptions(screen)

# space = pymunk.Space()
# space.gravity = 0, -100

# body = pymunk.Body(1, 20)
# body.position = 50, 550

# shape = pymunk.Circle(body, 10, (0, 0))
# space.add(body, shape)

# clock = pygame.time.Clock()

# for i in range(0, 500):
#     screen.fill((255, 255, 255))
#     space.debug_draw(draw_options)
#     space.step(1/50.0)
#     pygame.display.flip()
#     clock.tick(50)

# vs = [(-23,26), (23,26), (0,-26)]

# moment = pymunk.moment_for_poly(1, vs)
# body2 = pymunk.Body(1, moment)
# body2.position = 100, 550

# shape2 = pymunk.Poly(body2, vs)
# shape2.friction = 0.
# shape2.elasticity = 0.5
# space.add(body2, shape2)

# body3 = pymunk.Body(body_type = pymunk.Body.STATIC)
# body3.position = 300, 100

# shape3 = pymunk.Poly(body3, 
# [(-300, 0), (300, 0), (300, -2), (-300, -2)])
# shape3.friction = 0.
# shape3.elasticity = 0.5
# space.add(body3, shape3)

# body2.apply_impulse_at_local_point((60, 00), (0, 10))

# pygame.quit()