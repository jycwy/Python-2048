import tkinter as tk
import time as time

plane_x = 0
plane_y = 0

def key_callback(event):
    key_down = event.char
    global plane_x
    global plane_y
    if key_down == 's' and plane_y < 100:
        plane_y += 1
        for image in plane_image:
            canvas.move(image,0,1)
    if key_down == 'w' and plane_y >0:
        plane_y -= 1
        for image in plane_image:
            canvas.move(image,0,-1)
    if key_down == 'a' and plane_x > 0:
        plane_x -= 1
        for image in plane_image:
            canvas.move(image,-1,0)
    if key_down == 'd' and plane_x < 120:
        plane_x += 1
        for image in plane_image:
            canvas.move(image,1,0)

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200)
canvas.bind('<Key>',key_callback)
canvas.focus_set()
canvas.pack()
plane_image=[]
plane_image.append(canvas.create_polygon(100, 0, 90, 20, 110, 20, fill ='blue'))
plane_image.append(canvas.create_rectangle(90, 20, 110, 100, fill='grey'))
plane_image.append(canvas.create_polygon(90, 40, 60, 100, 90, 100, fill='blue'))
plane_image.append(canvas.create_polygon(110, 40, 110, 100, 140, 100, fill='blue'))





while True:
    time.sleep(0.1)
    root.update()
    root.update_idletasks()