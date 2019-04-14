import tkinter as tk
import morpion as mp
import numpy as np


type1="human"
type2="human"


class Player:
    def __init__(self,morpionGUI,type):
        self.morpionGUI = morpionGUI
        self.type=type  # numan or CPU
    def play(self):
        bool =False
        if self.type=="CPU":
            bool = self.morpionGUI.morpion.play_random()
            morpionGUI.active_cel = None
        elif self.type=="human":
            if morpionGUI.active_cell is not None:
                bool = self.morpionGUI.morpion.play(morpionGUI.active_cell)  
        
        self.morpionGUI.draw_board()
        return bool      # return True only if the move is valid

        



class MorpionGUI:

    cell_width=40
    cell_border=3
    cell_sep = 10
    dim = 2
    side = 3

    def __init__(self, parent):
        self.morpion=mp.Morpion(self.dim,self.side)       
        self.active_cell = None   # the cell clicked by the player
        self.number_of_players= 0
        self.player1 = Player(self,type1)
        self.player2 = Player(self,type2)
        
        
        self.frame = tk.Frame(parent)
        self.frame.pack()
        
        self.buttonPanel=tk.Frame(self.frame)      
        self.buttonPanel.pack()        
        
        
        self.button1 = tk.Button(self.buttonPanel, text="resume", background="red",command=self.resume)
        self.button1.pack(side=tk.LEFT)
        

        self.button2 = tk.Button(self.buttonPanel, text="dimension", background="red",command=self.change_dimension)
        self.button2.pack(side=tk.LEFT)
        self.button2.pack()

        self.button3 = tk.Button(self.buttonPanel, text="side", background="red",command=self.change_side)
        self.button3.pack(side=tk.LEFT)
        
        
        self.button4 = tk.Button(self.buttonPanel, text="players", background="red",command=self.change_players)
        self.button4.pack(side=tk.LEFT)

        
        self.label = tk.Label(self.buttonPanel,text=self.number_of_players)
        self.label.pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(self.frame,width=self.width(),height=self.height(),bg="blue")
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.pack(side=tk.TOP)
        self.initialize()
        self.change_players()
          


    def width(self):
        dim1 = self.cell_width
        dim2 = self.cell_border
        dim3 = self.cell_sep
        side = self.morpion.side
        if (self.morpion.dim==2) | (self.morpion.dim==3):
            return (dim1+dim2)*side-dim2+2*dim3
        elif self.morpion.dim==4:
            return dim3*(side+2)+((dim1+dim2)*side-dim2)*side-dim3
  
    def height(self):
        dim1 = self.cell_width
        dim2 = self.cell_border
        dim3 = self.cell_sep
        side = self.morpion.side
        if (self.morpion.dim==2) | (self.morpion.dim==4):
            return self.width()
        elif self.morpion.dim==3:
            return dim3*(side+2)+((dim1+dim2)*side-dim2)*side -dim3   

        
    def initialize(self):
        ensemble = np.arange(0,self.morpion.side)
        liste = mp.Combinatoire.cartesian_product(self.morpion.dim,ensemble)
        for coord in liste:
            self.draw_cell_border(coord)

    # return, as a tuple, the top lef corner of a cell
    def get_top_left_corner(self,coord):
        dim1 = self.cell_width
        dim2 = self.cell_border
        dim3 = self.cell_sep
        i=coord[0];j=coord[1]
        side= self.morpion.side 
        x=dim3+j*(dim1+dim2)
        y=dim3+i*(dim1+dim2)
        if (self.morpion.dim==3) | (self.morpion.dim==4)  :
            k=coord[2]
            y+=k*(side*(dim1+dim2)-dim2+dim3)
        if self.morpion.dim==4:
            l=coord[3]
            x+=l*(side*(dim1+dim2)-dim2+dim3)            
        return (x,y)        
        
    def draw_cell_border(self,coord):
        t = self.get_top_left_corner(coord)
        dim1 = self.cell_width
        x = t[0]
        y= t[1]
        self.canvas.create_rectangle(x,y,x+dim1,y+dim1,fill="white")


    def fill_cell(self,cell,color):
        tcell = mp.Combinatoire.tuple(cell)
        mark = self.morpion.board[tcell].mark
        dim1 = self.cell_width
        t = self.get_top_left_corner(cell)
        x = t[0]
        y = t[1]
        if mark=="O":
            self.canvas.create_oval(x+4,y+4,x+dim1 -8,y+dim1 -8,width=4,outline=color)
        elif mark=="X":
            self.canvas.create_line(x+4,y+4,x+dim1-8,y+dim1 -8,width=4,fill=color)
            self.canvas.create_line(x+dim1 -8,y+4,x+4,y+dim1 -8,width=4,fill=color)

    def draw_board(self):
        for cell in self.morpion.moves:
            self.fill_cell(cell,"black")
        if self.morpion.game_over:
            if self.morpion.winner_game() is not None:
                cells = self.morpion.winner_game()
                for i in cells:
                   cell = self.morpion.moves[i]
                   self.fill_cell(cell,color="red")
        else:
            if self.morpion.moves.size>2:
                cell = self.morpion.moves[-1]
                self.fill_cell(cell,color="red")



    def change_players(self):
        self.number_of_players= (self.number_of_players+1)%3
        if self.number_of_players== 0:
            self.player1 = Player(self,"CPU")
            self.player2 = Player(self,"CPU")
        elif self.number_of_players== 1:
            self.player1 = Player(self,"human")
            self.player2 = Player(self,"CPU")
        elif self.number_of_players== 2:
            self.player1 = Player(self,"human")
            self.player2 = Player(self,"human")
        self.label.configure(text=str(self.number_of_players))
        self.canvas.delete("all")
        self.morpion = mp.Morpion(self.dim,self.side)
        self.canvas.config(width=self.width(),height=self.height())
        self.canvas.pack()
        self.initialize()


    def change_side(self):
        self. canvas.delete("all")
        self.side=((self.side-1) % 3)+2
        print(self.side)
        self.morpion = mp.Morpion(self.dim,self.side)
        self.canvas.config(width=self.width(),height=self.height())
        self.canvas.pack()
        self.initialize()


    def change_dimension(self):
        self.dim=((self.dim-1) % 3)+2
        self.morpion = mp.Morpion(self.dim,self.side)
        self.canvas.config(width=self.width(),height=self.height())
        self.canvas.pack()
        self.initialize()


    def resume(self):
        self.morpion = mp.Morpion(self.dim,self.side)
        self.initialize()
        self.active_cell = None
        self.draw_board()    

     
#                     
    def callback(self,event):
       ensemble = np.arange(self.morpion.side)
       liste = mp.Combinatoire.cartesian_product(self.morpion.dim,ensemble)
       for cell in liste:
           t = self.get_top_left_corner(cell)
           if (t[0]<=event.x) & (event.x < t[0]+self.cell_width) & (t[1]<=event.y) & (event.y < t[1]+self.cell_width):
               self.active_cell=cell


         
if __name__ == '__main__':
    
    root = tk.Tk()
    morpionGUI = MorpionGUI(root)


    
    switch = 1
    
    while True:
       if switch == 1:
           if morpionGUI.player1.play():
               switch =2
       else:
           if morpionGUI.player2.play():
               switch = 1
       root.update()
       root.update_idletasks()
   