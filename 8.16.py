import tkinter as tk
import time as time
import random
from PIL import Image ,ImageTk

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

class GameFrame:
    def __init__(self):
        self.root = tk.Tk()
        self.field = GameField(self.root)
        while True:
            time.sleep(0.03)
            self.root.update()
            self.root.update_idletasks()



class GameField:
    def __init__(self,root):
        self.canvas = tk.Canvas(root,width = WINDOW_WIDTH,height = WINDOW_HEIGHT,bg = "white")
        self.score = 0
        self.best = 0

        self.canvas.bind('<Key>',self.key_callback)
        self.canvas.focus_set()
        self.canvas.pack()

        self.all_numbers =[]

        self.reset()

    def key_callback(self,event):
        pass

    def spawn(self):
        image2 = Image.open("2048_image/2.png")
        iamge2 = image2.resize((WINDOW_WIDTH /4,WINDOW_WIDTH / 4),Image.ANTIALIAS)

        image4 = Image.open("2048_image/4.png")
        iamge4 = image4.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        random_number = random.random()
        if random_number < 0.9:
            self.image =ImageTk.PhotoImage(image = iamge2)
        else:
            self.image = ImageTk.PhotoImage(image = image4)

        i = random.choice([1,2,3,4])
        j = random.choice([1,2,3,4])

        self.canvas.create_image((i-1)*100 + 50,WINDOW_HEIGHT-(j-1)*100-50,image=self.image)

    def reset(self):
        if self.score > self.best:
            self.best = self.score
        self.score = 0
        self.spawn()
        self.spawn()



    def move(self):
        pass


class Numbers
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image

        image2 = Image.open("2048_image/2.png")
        iamge2 = image2.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        image4 = Image.open("2048_image/4.png")
        iamge4 = image4.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        image8 = Image.open("2048_image/8.png")
        iamge8 = image8.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        image16 = Image.open("2048_image/16.png")
        iamge16 = image4.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        image32 = Image.open("2048_image/32.png")
        iamge32 = image2.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)

        image64 = Image.open("2048_image/64.png")
        iamge64 = image4.resize((WINDOW_WIDTH / 4, WINDOW_WIDTH / 4), Image.ANTIALIAS)


game = GameFrame()