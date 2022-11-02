"""Import"""
import random
from collections import defaultdict
from pyglet.image import load, ImageGrid, Animation
# 이미지 애니메이션을 위한 모듈 추가

import time # time_out 구현
from pyglet.window import key
import cocos.layer
import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

"""Actor"""
class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position, self.width * 0.5, self.height * 0.5)
    
    # 이동이 있는 경우 offset만큼 더 이동
    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    # 시간
    def update(self, elapsed):
        pass
    
    # 충돌에 대한 처리
    def collide(self, other):
        pass

"""PlayerCannon"""
class PlayerCannon(Actor):
    KEYS_PRESSED = defaultdict(int)

    def __init__(self, x, y):
        super(PlayerCannon, self).__init__('Cocos/cannon.png', x, y)
        self.speed = eu.Vector2(200, 0)

    def update(self, elapsed):
        pressed = PlayerCannon.KEYS_PRESSED
        space_pressed = pressed[key.SPACE] == 1
        # 스페이스가 눌러진 경우, space_pressed가 True값을 가짐
        # if PlayerShoot.INSTANCE is None and space_pressed:
        if space_pressed:
            #PlayerShoot 클래스의 멤버인 객체가 없고 스페이스가 눌러진 경우
            self.parent.add(PlayerShoot(self.x, self.y + 50))
            space_pressed = False
            # PlayerShoot.bullet_xy.append((self.x, self.y))
            PlayerShoot.INSTANCE = None
            #Actor에 총알 추가
        else:
            PlayerShoot.INSTANCE = None
        
        w = self.width * 0.5
        movement = pressed[key.RIGHT] - pressed[key.LEFT]
        # RIGHT만 누른경우 x==1, LEFT만 누른 경우 x==-1
        # 둘다 누른 경우 x == 0, 둘다 안 누른 경우 x ==0
        
        if (w < self.x) or (self.x < self.parent.width - w):
        # if movement != 0 and w <= self.x <= self.parent.width - w:
        # A,B를 비교(두 개 사건을 비교) / and or 활용
            self.move(self.speed * movement * elapsed)

            if self.x <= w:
                self.x = w
            if self.x >= self.parent.width - w:
                self.x = self.parent.width - w
            # if문 바꾸어 실습 진행
            # 좌/우 벽면으로 이동시 오류 발생
            # 현재 상태가 아닌, 미래 상태를 기준으로 변경

    def collide(self, other):
        other.kill()
        self.kill()

"""GameLayer""" # 레이어와 텍스트를 제외한 실제 화면
class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    def on_key_press(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 0
        # KEYS_PRESSED = static member
    
    def __init__(self, hud):
        super(GameLayer, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.hud = hud
        self.width = w
        self.height = h
        self.lives = 3
        self.score = 0
        # self.start_time = int(time.time())
        self.time = 100
        self.update_score()
        self.create_player()
        self.update_time()
        self.create_alien_group(100, 300)
        cell = 1.25 * 50
        self.collman = cm.CollisionManagerGrid(0, w, 0, h, cell, cell)
        self.schedule(self.update)

    def create_player(self):
        self.player = PlayerCannon(self.width * 0.5, 50)
        self.add(self.player)
        self.hud.update_lives(self.lives)

    def update_score(self, score=0):
        self.score += score
        self.hud.update_score(self.score)
        
        # 성능향상_1
        # 목표 점수 1000점 달성 -> Game Clear
        if self.score >= 1000:
            self.hud.show_game_clear()

    # 성능향상_2
    # time_out 설정 -> Time Over
    def update_time(self, time=100):
        self.hud.update_time(self.time)

    def create_alien_group(self, x, y):
        self.alien_group = AlienGroup(x, y)
        for alien in self.alien_group: # literable(literator)
        # self.ailen_group은 container 형식으로 묶음
            self.add(alien)

    def update(self, dt):
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
            if not self.collman.knows(node):
                self.remove(node)
        self.collide(PlayerShoot.INSTANCE)
        # self.collide(PlayerShoot.parent.)
        if self.collide(self.player):
            self.respawn_player()

        # Alien이 쏘는 shoot
        # 한 열에서는 하나의 미사일만 발사할 수 있도록
        for column in self.alien_group.columns:
            shoot = column.shoot()
            if shoot is not None:
                self.add(shoot)

        for _, node in self.children:
            node.update(dt)
        self.alien_group.update(dt)
        if random.random() < 0.001:
            self.add(MysteryShip(50, self.height - 50))
            # MysteryShip의 랜덤 생성
            # 업데이트 할 때마다 1/1000의 확률로 생성

    def collide(self, node):
        if node is not None:
            for other in self.collman.iter_colliding(node):
                node.collide(other)
                return True
        return False
    
    def respawn_player(self):
        self.lives -= 1
        if self.lives < 0:
            self.unschedule(self.update)
            self.hud.show_game_over()
        else:
            self.create_player()

    def time_out(self, time):
        if time <= 0:
            self.unschedule(self.update)
            self.hud.show_time_out()

"""Alien"""
class Alien(Actor):
    def load_animation(image):
        # 이미지를 애니메이션으로 업로드 하는 함수를 pyglet 모듈
        seq = ImageGrid(load(image), 2, 1)
        # 이미지가 2줄
        return Animation.from_image_sequence(seq, 0.5)
    
    TYPES = { # 각각의 요소는 '애니메이션,점수' 튜플 형식으로 저장
        '1': (load_animation('Cocos/alien1.png'), 40),
        '2': (load_animation('Cocos/alien2.png'), 20),
        '3': (load_animation('Cocos/alien3.png'), 10)
    }

    # self 파라미터를 받지 않는 함수 : 객체와 상관없이 사용하는 static 메소드(전역함수로 활용)
    def from_type(x, y, alien_type, column):
        animation, score = Alien.TYPES[alien_type]
        return Alien(animation, x, y, score, column)
    
    def __init__(self, img, x, y, score, column=None):
        super(Alien, self).__init__(img, x, y)
        self.score = score
        self.column = column

    def on_exit(self):
        super(Alien, self).on_exit()
        if self.column:
            self.column.remove(self)

"""AlienColumn"""
class AlienColumn(object):
    def __init__(self, x, y):
        alien_types = enumerate(['3', '3', '2', '2', '1'])
        self.aliens = [Alien.from_type(x, y+i*60, alien, self) for i, alien in alien_types]

    def should_turn(self, d):
        if len(self.aliens) == 0:
            return False
        alien = self.aliens[0]
        x, width = alien.x, alien.parent.width
        return x >= width - 50 and d == 1 or x <= 50 and d == -1
    
    def remove(self, alien):
        self.aliens.remove(alien)

    def shoot(self):
        if random.random() < 0.001 and len(self.aliens) > 0:
            pos = self.aliens[0].position
            return Shoot(pos[0], pos[1] - 50)
        return None

"""AlienCGroup"""
class AlienGroup(object):
    def __init__(self, x, y):
        self.columns = [AlienColumn(x + i * 60, y)
                        for i in range(10)]
        self.speed = eu.Vector2(10, 0)
        self.direction = 1
        self.elapsed = 0.0
        self.period = 1.0

    def update(self, elapsed):
        self.elapsed += elapsed
        while self.elapsed >= self.period:
            self.elapsed -= self.period
            offset = self.direction * self.speed
            if self.side_reached():
                self.direction *= -1
                offset = eu.Vector2(0, -10) 
            for alien in self:
                alien.move(offset)

    def side_reached(self):
        return any(map(lambda c: c.should_turn(self.direction), self.columns))

    def __iter__(self):
        for column in self.columns:
            for alien in column.aliens:
                yield alien

"""Shoot"""
class Shoot(Actor):
    def __init__(self, x, y, img='Cocos/shoot.png'):
        super(Shoot, self).__init__(img, x, y)
        self.speed = eu.Vector2(0, -400)

    def update(self, elapsed):
        self.move(self.speed * elapsed)

"""PlayerShoot"""
class PlayerShoot(Shoot):
    # bullet_xy = []
    INSTANCE = None

    def __init__(self, x, y):
        super(PlayerShoot, self).__init__(x, y, 'Cocos/laser.png')
        self.speed *= -1 
        PlayerShoot.INSTANCE = self
        # print("INSTANCE:", PlayerShoot.INSTANCE)                   

    def collide(self, other):
        if isinstance(other, Alien):
            self.parent.update_score(other.score)
            other.kill()
            self.kill()

    def on_exit(self):
        super(PlayerShoot, self).on_exit()
        PlayerShoot.INSTANCE = None

"""HUD""" # 점수, 라이프, 텍스트 등 출력
class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.score_text = cocos.text.Label('', font_size=18)
        self.score_text.position = (150, h - 40)
        self.lives_text = cocos.text.Label('', font_size=18)
        self.lives_text.position = (w - 120, h - 40)
        self.time_text = cocos.text.Label('', font_size=18) # time_text
        self.time_text.position = (20, h - 40)
        self.add(self.score_text)
        self.add(self.lives_text)
        self.add(self.time_text)

    def update_score(self, score):
        self.score_text.element.text = 'Score: %s' % score

    def update_lives(self, lives):
        self.lives_text.element.text = 'Lives: %s' % lives

    def update_time(self, time):
        self.time_text.element.text = 'Time: %s' % time

    def show_game_over(self):
        w, h = cocos.director.director.get_window_size()
        game_over = cocos.text.Label('Game Over', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_over.position = w * 0.5, h * 0.5
        self.add(game_over)
    
    def show_game_clear(self):
        w, h = cocos.director.director.get_window_size()
        game_clear = cocos.text.Label('Game Clear', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_clear.position = w * 0.5, h * 0.5
        self.add(game_clear)

    def show_time_out(self):
        w, h = cocos.director.director.get_window_size()
        game_clear = cocos.text.Label('Time Out', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_clear.position = w * 0.5, h * 0.5
        self.add(game_clear)

"""MysteryShip"""
class MysteryShip(Alien):
    SCORES = [10, 50, 100, 200]

    def __init__(self, x, y):
        score = random.choice(MysteryShip.SCORES)
        super(MysteryShip, self).__init__('Cocos/alien4.png', x, y, 
                                          score)
        self.speed = eu.Vector2(150, 0)

    def update(self, elapsed):
        self.move(self.speed * elapsed)

"""Main"""
if __name__ == '__main__':
    cocos.director.director.init(caption='Cocos Invaders', 
                                 width=800, height=650)
    main_scene = cocos.scene.Scene()
    hud_layer = HUD()
    main_scene.add(hud_layer, z=1)
    game_layer = GameLayer(hud_layer)
    main_scene.add(game_layer, z=0)
    cocos.director.director.run(main_scene)