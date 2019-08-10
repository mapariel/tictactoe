#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:18:12 2019

@author: martin
"""
import numpy as np
import morpionML as mpl


class Combinatoire:
# makes the list (as numpy arrays) of the elements of ensemble^n
# ensemble is a numpy array  
   @staticmethod 
   def cartesian_product(n,ensemble):
       if n==1:
           n=ensemble.size
           liste = np.reshape(ensemble,(n,1))
           return liste
       else:
           liste=np.zeros(shape=(0,n),dtype=int)
           
           sous_liste = Combinatoire.cartesian_product(n-1,ensemble)
           for i in iter(ensemble):
               for j in range(0,sous_liste[:,0].size):
                   element=sous_liste[j,]
                   element = np.append(i,element)
                   liste = np.vstack((element,liste))
           return liste  
   # given a numpyarray, returns a tuple with it's components    
   @staticmethod     
   def tuple(array):
        t=()
        for i in array:
           t+=(i,) 
        return t    
         

     # build a frame around the board (as a string), n is the width (and height) of each cell
def frame(board_s,n=1,spaces=" "):
         lines = str.splitlines(board_s)
         result = ""
         for line in lines:
             chunks = [ line[i:i+1] for i in range(0, len(line), 1) ]
             result += spaces+(spaces*2).join(chunks)+spaces+'\n'    
         
         if n>0: # there is a frame
             lines = str.splitlines(result)
             result=''
             n2 = n*(1+len(spaces)*2) 
    
             for line in lines:
                 chunks = [ line[i:i+n2] for i in range(0, len(line), n2) ]
                 result += '|'+'|'.join(chunks)+'|\n'
             lines = str.splitlines(result)
             width = len(lines[0])       
             linesep = '-'*width+"\n"       
             result = ""
             for i in range(len(lines)):
                 if i % n == 0:
                     result += linesep
                 result += lines[i]+"\n"           
             result += linesep 
         return result



class Cell:   
    def __init__(self,mark,coordinates):
        self.mark = mark   # O or X 
        self.coordinates = coordinates  # numpy array 
    
    def __repr__(self):
        return str(self.mark)
            

"""
Class morpion represents a game of Tic Tac Toe
There is no logic of player (human or AI)
Only the possibility to play a random cell of the board

"""
class Morpion:
    
     def __init__(self,dim,side):
         self.dim = dim   # the dimension should be 2,3 or 4
         self.side = side  # the side of the hypercube (4 is reasonnable to play)
         
         # create the tuple for the shape
         s=()
         for i in range(0,dim):
            s+=(side,)

         self.board = np.empty(dtype=object,shape=s)  # the game board, players  X or O
         self.starter=np.random.randint(0,2)   # 1 the cross starts 0 the O starts
         self.moves = np.zeros(dtype=int,shape=(0,dim))  # the moves made on this game
         self.is_game_over=False
         self.initialize_board()


     """
     # return a string representation of the game
     # each line is one move. For instance :
     1 2\n0 0\2 3
     """
     def output_moves(self):
         result = ""
         for i in range(self.moves.shape[0]):
             row = self.moves[i,:]
             row = [str(i) for i in row.tolist()]
             result += " ".join(row)+"\n"
         return result    
     
     # load the moves in this game. Replaces the existing moves 
     def input_moves(self,input_string):
         lines = input_string.splitlines()
         for line in lines:
             self.playS(line)

     # fill the  boards with empty cells
     def initialize_board(self):
            ensemble = np.arange(self.side)
            self.moves = np.zeros(dtype=int,shape=(0,self.dim)) # make sure there is no moves
            self.is_game_over=False  # the game is not over
            liste = Combinatoire.cartesian_product(self.dim,ensemble)
            for cell in liste:
                t= Combinatoire.tuple(cell) 
                self.board[t]=Cell('_',cell)    



        
     # simplement en 2D pour le moment
     def board_as_string(self,display_info=True):
         board_s=""
         if self.dim ==2 :     
            for i in range(self.side):
                row = self.board[i,:]  # gets the i-th row
                liste = row.tolist()
                liste = [i.mark for i in liste]
                board_s += "".join(liste)+"\n"
         elif self.dim ==4 :
             for i in range(self.side): 
                row=()
                for j in range(self.side):
                    m2d = Morpion(side=self.side,dim=2)
                    m2d.starter=self.starter
                    m2d.board = self.board[i,j,:,:] 
                    temp = str.splitlines(m2d.board_as_string(False))
                    temp = np.array(temp)
                    temp.shape = (temp.shape[0],1)
                    row += (temp,)
                row = np.hstack(row)
                for k in range(row.shape[0]):
                    board_s+=((''.join([''.join(x) for x in row[k]])))+"\n"
 
         if display_info:
             if self.dim==4 : board_s = frame(board_s,n=4,spaces=" ")
             else :  board_s = frame(board_s,n=1,spaces=" ")
             board_s =  board_s.replace("_"," ")
             board_s =  board_s.replace(".","_")
             if self.is_game_over:
                 if self.who_is_winner()=="":
                     board_s +="Game over ! \nThere is no winner."
                 else : board_s +="Game over ! \n"+self.who_is_winner()+" is the winner."
             else : board_s +="next player  : "+self.who_is_playing()         
         return board_s  
#            
               
                
                
    

            
                
            


     def who_is_starting(self):
         if  self.starter==0:
             return "O"
         else:
             return "X" 



     # who is playing (the two players alternate)   
     def who_is_playing(self):
         if self.moves[:,1].size%2 == self.starter:
             return "O"
         else:
             return "X" 

#      """
#      Cancels the previous move
#      """
     def cancel_previous_move(self):
         move = self.moves[-1,:]
         t= Combinatoire.tuple(move) 
         self.board[t]=Cell('_',move)
         self.is_game_over = False
         self.moves = self.moves[0:-1,:] # remove the last move
         return move

     # pick a random free cell for the next play 
     def play_random(self):
        cells = self.get_marks()
        empty_cells = self.board[cells=='_']
        if empty_cells.size>0:
            n = np.random.randint(0,high=empty_cells.size)
            cell = empty_cells[n].coordinates 
            self.play(cell)
            return True
        return False
  

     # the cell the next player is puting on the board
     # cell is a numpy array 
     def play(self,cell):  
         tcell = Combinatoire.tuple(cell)
         if self.is_game_over:             
             return False
         
         player = self.who_is_playing()
         if self.board[tcell].mark=='_':
             self.board[tcell].mark=player
             self.moves = np.vstack((self.moves,cell))
             # teste s'il reste des cases à jouer
             if self.board[self.get_marks()=='_'].size==0 :
                 self.is_game_over=True
             if self.winner_game() is not None:
                 self.is_game_over=True
             return True
         return False

     # the cell the next player is puting on the board, 
     # stringcell is a string like ("2 1")
     def playS(self,stringcell):
        liste = stringcell.split()
        liste = [int(i) for i in liste] 
        cell = np.array(liste)
        return self.play(cell)
		 
     
     


     # return an array with the marks
     def get_marks(self):   
         mark = lambda x: x.mark
         marks = np.vectorize(mark)
         return(marks(self.board))

     # two cells of the board are given
     # this tells if a winning line ("break through") can be drawn through those cells
     def __is_break_through(self,cellA,cellB):
             Delta = cellA-cellB
             value = 0
             reponse = True
             for i in np.nditer(Delta):
                 if i!=0:
                     if value==0:
                         value=i
                     if (i!=value) & (i!=-value):
                         reponse = False
             return reponse

        # are those three cells aligned ? 
     def __are_aligned(self,cellA,cellB,cellC):
            Delta1 = cellC-cellB
            Delta2 = cellB-cellA
            nul = np.zeros(dtype=int,shape=(0,self.dim))
            if np.array_equal(Delta1,nul): 
                return False
            if np.array_equal(Delta2,nul): 
                return False
            return(
            np.array_equal(Delta1* Delta2[Delta2!=0][0] 
            , Delta1[Delta1!=0][0]*Delta2)
            )
     
     # return the winning line (when they were played)
     def winner_game(self):
         size = self.moves[:,1].size-1
         if size<self.side : return None
         winner = np.zeros(shape=(self.side),dtype=int)
         winner[0] = size
         cellA = self.moves[winner[0]] 
         for winner[1] in range(winner[0]-2,0,-2):
                 cellB=self.moves[winner[1]]
                 if self.__is_break_through(cellA,cellB):
                     count = 2
                     for k in range (winner[1]-2,-1,-2):
                         cellC=self.moves[k]
                         if self.__are_aligned(cellA,cellB,cellC):
                             winner[count]=k
                             count+=1
                         if count==self.side: 
                             return winner
                         
     def who_is_winner(self):
         if self.is_game_over:
             if self.winner_game() is None:
                 return ""
             elif self.moves[:,1].size%2 == self.starter:
                 return "X"
             else:
                 return "O" 
             
                


if __name__ == '__main__':   
  

    from keras.models import load_model
#    
    model2 = load_model('model_keras.h5')
    model4 = load_model('four_dimension.h5')
    
    m = Morpion(2,3)
    
 
    
    
    while True :
        m.play_random()
        mpl.playAI(m,model2)
        if m.is_game_over : break
    print(m.board_as_string())


    

    
