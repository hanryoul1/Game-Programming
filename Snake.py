import random
import os
import time
import msvcrt

class Snake:
    def __init__(self, n):
        self.length = n
        self.head = []
        self.tail = []

class SnakeGame:
    direction = {"LEFT":-2, "DOWN":-1, "NON_DIR":0, "UP":1, "RIGHT":2}
    sprite = {"EMPTY":0, "BODY":1, "HEAD":2, "FOOD":3}
    element = {"SPRITE":0, "DIRECTION":1}
    
    def __init__(self, w, h, length, delay):
        self.W = w
        self.H = h
        self.initLen = length
        self.snake = Snake(length)
        self.delay = delay  
        self.board = [[[0]*2 for x in range(self.W)] for y in range(self.H)]
        #self.board[a][b][c]

        self.snake.head = [self.H//2, self.snake.length-1]
        self.snake.tail = [self.H//2, 0]

        for i in range(0, self.snake.length):
            self.board[self.H//2][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
            self.board[self.H//2][i][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        self.board[self.H//2][self.snake.length-1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
        self.board[self.H//2][self.snake.length-1][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        
        x = random.randint(0, self.W-1)
        y = random.randint(0, self.H-1)
        while self.board[y][x][SnakeGame.element["SPRITE"]]\
              != SnakeGame.sprite["EMPTY"]:
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)

        self.board[y][x][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]

    def DrawScene(self):
        os.system('cls||clear')
        for x in range(0, self.W+2):
            print("=", end="")
        print("")
        for y in range(0, self.H):
            print("|", end="")
            for x in range(0, self.W):
                if self.board[y][x][SnakeGame.element["SPRITE"]]\
                   == SnakeGame.sprite["BODY"]:
                    print("+", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["HEAD"]:
                    print("@", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["FOOD"]:
                    print("*", end="")
                else:
                    print(" ", end="")
            print("|")

        for x in range(0, self.W+2):
            print("=", end="")
        print("")
                

    @staticmethod
    def GetDirection():
        rtn = SnakeGame.direction["NON_DIR"]
        msvcrt.getch()
        ch = msvcrt.getch().decode()
        
        if ch == chr(72):
            print("UP")
            rtn = SnakeGame.direction["UP"]
        elif ch == chr(75):
            print("LEFT")
            rtn = SnakeGame.direction["LEFT"]
        elif ch == chr(77):
            print("RIGHT")
            rtn = SnakeGame.direction["RIGHT"]
        elif ch == chr(80):
            print("DOWN")
            rtn = SnakeGame.direction["DOWN"]

        return rtn
        
    def GameLoop(self):
        self.DrawScene()

        current = SnakeGame.direction["RIGHT"]
        ret = SnakeGame.direction["RIGHT"]
        
        while True:
            start = time.time()
            while (time.time() - start) <= self.delay/1000:
                if msvcrt.kbhit():
                    current = SnakeGame.GetDirection()
                
                # Codes 실습1
                if SnakeGame.direction != "DOWN":
                    SnakeGame.direction = "UP"
            
                if SnakeGame.direction != "UP":
                    SnakeGame.direction = "DOWN"

                ret = current
                # 진행방향 반대방향 다르면 아무처리X, 이전 정보 갖고 있음, CURRENT값을 마지막에 RET에 저장
                # 이전과 현재 비교, 갱신(이동할 때 머리와 꼬리 수정/벽 충돌, 먹이 섭취 유무에 따라 다름)
            
            self.DrawScene()
            print("Score: {}".format(self.snake.length - self.initLen))

if __name__ == '__main__' :
    game = SnakeGame(60, 24, 4, 300)
    game.GameLoop()