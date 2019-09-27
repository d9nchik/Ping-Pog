from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.counter = 0
        self.hit_bottom = False
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self, paddle):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        self.paddle = paddle
        if pos[1] <= 0:
            self.y = (-1) * self.y
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

        if self.hit_paddle(pos):
            self.y = random.randint(-4, -1)
            self.counter += 1
            if self.paddle.x == 2:
                self.x += 2
            if self.paddle.x == 2:
                self.x -= 2
        if pos[0] <= 0:
            self.x = (-1) * self.x
        if pos[2] >= self.canvas_width:
            self.x = (-1) * self.x

    def restarts(self):
        self.hit_bottom = False
        self.canvas.move(self.id, 0, -300)
        self.counter = 0


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10,
                                          fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2


tk = Tk()
tk.title("Игра")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0,
                highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
entry_message = canvas.create_text(250, 150, text="", font=("Times", 25))


def main(event):
    counter_points = canvas.create_text(390, 50, text="Очки: 0", font=("Times", 9))
    if ball.hit_bottom:
        ball.restarts()
    for x in range(3, 0, -1):
        canvas.itemconfig(entry_message, text="До начала игры %s" % x)
        tk.update()
        time.sleep(1)
    canvas.itemconfig(entry_message, text="")
    while 1:
        if not ball.hit_bottom:
            ball.draw(paddle)
            paddle.draw()
            canvas.itemconfig(counter_points, text="Очки: %s" % ball.counter)
        else:
            canvas.itemconfig(counter_points, text="")
            time.sleep(0.1)
            canvas.itemconfig(entry_message, text="Конец игры!\nВаш счёт: %s\nНажмите чтобы продолжить." % ball.counter)
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)


canvas.itemconfig(entry_message, text="Нажми чтобы начать")
canvas.bind_all('<Button-1>', main)
canvas.mainloop()
