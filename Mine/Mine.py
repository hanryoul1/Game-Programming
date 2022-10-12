import tkinter as tk
import tkinter.font
from tkinter import messagebox as msg
from tkinter import *
import numpy as np

# 1. 해당 좌표가 지뢰인지 아닌지에 대한 판별 : self.patter[y][x][0]
# 2. 해당 좌표의 8방향 주위 지뢰가 몇 개인지 숫자 정보 : self.pattern[y][x][1]
# 3. 오른쪽 클릭을 해서 깃발을 마킹했는지 : self.pattern[y][x][2]

TILE_SIZE = 24

class GameBoard:
    def __init__(self, w, h , mine, frame):
        self.imgFlag = tk.PhotoImage(file='C:\\Users\\한률\\Desktop\\IGP\\Game-Programming\\Mine\\image\\flag.png')
        self.imgMine = tk.PhotoImage(file='C:\\Users\\한률\\Desktop\\IGP\\Game-Programming\\Mine\\image\\mine.png')
        self.board = tk.Frame(frame) # 게임보드의 타일들을 포함할 프레임 'board' 생성
        self.board.pack()
        self.tileleft = w * h - mine # 승리하기 위해 클릭해야 하는 타일의 수 저장
        self.mine = mine # 지뢰의 수 저장
        self.flag = 0 # 사용된 깃발의 수 저장
        self.disabled = False # 게임 승리, 패배, 일시정지 시에 True
        
        self.width = w
        self.height = h

        self.dataBoard = np.zeros(self.width * self.height, dtype='i')
        self.dataBoard[:mine] = 9
        np.random.shuffle(self.dataBoard)
        self.dataBoard = self.dataBoard.reshape(self.width, self.height)        # 2d-array(w x h)에 지뢰를 9개 무작위 배치

        for x in range(self.width):
            for y in range(self.height):
                self.dataBoard[x][y] = self.boardCheck(x, y)        # dataBoard 9가 아닌(지뢰가 없는) 타일에 인접 지뢰 수 저장

        self.tileFrame = [[0] * self.height for _ in range(self.width)]
        self.tileBack = [[0] * self.height for _ in range(self.width)]
        self.tileBtn = [[0] * self.height for _ in range(self.width)]
        self.tileBtnImg = [[0] * self.height for _ in range(self.width)]  # 타일별 프레임, 라벨, 버튼, 변수 초기화


    def boardCheck(self, x, y):     # dataBoard[x][y] 칸의 지뢰여부 또는 인접지뢰 수를 출력
        if self.dataBoard[x][y] == 9:
            return 9        # dataBoard[x][y] == 9 이면 그대로 반환

        relativeCoord = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))      # 주변 칸의 상대좌표
        result = 0
        for crd in relativeCoord:
            if 0 <= x + crd[0] < self.width and 0 <= y + crd[1] < self.height:  # 주변 칸의 좌표가 유효한지 확인
                if self.dataBoard[x + crd[0]][y + crd[1]] == 9:                 # 주변 칸의 데이터가 9인지 확인
                    result += 1
        return result       # dataBoard[x][y] != 9 이면 인접 지뢰 수 반환


    def boardActivate(self):        # __init__에서 구성된 보드를 부모 프레임에 표시
        for x in range(self.width):
            for y in range(self.height):        # 보드의 모든 타일에 대하여
                self.tileFrame[x][y] = tk.Frame(self.board, width=TILE_SIZE, height=TILE_SIZE, padx=0, pady=0, relief='sunken', bd=1)
                self.tileFrame[x][y].pack_propagate(False)
                self.tileFrame[x][y].grid(column=x, row=y)      # 타일의 사이즈를 가진 작은 프레임 생성

                backText = self.dataBoard[x][y]
                if backText == 0:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text='')
                elif backText == 9:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text='', image=self.imgMine)
                else:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text=backText)     # 타일의 데이터에 따라 빈칸, 이미지, 숫자 라벨 구성 (패킹하지 않음)

                self.tileBtn[x][y] = tk.Button(self.tileFrame[x][y], command=(lambda x_=x, y_=y: self.leftClick(x_, y_)), bd=1)
                self.tileBtn[x][y].bind('<Button-3>', (lambda event, x_=x, y_=y: self.rightClick(x_, y_)))
                self.tileBtn[x][y].pack(fill=tk.BOTH, expand=tk.YES)  # 각 타일에 버튼 생성, command 지정 및 우클릭 이벤트 바인드                                      # 우클릭 횟수에 따라 사용된 깃발 수를 관리


    def leftClick(self, x, y):     # x, y 좌표의 타일이 클릭되었을 때 호출
        if not self.disabled:       # 보드가 활성화 되어있으면,
            self.tileBtn[x][y].pack_forget()
            self.tileBack[x][y].pack(fill=tk.BOTH, expand=tk.YES)       # 버튼을 언패킹. 지뢰 그림, 인접 지뢰 숫자 등을 포함한 라벨 패킹

            if self.dataBoard[x][y] == 9:
                self.tileBack[x][y].configure(background='RED', relief='flat')
                self.lose()     # 지뢰를 클릭했다면, 클릭한 칸의 배경을 붉게하고, 게임 종료
            else:
                self.tileleft -= 1      # 지뢰가 아니라면 클리어까지 남은 타일 수를 1 감소
                if self.tileleft == 0:
                    self.win()          # 클리어 까지 남은 타일의 수가 0이 되면 게임에서 승리

                if self.dataBoard[x][y] == 0:       # 인접 지뢰 숫자가 0인 타일에서 주변 타일로 재귀호출
                    relativeCoord = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
                    for crd in relativeCoord:
                        if 0 <= x + crd[0] < self.width and 0 <= y + crd[1] < self.height and self.tileBtn[x + crd[0]][y + crd[1]].winfo_ismapped():
                            self.leftClick(x + crd[0], y + crd[1])     # 유효한 인접 타일 중 클릭되지 않은 타일을 자동으로 클릭

            if self.tileBtnImg[x][y] == 1:      # 깃발이 사용된 칸을 클릭한 것이면, 우클릭 이벤트를 발생 (사용된 깃발 수 관리를 위해)
                self.rightClick(x, y)
                
            self.canvas.bind('<Button-1>', self.leftClick) # 지뢰오픈


    def rightClick(self, x, y):        # x, y 좌표의 타일이 우클릭되었을 때 호출
        if not self.disabled:               # 보드가 활성화 되어있으면,
            self.tileBtnImg[x][y] = (self.tileBtnImg[x][y] + 1) % 3
            if self.tileBtnImg[x][y] == 0:
                self.tileBtn[x][y].configure(image='', text='')
            elif self.tileBtnImg[x][y] == 1:
                self.tileBtn[x][y].configure(image=self.imgFlag, text='')
                self.flag += 1
            else:
                self.tileBtn[x][y].configure(image='', text='?')        # 타일의 버튼 이미지를 [0 : 표시하지 않음, 1 : 깃발, 2 : 물음표]로 표시함
                self.flag -= 1                                          # 우클릭 횟수에 따라 사용된 깃발 수를 관리
            
            self.canvas.bind('<Button-3>', self.rightClick) # 깃발표시


    def win(self):
        tk.messagebox.showinfo('Win', 'You win!')
        self.disabled = True


    def lose(self):
        tk.messagebox.showinfo('LOSE', 'You lose..')
        self.disabled = True
        

    def unpackBoard(self):
        self.board.pack_forget() 

def gameStart_level1(canvas):
    global game     # 전역변수 game 사용

    if game is not None:
        game.unpackBoard()      # 실행 중이던 게임이 있으면 화면에서 지움

    w = 9
    h = 9
    mine = 10
    game = GameBoard(w, h, mine, canvas)     # 사용자가 선택한 레벨에 따라 게임보드 생성
    game.boardActivate()

    uiPlace(w, h)
    game.disabled = False       # ui 재설정 및 게임 활성화

def gameStart_level2(canvas):
    global game     # 전역변수 game 사용

    if game is not None:
        game.unpackBoard()      # 실행 중이던 게임이 있으면 화면에서 지움

    w = 16
    h = 16
    mine = 40
    game = GameBoard(w, h, mine, canvas)     # 사용자가 선택한 레벨에 따라 게임보드 생성
    game.boardActivate()

    master.geometry('%dx%d+%d+%d' % ((w + 1) * TILE_SIZE, (h + 1) * TILE_SIZE + 64, (scrW - (w + 1) * TILE_SIZE) / 2, (scrH - (h + 1) * TILE_SIZE - 64) / 2))
    mainCanvas.configure(width=(w + 1) * TILE_SIZE, height=(h + 1) * TILE_SIZE)      # 화면의 사이즈와 위치 조정

    uiPlace(w, h)
    game.disabled = False       # ui 재설정 및 게임 활성화

def gameStart_level3(canvas):
    global game     # 전역변수 game 사용

    if game is not None:
        game.unpackBoard()      # 실행 중이던 게임이 있으면 화면에서 지움

    w = 30
    h = 16
    mine = 99
    game = GameBoard(w, h, mine, canvas)     # 사용자가 선택한 레벨에 따라 게임보드 생성
    game.boardActivate()   

    uiPlace(w, h)
    game.disabled = False       # ui 재설정 및 게임 활성화

    master.geometry('%dx%d+%d+%d' % ((w + 1) * TILE_SIZE, (h + 1) * TILE_SIZE + 64, (scrW - (w + 1) * TILE_SIZE) / 2, (scrH - (h + 1) * TILE_SIZE - 64) / 2))
    mainCanvas.configure(width=(w + 1) * TILE_SIZE, height=(h + 1) * TILE_SIZE)      # 화면의 사이즈와 위치 조정

    uiPlace(w, h)
    game.disabled = False       # ui 재설정 및 게임 활성화
    
def uiPlace(w, h):
    mainCanvas.place(y=32)
    winLose.place(x=w * TILE_SIZE / 2, y=(h + 1) * TILE_SIZE + 32)      # mainWindow 의 위젯들 배치
    
game = None

def quitGame():
    if msg.askokcancel('Hello, Mine!', '게임을 종료하시겠습니까?'):
        master.destroy()        # 게임종료 대화상자를 표시, 게임종료


master = Tk()
scrW = master.winfo_screenwidth()
scrH = master.winfo_screenheight()
master.geometry('%dx%d+%d+%d' % (10 * TILE_SIZE, 10 * TILE_SIZE + 64, (scrW - 10 * TILE_SIZE)/2, (scrH - 10 * TILE_SIZE - 64)/2))
master.resizable(False, False)
master.title('Hello, Mine!')
master.lift()       # mainWindow tk 윈도우를 생성, 초기설정

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="9*9", command = (lambda: gameStart_level1(master))) # 항목 추가
filemenu.add_command(label="16*16", command = (lambda: gameStart_level2(master)))
filemenu.add_command(label="16*30", command = (lambda: gameStart_level3(master)))  # self.gamestart
filemenu.add_separator() # 분리선 추가
filemenu.add_command(label="Exit", command = (lambda: quitGame()))
master.config(menu=menubar)

master.protocol("WM_DELETE_WINDOW", quitGame)       # 창 닫기 버튼 클릭 시 quitGame 함수 호출

defaultFont = tk.font.Font(family='맑은 고딕', size=10, weight='bold')
master.option_add("*Font", defaultFont)             # mainWindow 기본 폰트 지정
master.mainloop() 

""" mainWindow 의 GUI 구성 """ 
mainCanvas = tk.Canvas(master, width=10 * TILE_SIZE, height=10 * TILE_SIZE, padx=11, pady=11, relief='sunken', bd=1)
mainCanvas.pack_propagate(False)     # 게임이 들어갈 mainFrame 생성

winLoseFont = tk.font.Font(family='맑은 고딕', size=14, weight='bold')
winLose = tk.Label(master, text='', anchor=tk.CENTER, font=winLoseFont)         # 승, 패 표시 라벨 생성

uiPlace(9, 9) # mainWindow 위젯 배치 함수



"""
# 3차원 행렬 사용
pattern = np.arange(5*5*5).reshape(5, 5, 5)
pattern[0][0][0] = 10
pattern = [[[0]*5 for i in range(5)] for k in range(5)]

# Recursion
def F(n):
    print(n%10)
    if n//10 > 0:
        F(n//10)
F(123)

# 재귀함수
def detect_region(self, x, y):
    for yy in range(-1, 2):
        for xx in range(-1, 2):
            if x+xx < 0: continue
            if x+xx >= self.column: continue
            if y+yy < 0: continue
            if y+yy >= self.row: continue
            if self.pattern[y+yy][x+xx][2] != 0: continue

            self.detect_region(x+xx, y+yy)
"""


""" 
def gameStart(canvas):
    global game     # 전역변수 game 사용

    if game is not None:
        game.unpackBoard()      # 실행 중이던 게임이 있으면 화면에서 지움

    if level.get() == 0:
        w = 9
        h = 9
        mine = 10
    elif level.get() == 1:
        w = 16
        h = 16
        mine = 40
    else:
        w = 30
        h = 16
        mine = 99 
"""

"""
master.title("Hello, Mine!")
canvas = Canvas(master, width = 200, height = 150 )
menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="9*9", command = (lambda: gameStart(canvas))) # 항목 추가
filemenu.add_command(label="16*16", command = (lambda: gameStart(canvas)))
filemenu.add_command(label="16*30", command = (lambda: gameStart(canvas)))  # self.gamestart
filemenu.add_separator() # 분리선 추가
filemenu.add_command(label="Exit", command = master.destroy)
master.config(menu=menubar)
"""

"""
mainWindow = tk.Tk()
scrW = mainWindow.winfo_screenwidth()
scrH = mainWindow.winfo_screenheight()
mainWindow.geometry('%dx%d+%d+%d' % (10 * TILE_SIZE, 10 * TILE_SIZE + 64, (scrW - 10 * TILE_SIZE)/2, (scrH - 10 * TILE_SIZE - 64)/2))
mainWindow.resizable(False, False)
mainWindow.title('Hello, Mine!')
mainWindow.lift()       # mainWindow tk 윈도우를 생성, 초기설정

mainWindow.protocol("WM_DELETE_WINDOW", quitGame)       # 창 닫기 버튼 클릭 시 quitGame 함수 호출

defaultFont = tk.font.Font(family='맑은 고딕', size=10, weight='bold')
mainWindow.option_add("*Font", defaultFont)             # mainWindow 기본 폰트 지정

"""