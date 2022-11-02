import pygame
import time
import random

# Create the screen
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

dis_w = 800
dis_h = 600

dis = pygame.display.set_mode((dis_w, dis_h))
pygame.display.set_caption('Snake Game by HanRyoul')

clock = pygame.time.Clock()

# Snake size&speed
snake_block = 10
snake_speed = 20

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 40)

# Displaying the Score
def snake_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def snake_length(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

def message(word,color):
    msg = font_style.render(word, True, color)
    dis.blit(msg, [dis_w/4, dis_h/2.3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_w/2
    y1 = dis_h/2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Adding the Food
    food_x = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0

    while not game_over:

        # Game Over message
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press 'Q' to Quit", white)
            snake_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
        
        # Moving the Snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Game Over when Snake hits the boundaries
        if x1 >= dis_w or x1 < 0 or y1 >= dis_h or y1 < 0:
            game_close = True

        x1 += x1_change   
        y1 += y1_change  
        dis.fill(black)
        pygame.draw.rect(dis,red,[food_x, food_y, snake_block, snake_block])

        # Increasing the Length of the Snake
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        
        snake_length(snake_block, snake_list)
        snake_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_h - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()