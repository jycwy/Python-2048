import tkinter  as tk
import time  as time
from PIL import Image , ImageTk
import  random
import pygame
import json
import os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

class GameFrame:
    def __init__(self):
        self.root = tk.Tk()
        self.world=World(self.root)
        self.gameStart()

    def gameStart(self):
        while True:
            time.sleep(0.03)
            self.root.update()
            self.root.update_idletasks()
            if self.world.world_run == True:
                self.world.run()

class World:
    def __init__(self,root):
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,bg = "white")
        image = Image.open("image/bg.jpg")
        image = image.resize((WINDOW_WIDTH,WINDOW_HEIGHT), Image.ANTIALIAS)

        self.bg = ImageTk.PhotoImage(image = image)
        self.canvas.create_image(WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2,image = self.bg)




        self.canvas.bind("<Key>",self.key_callback)
        self.canvas.focus_set()
        self.canvas.pack()
        self.all_fighters =[]

        pygame.mixer.init() #initialize the sound

        self.hero = Fighter(100,100,hp = 10,canvas= self.canvas,is_hero = True)
        self.all_fighters.append(self.hero)
        self.all_bullets =[]

        self.all_explosion = []
        self.explosion_images = []
        self.initialize_explosion_image()

        self.explosion_sound= pygame.mixer.Sound("audio/explosion.wav")


        self.all_ai=[]
        self.create_enimies()

        self.point = 0
        self.text = self.canvas.create_text(WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10, text="your grade: "+ str(self.point), fill="black",font= 50)
        # game over after hero die  8* *8frames
        self.last_time = 8*8
        self.has_display_points = False

        self.world_run = True

    def run(self):
        if self.hero.hp > 0:
            self.move()
            self.judge_hit()
            self.judge_collision()
            self.ai_command()
            self.display_explosion()
        elif self.last_time > 0:
            self.last_time -= 1
            self.display_explosion()
        elif not self.has_display_points:
            self.canvas.delete('all')
            self.has_display_points= True
            self.display_point()

    def  display_point(self):
        points_list = []
        image = Image.open("image/bg2.png")
        image = image.resize((WINDOW_WIDTH,WINDOW_HEIGHT),Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, image=self.bg)
        create_rectangle = False
        if os.path.isfile("data/points_rank.json"):
            file = open("data/points_rank.json",'r')
            points_list=json.load(file)
            points_list.append(self.point)
            points_list.sort(reverse=True)
            points_list = points_list[:10]
        else:
            for i in range(10):
                points_list.append(0)
            points_list[0] = self.point
        file = open("data/points_rank.json",'w')
        json.dump(points_list,file)
        file.close()

        for i, point in enumerate( points_list):
            self.canvas.create_text(WINDOW_WIDTH  / 2, 50+ 50* i,text =str(i+1) + "th is " +str(point),font = 50)
            if point == self.point and create_rectangle == False :
                self.canvas.create_rectangle(WINDOW_WIDTH /2 - 50,50 + 50*i +8,WINDOW_WIDTH /2 + 50,50 + 50*i - 8,outline = "red")
                self.canvas.create_text(WINDOW_WIDTH /2  - 150,50 + 50* i,text = "this is your grade",font = 50)
                create_rectangle = True


    def ai_command(self):
        for ai in self.all_ai:
            if ai.fighter.hp > 0:
                ai.control()

    def create_enimies(self):
        for i in range(5):
            enemy = Fighter(100+100 * i,400,hp = 10,canvas = self.canvas)
            self.all_fighters.append(enemy)
            self.all_ai.append(Ai(enemy,self))



    def key_callback(self,event):
        if self.hero.hp > 0:
            key_down = event.char

            if key_down == 's':
                self.hero.direction = "backward"
            if key_down == 'w':
                self.hero.direction = "forward"
            if key_down == 'a' :
                self.hero.direction = "left"
            if key_down == 'd' :
                self.hero.direction = "right"
            if key_down == 'j':
                self.all_bullets.append(self.hero.fire())
            if key_down == 'f':
                if self.world_run == True:
                    self.world_run = False

                elif self.world_run == False:
                    self.world_run = True



    def initialize_explosion_image(self):
        image= Image.open("image/explosion.png")
        for i in range(8):
            for j in range(8):
                small_image = image.crop((j*128,i*128,j*128+128,i*128+128))
                self.explosion_images.append(ImageTk.PhotoImage(image = small_image))



    def display_explosion(self):

        for explosion in self.all_explosion:
            if explosion.time == 0:
                self.explosion_sound.play()
                explosion.image = self.canvas.create_image(explosion.x, WINDOW_HEIGHT-explosion.y, image=self.explosion_images[explosion.time])

            else:
                self.canvas.delete(explosion.image)
                if explosion.time == explosion.max_time:
                    self.all_explosion.remove(explosion)
                    break
                explosion.image=self.canvas.create_image(explosion.x, WINDOW_HEIGHT-explosion.y, image=self.explosion_images[explosion.time])

            explosion.time +=1






    def judge_hit(self):
        for i,fighter in enumerate(self.all_fighters):
            for j, bullet in enumerate(self.all_bullets):
                if fighter.x - 1/2 * fighter.width < bullet.x and \
                   fighter.x + 1/2 * fighter.width > bullet.x and \
                   fighter.y - 1 / 2 * fighter.height < bullet.y and \
                   fighter.y + 1 / 2 * fighter.height > bullet.y:
                    fighter.hp -= bullet.damage
                    del  self.all_bullets[j]
                    self.canvas.delete(bullet.image)

                    if fighter.hp <= 0:
                        if bullet.owner == self.hero:
                            self.point += 100
                            self.canvas.delete(self.text)
                            self.text=self.canvas.create_text(WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10, text=str(self.point),
                                                fill="black")
                        del self.all_fighters[i]
                        self.all_explosion.append(Explosion(fighter.x,fighter.y))
                        self.canvas.delete(fighter.image)

    def judge_collision(self):
        delete_set = set([])
        for fighter1 in self.all_fighters :

            for fighter2 in self.all_fighters:


                if fighter1 != fighter2:
                    if abs(fighter1.x - fighter2.x ) < fighter1.width /2+ fighter2.width /2 and abs(fighter1.y - fighter2.y) < fighter1.height/2 + fighter2.height/2:
                        fighter1.hp = 0
                        fighter2.hp = 0
                        self.all_explosion.append(Explosion(fighter1.x, fighter1.y))
                        self.all_explosion.append(Explosion(fighter2.x, fighter2.y))
                        delete_set.add(fighter1)
                        self.canvas.delete(fighter1.image)
                        delete_set.add(fighter2)


                        self.canvas.delete(fighter2.image)
        for fighter in delete_set:
            self.all_fighters.remove(fighter)








    def move(self):
        for fighter in self.all_fighters:
            if fighter.direction == "forward" and fighter.y < WINDOW_HEIGHT - fighter.height / 2:
                self.canvas.move(fighter.image,0,-fighter.speed)
                fighter.y += fighter.speed


            if fighter.direction == "backward" and fighter.y > fighter.height /2:

                self.canvas.move(fighter.image,0,fighter.speed)   #  NOTE：（Δx，Δ）
                fighter.y -= fighter.speed


            if fighter.direction == "left" and fighter.x >fighter.width /2:
                self.canvas.move(fighter.image,-fighter.speed,0)
                fighter.x -= fighter.speed

            if fighter.direction == "right" and fighter.x < WINDOW_WIDTH - fighter.width / 2:
                self.canvas.move(fighter.image,fighter.speed,0)
                fighter.x += fighter.speed
            fighter.direction = "stop"

        for index, bullet in enumerate( self.all_bullets):
            if bullet.direction == "forward":
                bullet.y += bullet.speed
                self.canvas.move(bullet.image,0,- bullet.speed)
            if bullet.direction == "backward":
                bullet.y -= bullet.speed
                self.canvas.move(bullet.image,0, bullet.speed)
            if bullet.y <0 or bullet.y > WINDOW_HEIGHT:
                del self.all_bullets[index]







class Fighter:
    def __init__(self,x,y,canvas,hp,is_hero = False, speed = 5):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.canvas = canvas
        self.is_hero = is_hero
        image = Image.open("image/Fighter forward.png")
        if not is_hero:
            image = image.rotate(180)




        self.imageTk = ImageTk.PhotoImage(image=image)
        self.image=canvas.create_image(x,WINDOW_HEIGHT-y,image = self.imageTk)
        self.direction = "stop"
        self.width = 50
        self.height = 70
        self.fire_sound = pygame.mixer.Sound("audio/shot.wav")




    def fire(self):
        self.fire_sound.play()
        if self.is_hero == True:
            return Bullet(self.x,self.y + 35, canvas = self.canvas,direction = "forward",owner = self)

        if self.is_hero == False:
            return Bullet(self.x, self.y - 35, canvas = self.canvas, direction= "backward",owner = self)


class Bullet:
    def __init__(self,x,y,canvas,direction,owner,speed = 10,damage = 5,color = "black" ):
        self.x = x
        self.y = y
        self.radius = 6
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.owner = owner
        self.image = canvas.create_oval(x - 1/2 * self.radius, WINDOW_HEIGHT-(y+1/2 * self.radius),x + 1/2 * self.radius,WINDOW_HEIGHT - (y-1/2*self.radius),fill = color)


class Ai:
    def __init__(self,fighter,world):
        self.fighter = fighter
        self.world = world
        self.last_direction = "stop"


    def control(self):

        random_number = random.random()


        if random_number < 0.5:
            self.fighter.direction = self.last_direction
        elif random_number < 0.6:
            self.fighter.direction = "forward"
        elif random_number< 0.7:
            self.fighter.direction = "backward"
        elif random_number < 0.8:
            self.fighter.direction = "left"
        elif random_number < 0.9:
            self.fighter.direction = "right"
        elif random_number < 0.93:
            self.world.all_bullets.append(self.fighter.fire())

        for bullet in self.world.all_bullets:
            if( bullet.direction == "forward" and bullet.y < self.fighter.y )or \
                    ( bullet.direction == "backward" and bullet.y> self.fighter.y):
                if 0 <= bullet.x - self.fighter.x <= self.fighter.width / 2:
                    self.fighter.direction = "left"
                elif - self.fighter.width / 2 < bullet.x - self.fighter.x < 0:
                    self.fighter.direction = "right"

        self.last_direction = self.fighter.direction

        for fighter in self.world.all_fighters:
            if self.fighter != fighter:
                if 0<fighter.x - self.fighter.x < fighter.width / 2 + self.fighter.width /2 + self.fighter.speed + fighter.speed and abs(fighter.y - self.fighter.y) < fighter.height /2 + self.fighter.height /2 + self.fighter.speed:
                    self.fighter.direction = "left"
                if 0<self.fighter.x - fighter.x < fighter.width / 2 + self.fighter.width /2 + self.fighter.speed + fighter.speed and abs(fighter.y - self.fighter.y) < fighter.height /2 + self.fighter.height /2 + self.fighter.speed:
                    self.fighter.direction= "right"
                if 0<fighter.y - self.fighter.y < fighter.height / 2 + self.fighter.height /2 + self.fighter.speed + fighter.speed and abs(fighter.x - self.fighter.x) < fighter.width /2 + self.fighter.width /2 + self.fighter.speed:
                    self.fighter.direction = "backward"
                if 0<self.fighter.y - fighter.y < fighter.height / 2 + self.fighter.height /2 + self.fighter.speed + fighter.speed and abs(fighter.x - self.fighter.x) < fighter.width /2 + self.fighter.width /2 + self.fighter.speed:
                    self.fighter.direction = "forward"


class Explosion:
   def __init__(self,x,y):
       self.image = None  # this image is the image ID on the canvas
       self.x = x
       self.y = y
       self.time = 0
       self.max_time = 8 * 8 -1




game = GameFrame()