from pygame.constants import K_RIGHT
from stage1 import *
from stage2 import *
from stage3 import *

# 오프닝 
def start_menu():
    pygame.init()
    pygame.mixer.music.load('sound/game_start.mp3')  
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(.9)

    text_background_color = (255, 255, 255)
    title_font = pygame.font.SysFont('bahnschrift', 44)
    menu_font = pygame.font.SysFont('bahnschrift', 28)
    
    while True:
        screen.blit(background, (0, 0))  
        title_label = title_font.render('Welcome to', True, (0, 0, 0))
        title2_label = title_font.render('\'Pang Pang\'', True, (0, 0, 0))
        start_label = menu_font.render('Enter to \'Start\'', True, (0, 0, 0), text_background_color)  
        way_label = menu_font.render('Shift to \'How to Play\'', True, (0, 0, 0), text_background_color)
        
        screen.blit(title_label, (220, 260))
        screen.blit(title2_label, (220, 310))
        screen.blit(start_label, (10, 390))
        screen.blit(way_label,(10,430))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_loop()
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    game_rule()

# 게임 방법
def game_rule():
    # pygame.mixer.music.load('sound/game_start.mp3')  
    # pygame.mixer.music.play(-1) 
    # pygame.mixer.music.set_volume(.4)

    rule_background = pygame.image.load('image/rule.png')
    next_font = pygame.font.SysFont('bahnschrift', 20)
    next_label = next_font.render('Enter to Play...', True, (0, 0, 0))
    while True:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()              
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_loop()

        screen.blit(rule_background, (0, 0))
        screen.blit(next_label, (15, 430))
        pygame.display.update()
                   
# 스테이지 연결 이미지 
def level1():
    stage1 = pygame.image.load('image/stage1.png')
    screen.blit(stage1, (0,0))
    pygame.display.update()
    i = 0
    while i < 200:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 201
                pygame.quit()
                break

def level2():
    stage2 = pygame.image.load('image/stage2.png')
    screen.blit(stage2, (0,0))
    pygame.display.update()
    i = 0
    while i < 200:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 201
                pygame.quit()
                break

def level3():
    stage3 = pygame.image.load('image/stage3.png')
    screen.blit(stage3, (0,0))
    pygame.display.update()
    i = 0
    while i < 200:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 201
                pygame.quit()
                break
      
# 게임 엔딩 - 성공
def success_screen():
    pygame.mixer.music.load('sound/game_clear.mp3')  
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(.9)

    success_background = pygame.image.load('image/success_screen.png')
    screen.blit(success_background, (0, 0))

    pygame.display.update()
    pygame.time.delay(7000)
    pygame.quit()

# main loop
def main_loop() :

    level1()
    startGame_1()
    runGame_1()

    level2()
    startGame_2()
    runGame_2()  

    level3()
    startGame_3()
    runGame_3()

    success_screen() 

start_menu()