# <Pong.py 완성하기>
#공이 움직이는 방향 : 4방향 (45 90 135 180) / 교재는 1, -1로 설정
#게임이 진행되며 속력증가 설정 = 공에 대한 속도 정보 필요
#방향 단위 vector로 하면 용이(?)  
#tkinter에서는 내려갈수록 커지는 y좌표 사용


"""
from tkinter import Tk
root = Tk() #Tk라는 class 생성
root.title('Hello')
root.mainloop()
"""

import tkinter as tk
class Game(tk.Frame):
    def __init__(self, master): # master : tkinter > Frame > Canvas   
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg ='#aaaaff', #RGB/R=aa, G=aa, B=ff
                                width = self.width,
                                height = self.height,)

        self.canvas.pack()
        self.pack()
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, pong!')
    game = Game(root)
    game.mainloop()


