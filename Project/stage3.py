import pygame
import time
import sys
import os

######################################################################################################
# 전역 변수
clock = pygame.time.Clock()

screen_width = 640 
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("image/background.png")

health = 3
total_time = 30
######################################################################################################

def success_screen():
    pygame.mixer.music.load('sound/game_clear.mp3')  
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(.9)

    success_background = pygame.image.load('image/success_screen.png')
    screen.blit(success_background, (0, 0))

    pygame.display.update()
    pygame.time.delay(7000)
    pygame.quit()

def death_screen():  
    pygame.mixer.music.load('sound/game_over.wav')  
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(.9)

    death_background = pygame.image.load('image/death_screen.png')
    screen.blit(death_background, (0, 0))

    pygame.display.update()
    pygame.time.delay(7000)
    pygame.quit()

def startGame_3():
    global screen, clock
    global background, stage, character, char_life, weapon, ball_images
    global music, bulletSound, hitSound
    # pygame.init()
    # screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pang Pang!")
    clock = pygame.time.Clock()

    # 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 폰트 등)
    current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
    image_path = os.path.join(current_path, "image") # image 폴더 위치 반환

    background = pygame.image.load(os.path.join(image_path, "back3.png"))
    stage = pygame.image.load(os.path.join(image_path, "stage.png"))
    character = pygame.image.load(os.path.join(image_path, "character.png"))
    char_life = pygame.image.load('image/heart.png')
    weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
    ball_images = [
        pygame.image.load(os.path.join(image_path, "ball1_stage3.png")),
        pygame.image.load(os.path.join(image_path, "ball2_stage3.png")),
        pygame.image.load(os.path.join(image_path, "ball3_stage3.png")),
        pygame.image.load(os.path.join(image_path, "ball4_stage3.png"))
    ]  

    # 사운드 로딩
    bulletSound = pygame.mixer.Sound('sound/gun_shot.mp3')
    hitSound = pygame.mixer.Sound('sound/balloon_burst.wav')
    music = pygame.mixer.music.load('sound/level3.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.9)

def explode_3():
    global health
    global total_time, elapsed_time
    health -= 1

    total_time = total_time - elapsed_time
    pygame.display.update()
    time.sleep(2)
    runGame_3()

def runGame_3():
    global health, total_time, elapsed_time

    # Font 정의
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 25, True) 
    start_ticks = pygame.time.get_ticks() # 시작 시간 정의
    
    # 스테이지 만들기
    stage_size = stage.get_rect().size
    stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

    # 캐릭터 만들기
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - stage_height - character_height

    # 캐릭터 이동 방향
    character_to_x = 0

    # 캐릭터 이동 속도
    character_speed = 5

    # 무기 만들기
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]

    # 무기는 한 번에 여러 발 발사 가능
    weapons = []

    # 무기 이동 속도 
    weapon_speed = 10

    # 공 크기에 따른 최초 스피드
    ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

    # 공들
    balls = []

    # 최초 발생하는 큰 공 추가
    balls.append({
        "pos_x" : 50, # 공의 x 좌표
        "pos_y" : 50, # 공의 y 좌표
        "img_idx" : 0, # 공의 이미지 인덱스
        "to_x" : 3, # x축 이동방향 / -3 -> 왼쪽, 3 -> 오른쪽
        "to_y": -6, # y축 이동방향
        "init_spd_y" : ball_speed_y[0]}) # y 최초 속도

    # 사라질 무기와 공 정보 저장 변수
    weapon_to_remove = -1
    ball_to_remove = -1

    running = True
    while running:
        dt = clock.tick(30)

        # 2. 이벤트 처리 (키보드, 마우스 등)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    character_to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    character_to_x += character_speed
                elif event.key == pygame.K_SPACE: # 무기 발사
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0

        # 3. 게임 캐릭터 위치 정의
        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 무기 위치 조정
        weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로
        
        # 천장에 닿은 무기 없애기
        weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
        
        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls): # enumerate : 리스트의 원소에 순서값을 부여해주는 함수
            ball_pos_x = ball_val["pos_x"] # 50
            ball_pos_y = ball_val["pos_y"] # 50
            ball_img_idx = ball_val["img_idx"] # 0

            ball_size = ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * (-1)

            # 세로 위치
            # 스테이지에 튕겨서 올라가는 처리
            if ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] = ball_val["init_spd_y"]
            else: # 그 외의 모든 경우에는 속도를 증가(-값에서 +값으로 증가)
                ball_val["to_y"] += 0.5
            
            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        # 4. 충돌 처리
        # 캐릭터 rect 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls): # enumerate : 리스트의 원소에 순서값을 부여해주는 함수
            ball_pos_x = ball_val["pos_x"] # 50
            ball_pos_y = ball_val["pos_y"] # 50
            ball_img_idx = ball_val["img_idx"] # 0

            # 공 rect 정보 업데이트
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌 처리
            if character_rect.colliderect(ball_rect):
                bulletSound.play()
                broken_heart = pygame.image.load('image/broken_heart.png') 
                screen.blit(broken_heart, (300 - (broken_heart.get_width()/2), 60))
                pygame.display.update()

                if health <= 0:
                    running = False
                    time.sleep(2)
                    death_screen()

                else:
                    explode_3()
            
            # 공과 무기들 충돌 처리
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_pos_x = weapon_val[0]
                weapon_pos_y = weapon_val[1]

                # 무기 rect 정보 업데이트
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_pos_x
                weapon_rect.top = weapon_pos_y

                # 충돌 체크
                if weapon_rect.colliderect(ball_rect):
                    hitSound.play()
                    weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                    ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                    # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                    if ball_img_idx < 3:
                        # 현재 공 크기 정보를 가지고 옴
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]

                        # 나눠진 공 정보
                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                        # 왼쪽으로 튕겨나가는 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : -3, # x축 이동방향 / -3 -> 왼쪽, 3 -> 오른쪽
                            "to_y": -6, # y축 이동방향
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})
                        
                        # 오른쪽으로 튕겨나가는 작은 공
                        balls.append({
                            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                            "to_x" : 3, # x축 이동방향 / -3 -> 왼쪽, 3 -> 오른쪽
                            "to_y": -6, # y축 이동방향
                            "init_spd_y" : ball_speed_y[ball_img_idx + 1]})
                    break
            else: # 계속 게임을 진행 
                continue # 안쪽 for문 조건이 맞지 않으면 continue, 바깥 for문 계속
            break # 안쪽 for문 break를 만나면 진입 가능 -> 2중 for문 한번에 탈출

        # 충돌된 공 or 무기 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

        # 모든 공을 없앤 경우 게임 종료 (성공)
        if len(balls) == 0:
            running = False
            pygame.time.delay(1000)
            success_screen()

        # 5. 화면에 그리기
        screen.blit(background, (0, 0))

        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
        for ind, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

        screen.blit(stage, (0, screen_height - stage_height))
        screen.blit(character, (character_x_pos, character_y_pos))
        
        # 목숨 만들기
        #screen.blit(char_life, (540, 50)) 
        screen.blit(char_life, (400, 15)) 
        life = font.render('x' + str(health), 1, (0,0,0))
        #screen.blit(life, (595, 45))
        screen.blit(life, (435, 10))
        text = font.render('Stage: 3/3', 1, (0,0,0))
        screen.blit(text, (490, 10))
        
        # 경과 시간 계산
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
        timer = font.render("Time : {}".format(int(total_time - elapsed_time)), True, (0, 0, 0))
        screen.blit(timer, (15, 10))

        # 시간 초과했다면
        if total_time - elapsed_time <= 0:
            running = False
            time.sleep(2)
            death_screen()

        pygame.display.update()