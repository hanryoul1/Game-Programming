# 레벨
# column*row, mines; 9*9, 10; 16*16, 40;30*16, 99

# 메뉴
menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="9*9", command = self.begin)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.destroy)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar)

# 메시지 박스
from tkinter import messagebox
tk.messagebox.showinfo('Win', 'You win!')

# 3차원 행렬 사용
import numpy as np # pip install numpy
pattern = np.arange(5*5*5).reshape(5, 5, 5)
pattern[0][0][0] = 10
pattern = [[[0]*5 for i in range(5)] for k in range(5)]

# 마우스 버튼 이벤트
self.canvas.bind('<Button-1>', self.left_button)
self.canvas.bind('<Button-3>', self.right_button)

def left_button(self, event):
    x = event.x//self.square
    y = event.y//self.square
def right_button(self, event):
    x = event.x//self.square
    y = event.y//self.square

# Recursion
def F(n):
    print(n%10)
    if n//10 > 0:
        F(n//10)

F(123)

def detect_region(self, x, y):
    for yy in range(-1, 2):
        for xx in range(-1, 2):
            if x+xx < 0: continue
            if x+xx >= self.column: continue
            if y+yy < 0: continue
            if y+yy >= self.row: continue
            if self.pattern[y+yy][x+xx][2] != 0: continue
            self.detect_region(x+xx, y+yy)
