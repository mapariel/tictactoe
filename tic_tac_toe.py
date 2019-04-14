# -*- coding: utf-8 -*-
#  This file was a very first attempt....
# it is not used....



import numpy as np



size = 5  # this is the size of the grid (a cube in four dimensions)

plateau = np.arange(1,size**4+1)
plateau.shape = (size,size,size,size)
vector = np.array([0,0,0,0])






# fait les liste de tous les eĺéments de set^n
# set est un array qui contient les éléments
def cartesian_product(n,ensemble):
   if n==1:
       n=ensemble.size
       liste = np.reshape(ensemble,(n,1))
       return liste
   else:
       liste=np.zeros(shape=(0,n),dtype=int)
       
       sous_liste = cartesian_product(n-1,ensemble)
       for i in iter(ensemble):
           for j in range(0,sous_liste[:,0].size):
               element=sous_liste[j,]
               element = np.append(element,i)
               liste = np.vstack((element,liste))
       return liste    
       

# a direction (vector) is given
# this calculates all the possible cells form where 
# a winning line can be drawn in the direction of the vector
# 
def starting_cell(vector):
    n = vector.size
    move = np.array([0,0,0,0])
    zeros = vector == 0
    n_zeros = vector[zeros].size
    liste=np.zeros(shape=(0,n),dtype=int)
    # when the composant is the 0, there is a freedom to start on the face
#    liste=np.zeros(shape=(0,n),dtype=int)
    move[vector==1] = 0
    move[vector==-1] = size
    ensemble = np.arange(0,size+1)
    if n_zeros>=1 :
        sous_liste = cartesian_product(n_zeros,ensemble)
        for j in range(0,sous_liste[:,0].size):
            element=sous_liste[j,]
            move[zeros] = element
            liste = np.vstack((move,liste))
    else :
         liste = np.vstack((move,liste))
    return liste
      

#
#  given an array [a,b,c,d]  with at least one 1 and 0 for the rest
#  complete it by keeping the one at the same place and replacing the zeros by -1 or 0 
#  the results are all the directions a line can be drawn in the hyper cube 
# for instance if vector is [1,0,0,0] the exit can be  [1,0,-1,-1]       
def compute_directions(vector):
    ensemble = np.array([0,-1])
    bools = vector==0
    n = vector.size
    n_zeros = vector[bools].size
    liste=np.zeros(shape=(0,n),dtype=int)
    
    sous_liste = cartesian_product(n_zeros,ensemble)    
    for i in range(0,sous_liste[:,0].size):
        vector[bools]=sous_liste[i,]
        liste = np.vstack((vector,liste))
#        print(vector)
#        winning_moves(vector)
    return liste    



def display_lines():
    vector=np.array([0,0,0,0])
    for n in range(1,4):
        if n==1:
            for i in range (0,4):
                vector[i]=1
                compute_directions(vector)
                vector=np.array([0,0,0,0])
        elif n==2:
            for i in range (0,4):
                for j in range(i+1,4):
                    vector[i]=1
                    vector[j]=1
                    compute_directions(vector)
                    vector=np.array([0,0,0,0])
        elif n==3:
            for i in range (0,size):
                for j in range(i+1,4):
                    for k in range(j+1,4):
                        vector[i]=1
                        vector[j]=1
                        vector[k]=1
                        compute_directions(vector)                   
                        vector=np.array([0,0,0,0])


def test():
    print("Test 1")
    vector=np.array([1,0,0,0])
    liste = compute_directions(vector)
    
    n = liste[:,0].size
    
    for i in range(0,n):
        print(liste[i,])
        print("-------------")
        print(starting_cell(liste[i,]))
        print("=================")





test()

#display_lines()


        

  


####  FIRST VESRION TO FORGET....      
   
#for n in range(4):
#    i=n % 4
#    j=(n+1) % 4
#    k=(n+2) % 4
#    l=(n+3) % 4
#    
#    print("####### AXE "+str(n)+"   ######")
#    
#    for var[i] in range(0,size):
#        for var[j] in range(0,size):
#                for var[k] in range(0,size):
#                    for var[l] in range(0,size):
#                        print(plateau[var[0],var[1],var[2],var[3]])
#                    count+=1
#                    print("----- #"+str(count)+"-----")
#
#
#
## the lines where two coordinates change
#
#index = np.arange(4)
#
#for i in range(0,3):
#    for j in range (i+1,4):
#        index = np.arange(4)
#        index[index == i]=-1
#        index[index == j]=-1
#        k=index[index!=-1][0]
#        l=index[index!=-1][1]            
#                    
#        print("####### AXE "+str(k)+"-"+str(l)+"   ######")
#        for var[i] in range(0,size):
#            for var[j] in range(0,size):
#                    for var[k] in range(0,size):
#                        var[l]=var[k]
#                        print(plateau[var[0],var[1],var[2],var[3]])
#                    count+=1
#                    print("----- #"+str(count)+"-----")                   
#                    for var[k] in range(0,size):
#                        var[l]=size-1-var[k]
#                        print(plateau[var[0],var[1],var[2],var[3]])
#                    count+=1
#                    print("----- #"+str(count)+"-----")                   
#                    
#        
# # the lines where three coordinates change
#
#index = np.arange(4)
#
#for i in range(0,4):
#    index = np.arange(4)
#    index[index == i]=-1
#    j=index[index!=-1][0]
#    k=index[index!=-1][1]
#    l=index[index!=-1][2]            
#    
#            
#    print("####### AXE "+str(j)+"-"+str(k)+"-"+str(l)+"   ######")
#    for var[i] in range(0,size):
#        for var[j] in range(0,size):
#                for var[k] in range(0,size):
#                    var[l]=var[k]
#                    print(plateau[var[0],var[1],var[2],var[3]])
#                count+=1
#                print("----- #"+str(count)+"-----")                   
#                for var[k] in range(0,size):
#                    var[l]=size-1-var[k]
#                    print(plateau[var[0],var[1],var[2],var[3]])
#                count+=1
#                print("----- #"+str(count)+"-----")                   
#                   
#
#
#
