import tkinter as tk
import time as time

def key_callback(event):
    print(event.char)

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
    for image in plane_image:
        canvas.move(image,1,1)
    root.update()
    root.update_idletasks()