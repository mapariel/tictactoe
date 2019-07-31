#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 09:20:31 2019
@author: martin
"""
import morpion as mp
import numpy as np
import scipy.optimize as scop

# deep learning attempt

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Activation,Dense

import logistic as lg


"""
Calculates the features  for the last position of this game
if the game is:
+-----------+
| X | X | _ |
+-----------+
| O | O | _ |
+-----------+
| _ | _ | _ |
+-----------+

Feature for the last move, if the player is X, will be :
x = 1 1 1 0 -1 -1 0 0 0 0    # the first one is the bias
and if the player is O :
x = 1 -1 -1 0 1 1 0 0 0 0     
"""
def get_features(morpion,player='O'):
    player = morpion.who_is_playing()
    other_player='X'
    if player=='X' : other_player = 'O'
    table = np.zeros(shape = morpion.get_marks().shape)
    table[morpion.get_marks()==player]=1
    table[morpion.get_marks()==other_player]=-1
    x = table.flatten()
    n = x.shape[0] 
    x.shape=(1,n)
    return x    
    

"""
When a game is finished, this will extract  features and label out of this game :
the state of the board before the last move as features 
and the move of the winner as y
"""
def get_features_label(morpion):
    if not morpion.is_game_over: return None
    winner = morpion.who_is_winner()  
    if winner =="" : return None   
    
    dim = morpion.dim
    side = morpion.side
    
    dims = (side,)
    for i in range(dim-1):
        dims = dims+(side,)    
# this takes into account only the last winning move
    move = morpion.cancel_previous_move()  # get the last move
    y = np.ravel_multi_index(move,dims)
    x = get_features(morpion,player=winner)
    return x,y   
        
"""
param y : the labels, dim=(m,1)
returns Y : dim=(m,nb_labels)
"""
def transform_labels(y,nb_labels):
    m = y.shape[0]
    Y = np.zeros(shape=(m,nb_labels))
    for i in range(m):
        Y[i,int(y[i])]=1
    return Y    



# simulates games with given side and dimension
# returns the features X and the labels y  
# n is the dimension of the training set  
# according to the model 1    
def simulation(m=10,side=3,dim=2):
    n = side**dim 
    X = np.zeros(shape=(0,n))
    y = np.zeros(shape=(0,1))
    # play until it gets m features 
    while(True):
        mo = mp.Morpion(dim,side)
        mo.initialize_board()
        while(True):
            mo.play_random()
            if mo.is_game_over: break
        if not mo.who_is_winner()=="":
            [X_1,y_1] = get_features_label(mo)
            X = np.vstack((X,X_1))
            y = np.vstack((y,y_1))
        if X.shape[0]>m : break
    # returns exactly m features    
    return X[:m,:],y[:m]  



"""
# knowing a game, predicts the next move
# 
"""
def playAI(morpion,model):
    move = ""
    if morpion.is_game_over: 
        return None
    player = morpion.who_is_playing()
    x = get_features(morpion,player)
    probas = model.predict(x)  
    side = morpion.side
    dim = morpion.dim
    dims = (side,)
    for i in range (dim-1):
        dims +=(side,)  
    while True:
        y_hat = np.argmax(probas)
        move = np.unravel_index(y_hat,shape=dims)
        data = tuple(str(x) for x in move)
        moveS = " ".join(data)
        is_valid = morpion.playS(moveS)
        if is_valid:
            break
        else:
            probas[0,y_hat]=0
    return move









        

if __name__ == '__main__': 

    m=2000
    side=3
    dim=2
    nb_labels = side**dim
    # learn
#    
    print("simulation...")
    
    X,y=simulation(m,side=side,dim=dim)
    np.savetxt("X_train",X,delimiter=",")
    np.savetxt("y_train",y,delimiter=",")

#    
#    print("validation...")
    m_val=int(m*0.2)

    X_val,y_val = simulation(m=m_val,side=side,dim=dim)
#    np.savetxt("X_val",X_val,delimiter=",")
#    np.savetxt("y_val",y_val,delimiter=",")
#
#
#
#    scores = model.evaluate(X_val, y_val, verbose=1)
#    print("Accuracy (validation): %.2f%%" % (scores[1]*100))
#    print("loss (validation): ",round(scores[0],3))
    


  

#    model.fit(X, Y, epochs=150, batch_size=10) 
#    model.save('model_keras.h5') 

    model = load_model('model_keras.h5') 


    """       
    


    """
   
#    
#        ##   deep learning model
#    model = Sequential()
#    model.add(Dense(9, input_dim=9, activation='relu'))
#    model.add(Dense(9, activation='relu'))
#    model.add(Dense(9, activation='relu'))        
#    model.add(Dense(9, activation='sigmoid'))
#    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#    
#
    m = X.shape[0]
    Y =transform_labels(y,nb_labels=nb_labels)
    Y_val =transform_labels(y_val,nb_labels=nb_labels)  

    scores = model.evaluate(X, Y, verbose=1)
    print("Accuracy (training): %.2f%%" % (scores[1]*100))
    scores = model.evaluate(X_val, Y_val, verbose=1)
    print("Accuracy (validation): %.2f%%" % (scores[1]*100))
    



#  
#    
    nombre_parties=1000
    playerX="AI"   #  random or AI 
    playerO="random"
    countX = 0  # games won by X
    countO = 0  # games won by O
    
    morp = mp.Morpion(dim=dim,side=side)   
    morp.starter =1
    

    
    
    for games in range(nombre_parties):
#        morp.starter = 1  # the cross starts
        morp.initialize_board()
        morp.starter = 1  # the cross starts

        while True:
            player = morp.who_is_playing()
            if player == "X":
                if playerX == "random" : morp.play_random()
                elif playerX == "AI" :  playAI(morp,model)
            else :
                if playerO == "random" : morp.play_random()
                elif playerO == "AI" :   playAI(morp,model)
            if morp.is_game_over: break
        if (morp.who_is_winner()=="X") : countX+=1
        if (morp.who_is_winner()=="O") : countO+=1
#        print(morp.board_as_string())
    #    https://stackoverflow.com/questions/19843752/structure-of-inputs-to-scipy-minimize-function
    
    
    print(morp.who_is_starting()," starts")
    
    print(nombre_parties," games.")
    print("X is ",playerX," and won ",round(countX/nombre_parties*100,2)," %")
    print("O is ",playerO," and won ",round(countO/nombre_parties*100,2)," %")
    draws = nombre_parties-countX-countO 
    print("games ended in a draw ",round(draws/nombre_parties*100,2)," %")
