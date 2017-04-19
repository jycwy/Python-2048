import tkinter as tk
import time as time
import random
import json
import os

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

class GameFrame:
    def __init__(self):
        self.root = tk.Tk()
        self.field = GameField(self.root)
        while True:
            time.sleep(0.02)
            self.root.update()
            self.root.update_idletasks()

            self.field.display_board(self.field.board)





class GameField:
    def __init__(self,root):
        self.gameover = False
        self.canvas = tk.Canvas(root,width = WINDOW_WIDTH,height = WINDOW_HEIGHT,bg = "white")
        self.score = 0
        self.best = 0
        self.direction = 'stop'
        self.canvas.bind('<Key>',self.key_callback)
        self.canvas.focus_set()
        self.canvas.pack()
        self.text = self.canvas.create_text(200, 100,text="Score: " + str(self.score) + "   " + "Highest: " + str(self.best),font=100)

        self.board = [[0] * 4,[0]*4,[0]*4,[0]*4]
        self.reset()

        points_list = []
        self.all_animations = []
        self.picture_list = [[[None, None]] * 4, [[None, None]] * 4, [[None, None]] * 4, [[None, None]] * 4]


        if os.path.isfile("data/2048_points_rank.json"):
            file = open("data/2048_points_rank.json", 'r')
            points_list = json.load(file)
            points_list.append(self.score)
            points_list.sort(reverse=True)
            self.best = points_list[0]

        else:
            self.best = 0





    def display_board(self,board):
        self.score = 0

        for i in range(4):
            for j in range(4):
                self.score += board[i][j]
        self.canvas.delete(self.text)
        self.text = self.canvas.create_text(200, 100,text="Score: " + str(self.score) + "   " + "Highest: " + str(self.best),font=100)


        if self.gameover == False:
            for i in range(4):
                for j in range(4):

                    if board[i][j] != 0:
                        color = None

                        if board[i][j] == 2:
                            color = "#ffe4c4"
                        elif board[i][j] == 4:
                            color = "#eee9e9"

                        elif board[i][j] == 8:
                            color = "#eedfcc"

                        elif board[i][j] == 16:
                            color = "#fff8dc"

                        elif board[i][j] == 32:
                            color = "#f0fff0"

                        elif board[i][j] == 64:
                            color = "#e6e6fa"

                        elif board[i][j] == 128:
                            color = "#fff0f5"

                        elif board[i][j] == 256:
                            color = "#ffe4e1"

                        elif board[i][j] == 512:
                            color ="#e0ffff"

                        elif board[i][j] == 1024:
                            color = "#ffc0cb"

                        elif board[i][j] == 2048:
                            color = "#d8bfd8"
                        for animation in self.all_animations:
                            speed = 5
                            delta_x = 0
                            delta_y = 0
                            original_x =i
                            original_y = j

                            if animation.direction == "down" and animation.x == i and animation.y == j and abs(delta_y)< animation.distance :
                                original_x= i
                                original_y = j - animation.distance/100
                                delta_y = animation.moved
                                animation.moved += speed
                            if animation.direction == "forward" and animation.x == i and animation.y == j and abs(delta_y)< animation.distance :
                                original_x = i
                                original_y = j+ animation.distance / 100
                                delta_y = -animation.moved
                                animation.moved += speed
                            if animation.direction == "left" and animation.x == i and animation.y == j and abs(delta_x)< animation.distance :
                                original_x= i+ animation.distance/100
                                original_y=j

                                delta_x = -animation.moved
                                animation.moved += speed
                            if animation.direction == "right" and animation.x == i and animation.y == j and abs(delta_x)< animation.distance :
                                original_x = i - animation.distance / 100
                                original_y = j
                                delta_x = animation.moved
                                animation.moved += speed
                            self.picture_list[i][j][1] = self.canvas.create_rectangle(100 * original_x + delta_x,
                                                                                          WINDOW_HEIGHT - 100 * original_y + delta_y,
                                                                                          100 * original_x + 100 + delta_x,
                                                                                          WINDOW_HEIGHT - 100 * original_y - 100 + delta_y,
                                                                                          fill=color)
                            self.picture_list[i][j][0] = self.canvas.create_text(100 * original_x + 50 + delta_x,
                                                                                     WINDOW_HEIGHT - 100 * original_y - 50 + delta_y,
                                                                                     text=str(self.board[i][j]),
                                                                                     font=100)
                    else:
                        self.canvas.create_rectangle(100 * i, WINDOW_HEIGHT - 100 * j, 100 * i + 100,WINDOW_HEIGHT - 100 * j - 100, fill="white")
        if self.gameover == True:

            self.canvas.create_rectangle(0,200,400,600,fill = "white")




    def points(self):
        if self.gameover == True:
            points_list = []
            if os.path.isfile("data/2048_points_rank.json"):
                file = open("data/2048_points_rank.json", 'r')
                points_list = json.load(file)
                points_list.append(self.score)
                points_list.sort(reverse=True)
                file = open("data/2048_points_rank.json", 'w')
                json.dump(points_list, file)
                file.close()


            else:
                points_list.append(self.score)
                file = open("data/2048_points_rank.json",'w')
                json.dump(points_list,file)
                file.close()
            self.best = points_list[0]

    def key_callback(self,event):
        key_down = event.char
        if key_down == 'w':
            self.direction = 'up'
            self.move()


        if key_down == 's':
            self.direction = 'down'
            self.move()


        if key_down == 'a':
            self.direction = 'left'
            self.move()


        if key_down == 'd':
            self.direction = 'right'
            self.move()



    def spawn(self):
        num = 0

        if self.if_gameover() == False:

            while num == 0:
                random_number = random.random()
                x = random.choice([0, 1, 2, 3])
                y = random.choice([0, 1, 2, 3])


                if random_number < 0.7 and self.board[x][y] == 0:
                    self.board[x][y]=2
                    num += 1
                elif random_number < 1.0 and self.board[x][y] == 0:
                    self.board[x][y]=4
                    num += 1


    def if_gameover(self):
        print("gameover")
        gameover = False
        full = True
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    full = False
                    break
        if full == True:
            movable = False
            for i in [1,2]:
                for j in [1,2]:
                    if self.board[i][j] == self.board[i+1][j] or self.board[i][j] == self.board[i-1][j] or self.board[i][j] == self.board[i][j+1] or self.board[i][j] == self.board[i][j -1]:
                        movable = True
            for i in [0,3]:
                for j in [1,2]:
                    if self.board[i][j] == self.board[i][j+1] or self.board[i][j] == self.board[i][j-1]:
                        movable = True
            for i in [1,2]:
                for j in [0,3]:
                    if self.board[i][j] == self.board[i+1][j] or self.board[i][j] == self.board[i-1][j]:
                        movable = True

            if movable == False:
                print("over")
                self.canvas.delete("all")
                gameover = True
                self.gameover = gameover
                self.points()
                
        return gameover

    def reset(self):
        if self.score > self.best:
            self.best = self.score
        self.score = 0
        self.spawn()
        self.spawn()




    def move(self):
        is_moved = False
        self.if_gameover()
        if self.direction == 'down':
            for i in range(4):
                for j in range(4):
                    for k in range(j):
                        x = i
                        original_y = j
                        y = j - k
                        if self.board[x][y] == 0:
                            break
                        elif self.board[x][y-1] == 0 :
                            num = self.board[x][y]
                            self.board[x][y] = 0
                            self.board[x][y -1] = num
                            is_moved = True
                            continue
                        elif self.board[x][y] == self.board[x][y-1]:
                            self.board[x][y-1] +=  self.board[x][y]
                            self.board[x][y] = 0
                            is_moved = True
                            self.all_animations.append(Animation(x,y,self.direction,k))
                            break
                        else:
                            self.all_animations.append(Animation(x,y,self.direction,k))
                            break
            if is_moved == True:
                self.spawn()


        if self.direction == 'up':
            is_moved = False
            for i in range(4):
                for j in range(4):
                    for k in range(j):
                        x= i
                        original_y = 3-j
                        y= 3-j+k
                        if self.board[x][y]== 0 :
                            break
                        elif self.board[x][y+1] == 0:
                            num = self.board[x][y]
                            self.board[x][y]= 0
                            self.board[x][y+1] = num
                            is_moved = True
                            continue
                        elif self.board[x][y] == self.board[x][y+1]:
                            self.board[x][y+1] += self.board[x][y]
                            self.board[x][y] = 0
                            is_moved = True
                            self.all_animations.append(Animation(x,y,self.direction,k))
                            break
                        else:
                            self.all_animations.append(Animation(x, y, self.direction, k))
                            break
            if is_moved == True:
                self.spawn()


        if self.direction == 'left':
            is_moved = False
            for i in range(4):
                for j in range(4):
                    for k in range(j):
                        original_x = j
                        x= j- k
                        y= i
                        if self.board[x][y] == 0:
                            break
                        if self.board[x-1][y] == 0:
                            num = self.board[x][y]
                            self.board[x][y] = 0
                            self.board[x-1][y] = num
                            is_moved = True
                            continue
                        elif self.board[x][y]== self.board[x-1][y]:
                            self.board[x-1][y] += self.board[x][y]
                            self.board[x][y] = 0
                            is_moved = True
                            self.all_animations.append(Animation(x, y, self.direction, k))
                            break
                        else:
                            self.all_animations.append(Animation(x, y, self.direction, k))
                            break
            if is_moved == True:
                self.spawn()

        if self.direction == 'right':
            is_moved = False
            for i in range(4):
                for j in range(4):
                    for k in range(j):
                        original_x = 3-j
                        x = 3-j+k
                        y = i
                        if self.board[x][y] == 0:
                            break
                        if self.board[x+1][y] == 0:
                            num = self.board[x][y]
                            self.board[x][y] = 0
                            self.board[x+1][y] = num
                            is_moved = True
                            continue
                        elif self.board[x][y] == self.board[x+1][y]:
                            self.board[x+1][y] += self.board[x][y]
                            self.board[x][y] = 0
                            is_moved = True
                            self.all_animations.append(Animation(x, y, self.direction, k))
                            break
                        else:
                            self.all_animations.append(Animation(x, y, self.direction, k))
                            break
            if is_moved == True:
                self.spawn()

class Animation:
    def __init__(self,x,y,direction,distance):
        self.x = x
        self.y = y
        self.direction = direction
        self.distance = (distance+1 )* 100
        self.moved = 0



game = GameFrame()