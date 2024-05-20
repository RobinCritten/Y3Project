# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:06:17 2024

@author: robcr
"""


#Function combination and combinationUintil sourced from https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/


import numpy as np
import math
from playsound import playsound
import random
  
def createGrid(m,n):
    #create grid of coordinates for mxm grid in n dimensions
    coords = [] #set of current coords
    d = 1 #dimension number coutner 

    #loop for each dimnesion
    for i in range(n):
        coords.append(0) #Each dimension also needs its own cooridnate axis
    
    lst = []
    lst = fillLst(coords, d, lst, m, n)
    
    #return grid,lst
    return lst

def fillLst(coords,d,lst,m,n):
    
    for i in range(m):
        coords[d-1] = i
        if d < n:
            fillLst(coords,d+1,lst,m,n)
        else:
            lst.append(tuple(coords))
              
    return lst
 
#will take current predecessor combination as input
#compare against another set of coords
#if true they are neighbours
def isMooreNeighbourhood(a,b):
    for i in range(len(a)):
        if not (abs(a[i]-b[i]) == 1 or abs(a[i]-b[i]) == 0):
            return False
    return True

#finds if a cell within the successor grid is quiescent or not at time T+1
def findSuccessor(pre,lstSuccessor,m):
    
    res = []
    
    for i in lstSuccessor:
        
        sigma = 0 #counter for how may non-quiescent neighbours a cell has
        quiescent = True #tracks if a cell is quiescent
            
        for j in pre:
            if j == i:
                quiescent = False
            elif isMooreNeighbourhood(i, j):
                sigma+=1
        
        if sigma == 3 and quiescent:
            res.append(i)
        elif (sigma == 2 or sigma == 3) and (not quiescent):
            res.append(i)
    
    return res

def findSuccessorGrid(lstPrecursor,m,n):
    
    lstSuccessor = [] #store list of non border cells
    border = False #Tracks if cell is a border cell
    
    for i in lstPrecursor: #iterate through all cells
        border = False
        for j in i: #itterate through all coordinates of cell
            if j == m+1 or j == 0:
                border = True
        
        if border == False: #append if not on border
            lstSuccessor.append(i)
    
    return lstSuccessor

def GenerateCoordsFirstHalf(lstPrecursor,i):
    pre = [0]*i #final list of coordinates
    lst = lstPrecursor.copy()
    
    for counter in range(i):
        r = random.randint(0,(len(lst)-1))
        pre[counter] = lst[r]
        del lst[r]
        
    return pre
        

def GenerateCoordsSecondHalf(lstPrecursor,i):
    lst  = lstPrecursor.copy()
    
    for counter in range((len(lstPrecursor)-i)):
        del lst[random.randint(0,(len(lst)-1))]
        
    return lst

def RandomSample(lstPrecursor,i,lstSuccessor,m,res,d):
    
    pre_density = i/len(lstPrecursor) #density of precursor config
    if pre_density > 0.5:
        x = 1 - pre_density
    else:
        x = pre_density

    #function for samlpes needed for precursor density    
    mult = 1 - (((15/136)*(x**2))+((2101/1360)*x))
    count = math.ceil(math.comb(((m+2)**d),i)*mult)
    
    for k in range(count):
        
        #Generate set of coordinates
        if i < int((len(lstPrecursor)+1)/2):
            pre = GenerateCoordsFirstHalf(lstPrecursor,i)
        else:
            pre = GenerateCoordsSecondHalf(lstPrecursor,i)
        
        #Turn Coordinates into results
        Successor = findSuccessor(pre,lstSuccessor,m) 
        index = int((len(Successor)/len(lstSuccessor)) / (1/len(lstSuccessor)))
        res[index,0] = res[index,0] + pre_density
        res[index,1] = res[index,1] + 1
        if pre_density < res[index,2]:
            res[index,2] = pre_density
        if pre_density > res[index,3]:
            res[index,3] = pre_density
    return res
    
if __name__ == "__main__":
    
    ########################################################
    m = 2 #size of grid
    n = 2 #number of dimensions
    sim = 100 #number of simulations
    #fileName = "2d2mRandomBinomial.csv"
    ########################################################
    
    resultSet = [] #store final results of each simulation
    for counter in range(sim):
        lstPrecursor = createGrid(m+2,n) #find grid for size m+2 by m+2
        lstSuccessor = findSuccessorGrid(lstPrecursor, m, n) #find coords for m by m 
        results = np.zeros(((len(lstSuccessor)+1),6))
        #results = [[summation,number,lowest,highest,mean],...]
        
        
        for l in results:
            l[2] = 1       
        for i in range(len(results)):
            results[i,2] = 1 
            results[i,5] = (1/len(lstSuccessor))*i
            
        
        #itterate through all possible combinations
        #counter = 0
        for i in range(len(lstPrecursor)+1):
            
            #reset res for each loop
            res = np.zeros(((len(lstSuccessor)+1),6))
            #results = [[summation,number,lowest,highest,mean],...]
            for l in res:
                l[2] = 1     
            for x in range(len(res)):
                res[x,2] = 1 
                res[x,5] = (1/len(lstSuccessor))*x
            
            
            #Randomly sample
            RandomSample(lstPrecursor,i,lstSuccessor,m,res,n)
        
            
            #write inidividual segment for each precursor density
            # f = open(fileName, 'a', newline ='')
            # writer = csv.writer(f)
            # for c in res:
            #     if c[1] !=0: #only calculate mean if there was a least one value of that successor density   
            #         c[4] = c[0]/c[1] #calculate mean
            #     writer.writerow(c)
            # writer.writerow("")
            # f.close()
            
            #append results to final total
            for y in range(len(res)):
                results[y,0] = results[y,0] + res[y,0]
                results[y,1] = results[y,1] + res[y,1]
                if res[y,2] < results[y,2]:
                    results[y,2] = res[y,2]
                if res[y,3] > results[y,3]:
                    results[y,3] = res[y,3]
            
        print("Simulation Number: {0}".format(counter))
        resultSet.append(results)
    
    # f = open(fileName,'a',newline = '')
    # writer = csv.writer(f)
    # for i in results:
    #     i[4] = i[0]/i[1] #calculate mean
    #     writer.writerow(i)
    # f.close()
    
    lowerBoundCorrect = 0
    upperBoundCorrect = 0
    CorrectLowerBounds = [0,0.1875,0.1875,0.25,0.1875] #2d2m
    CorrectUpperBounds = [1,0.6875,0.625,0.5,0.5] #2d2m
    #CorrectLowerBounds = [0,0.12,0.12,0.12,0.12,0.16,0.16,0.16,0.2,0.2] #2d3m
    #CorrectUpperBounds = [1,0.8,0.76,0.72,0.68,0.64,0.6,0.6,0.56,0.52] #2d3m
    for r in resultSet:
        for i in range(len(CorrectLowerBounds)):
            #print("Testing",r[i,2])
            #print("Testing2",CorrectLowerBounds[i])
            if r[i,2] == CorrectLowerBounds[i]:
                lowerBoundCorrect+=1
            if r[i,3] == CorrectUpperBounds[i]:
                upperBoundCorrect+=1
    print("Probability of Lower bounds being correct: {0}".format((lowerBoundCorrect/len(CorrectLowerBounds))/sim))
    print("Probability of Upper bounds being correct: {0}".format((upperBoundCorrect/len(CorrectUpperBounds))/sim))
    
    playsound("ding.wav") #know when done