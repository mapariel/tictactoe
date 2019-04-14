#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import classe as cl
import numpy as np

cell_width=50
cell_border=2
cell_sep = 20
frame = tk.Tk()





def play():
#    while(True):
        cell = np.random.randint(0,m.side,4)
        mark = m.who_is_playing()
        if m.play(cell):
                fill_cell(cell[0],cell[1],cell[2],cell[3],mark,"black")
    
        if m.game_over:
#                canvas.create_text(200,200,text="GAME OVER",font=('Courier',30),fill="red")
                A = m.winner_game()
                mark = m.who_is_winner()
                cellA = m.moves[A[0]]
                cellB = m.moves[A[1]]
                cellC = m.moves[A[2]]
                cellD = m.moves[A[3]]
                fill_cell(cellA[0],cellA[1],cellA[2],cellA[3],mark,"red")
                fill_cell(cellB[0],cellB[1],cellB[2],cellB[3],mark,"red")
                fill_cell(cellC[0],cellC[1],cellC[2],cellC[3],mark,"red")
                fill_cell(cellD[0],cellD[1],cellD[2],cellD[3],mark,"red")
                

def width():
    return cell_width*16+cell_sep*5+cell_border*12

def draw_sub_grid(i,j):
    x = i*(cell_width*4+cell_border*3)+(i+1)*cell_sep
    y = j*(cell_width*4+cell_border*3)+(j+1)*cell_sep
    canvas.create_rectangle(x,y,x+cell_width*4+cell_border*3,y+cell_width*4+cell_border*3)

def draw_cell_border(i,j,k,l):
    x = i*(cell_width*4+cell_border*3)+(i+1)*cell_sep+k*cell_width+(k-1)*cell_border
    y = j*(cell_width*4+cell_border*3)+(j+1)*cell_sep+l*cell_width+(l-1)*cell_border    
    canvas.create_rectangle(x,y,x+cell_width,y+cell_width,fill="white")


def fill_cell(i,j,k,l,mark,color):
    x = i*(cell_width*4+cell_border*3)+(i+1)*cell_sep+k*cell_width+(k-1)*cell_border
    y = j*(cell_width*4+cell_border*3)+(j+1)*cell_sep+l*cell_width+(l-1)*cell_border    
    if mark=="O":
        canvas.create_oval(x+4,y+4,x+cell_width-8,y+cell_width-8,width=4,outline=color)
    elif mark=="X":
        canvas.create_line(x+4,y+4,x+cell_width-8,y+cell_width-8,width=4,fill=color)
        canvas.create_line(x+cell_width-8,y+4,x+4,y+cell_width-8,width=4,fill=color)






canvas = tk.Canvas(frame,width=width(),height=width(),bg="blue")
btn = tk.Button(frame,text="Play",command=play)
btn.pack()


for i in range (0,4):
    for j in range(0,4):
        for k in range(0,4):
            for l in range(0,4):
                draw_cell_border(i,j,k,l)


canvas.pack()

m = cl.morpion(4)
