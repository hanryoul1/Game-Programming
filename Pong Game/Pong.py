# <Pong.py 완성하기>
#공이 움직이는 방향 : 4방향 (45 90 135 180) / 교재는 1, -1로 설정
#게임이 진행되며 속력증가 설정 = 공에 대한 속도 정보 필요
#방향 단위 vector로 하면 용이(?)  
#tkinter에서는 내려갈수록 커지는 y좌표 사용
#ball class 2개 생성 : paddle에 붙어 있는 ball / 떨어져나가는 ball

"""
<Step_01>
from tkinter import Tk
root = Tk() #Tk라는 class 생성
root.title('Hello')
root.mainloop()
"""

"""
<Step_02>
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
"""
#<Step_03>
import tkinter as tk
nW = 600
nH = 400
root = tk.Tk()
frame = tk.Frame(root)
canvas = tk.Canvas(frame, 
width=nW, height=nH,bg='#aaaaff')
# Canvas (master, option=value, ... )
# #ff0000 -> red

coord = 10, 50, nW-10, nH-50 #tuple 
arc = canvas.create_arc(coord, start=0, 
extent=270, fill='red')
filename = tk.PhotoImage(file = 'C:\\Users\\한률\\Desktop\\경희대\\게임프로그래밍입문\\image\\ball.png')
Image = canvas.create_image(97, 97, 
anchor=tk.CENTER, image=filename)
# anchor: NW, N, NE, W, CENTER, E, SW, S, SE

text = canvas.create_text(0, 0, text = 'Ball', 
anchor = tk.NW, font = ('Arial', '32'))

frame.pack() # pack: displaying the widget
canvas.pack() # on its parent container
root.title('Hello, Pong!')
root.mainloop()