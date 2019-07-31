#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 07:38:48 2019
a class to implement logistic regression
all the vectors inserted as parameters have dimension (n,) 
where n is the number of elements of the vector
@author: martin
"""

import numpy as np
import scipy.optimize as scop


class Logistic():
    
    def __init__(self,bias=True,lam=0,nb_labels=1):
        self.Theta = None
        self.bias = bias
        self.lam = lam
        self.nb_labels = nb_labels
    
    def __sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    """ 
    logistic regression
    """
    
    
    """
    #   calculates the cost of linked to a logistic regression
    #   parameters 
    #   y the labels equals 0 or 1
    # returns also the gradient of the cost  
    # theta is a 1 dimensional vector      
    """
    def cost(self,theta,X,y):
        cost = 0 
        m,n = X.shape
        theta2 = np.array(theta)
        theta2.shape=(n,1)
        theta = theta2
        y = y.copy()  
        y.shape=(m,1)
        h = self.__sigmoid(X.dot(theta))
        cost = (-(y.T).dot(np.log(h)) - ((1-y).T).dot(np.log(1-h)) )/m    
        return cost[0,0]
    
    def grad(self,theta,X,y):
        m,n = X.shape
        grad = np.zeros(shape=(n,1))
        theta2 = np.array(theta)
        theta2.shape=(n,1)
        theta = theta2
        y = y.copy()
        y.shape=(m,1)
        h = self.__sigmoid(X.dot(theta))
        grad = (X.T).dot(h-y)/m 
        grad.shape=(n,)
        return grad
    
    """
    # returns the label vector
    # 1 if y = i
    # 0 otherwise
    # y is a vector (numpy array of dim (m,0) )
    # i is an integer (0,1,..., until dim of the side-1)     
    """
    def get_label(self,y,i): 
        y = y.copy()
        y[y==i]=-1
        y[y>=0]=0
        y=y/(-1)
        return y      
    
    """
    # add the bias feature to the matrix of features
    """
    def add_bias(self,X):
        m = X.shape[0]
        X2 = np.copy(X)
        # add the bias
        uns = np.ones(shape=(m,1))
        X2 = np.hstack((uns,X))
        return X2
    
    
    """
    # implementation of logistic regression
    # param X : matrix of features, dim=(m,n)
    # param y : labels, dim=(m,)
    # parama lam:  regularization parameter
    # param nb_labels : number of lables (from 1 to nb_labels)
    
    # returns Theta : parameters of the regression, 
    # dim = (nb_labels,n)   
    """
    def fit(self,X,y):
        if self.bias:
            X = self.add_bias(X)
        
        n = X.shape[1]
        self.Theta = np.zeros(shape=(self.nb_labels,n))
        theta_0 = np.zeros(shape=(n,))
        for i in range(self.nb_labels):

    #        theta_row = np.array([])
    #        theta_i.shape=(0,n)
    #        
    ##        for j in range(side):
            y0 = self.get_label(y,i)
            mini = scop.minimize(self.cost,x0= theta_0 ,
                                 method="CG",args=(X,y0),jac=self.grad)
    #        mini = scop.minimize(cost,x0= theta_0 ,method="CG",args=(X,y0))
            
            self.Theta[i,:] = mini['x']
  
            
    
   
    
    def predict(self,x):
        if len(x.shape)==1:
            x = x.reshape(1,x.shape[0])
        if self.bias:  # add the bias
            x = self.add_bias(x)
            
        probas = self.__sigmoid(x.dot(self.Theta.T))
        return probas

    def evaluate(self,X,y,verbose=1):
        m = X.shape[0]
        probas = self.predict(X)
        pred = np.argmax(probas,axis=1)
        count = 0
        
        loss= self.loss(X,y)
        
        for k in range(m):
            if ((pred[k]==y[k,0])) : count+=1
        return loss,count/m  

    
    
    def save(self,name="model_reglin"):
        np.savetxt(name,self.Theta,delimiter=",")


    def load(self,name="model_reglin"):
        self.Theta = np.loadtxt(name,delimiter=",")
        
    def loss(self,X,y): 
        m = X.shape[0]
        loss = 0
        probas = self.predict(X)
        for i in range(m):
           loss = loss - np.log(probas[i,int(y[i])])
        return loss/m    

    
    
