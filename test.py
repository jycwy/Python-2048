import tkinter as tk
import time as time
from PIL import Image , ImageTk

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
class Gameframe
    def __init__(self):
        self.root = tk.Tk()
        self.world = World(self.root)
        self.GameStart()

    def GameStart(self):
        while true:
            time.sleep(0.03)
            self.root.update()
            self.root.update_idletasks()
            self.world.move()


class World
    def __init__(self,root):
        self.canvas = tk.Canvas(root,width = WINDOW_WIDTH,height = WINDOW_HEIGHT )
        self.canvas.bind("<key>",self.key_callback)
        self.canvas.focus_set()
        self.canvas.pack() #布局
        self.all_fighters = []
        self.hero = Fighter(100,100,canvas = self.canvas)  #为什么要加canvas
        self.all_fignter.append(self.hero)

    def key_callback(self,event):
        key_down = event.char

        if key_down == "w"
            self.hero.direction = "forward"
        if key_down == "s"
            self.hero.direction = "backward"
        if key_down == "a"
        self.hero.direction = "left"
        if key_down == "d"
            self.hero.direction = "right"

    def move(self):
        for fighter in self.all_fighters:
            if fighter.direction == "forward":
                self.canvas.move(fighter.image,0,-fighter.speed)
            if fighter.direction == "backward":
                self.canvas.move(fighter.image,0,fighter.speed)
            if fighter.direction == "left":
                self.canvas.move(fighter.image,-fighter.speed,0)
            if fighter.direction == "right":
                self.canvas.move(fighter.image,fighter.speed,0)
            fighter.direction = stop
class Fighter
    def __init__(self,x,y,canvas,speed=5):
       ### self.x = x
        self.y = y
        self.speed = speed
        image = Image.open("image/fighter foreard.png")
        self.imageTk = ImageTk.PhotoImage(image=image)
        self.image = canvas.create_image(x,WINDOW_HEIGHT - y,image = self.imageTk)
        self.direction = "stop"  #？？？


game = Gameframe()