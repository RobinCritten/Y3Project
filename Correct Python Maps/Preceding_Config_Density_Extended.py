# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 13:20:13 2024

@author: robcr
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 18:48:16 2024

@author: robcr
"""


#Function combination and combinationUintil sourced from https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/


import numpy as np
import csv
import math
from playsound import playsound
  
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
    


# Program to print all combination 
# of size r in an array of size n
# The main function that prints 
# all combinations of size r in 
# arr[] of size n. This function 
# mainly uses combinationUtil()
def combination(arr, n, r, lstSuccessor,m,results):
     
    # A temporary array to 
    # store all combination
    # one by one
    pre = [0]*r
    pre_density = r/len(arr)
 
    # Print all combination 
    # using temporary array 'data[]'
    results = combinationUtil(arr, pre, 0, n - 1, 0, r, 
                    lstSuccessor,m,pre_density,results)
    
 
# arr[] ---> Input Array
# pre[] ---> Temporary array to
#         store current combination
# start & end ---> Starting and Ending
#             indexes in arr[]
# index ---> Current index in data[]
# r ---> Size of a combination 
# to be printed 
def combinationUtil(arr, pre, start,end, index, r, 
                    lstSuccessor,m,pre_density,results):
                             
    
    if (index == r):
        Successor = findSuccessor(pre,lstSuccessor,m)
        index = int((len(Successor)/len(lstSuccessor)) / (1/len(lstSuccessor)))
        results[index,0] = results[index,0] + pre_density
        results[index,1] = results[index,1] + 1
        if pre_density < results[index,2]:
            results[index,2] = pre_density
        if pre_density > results[index,3]:
            results[index,3] = pre_density
        #print(results[index,1])
        return results
 
    # replace index with all
    # possible elements. The
    # condition "end-i+1 >= 
    # r-index" makes sure that 
    # including one element at
    # index will make a combination 
    # with remaining elements at 
    # remaining positions
    i = start; 
    while(i <= end and end - i + 1 >= r - index):
        pre[index] = arr[i]
        combinationUtil(arr, pre, i + 1, end, index + 1, r,
                        lstSuccessor,m,pre_density,results)
        i += 1
 
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

    
if __name__ == "__main__":
    
    ########################################################
    m = 2 #size of grid
    n = 2 #number of dimensions
    fileName = "2d2m_newNeighbour_Precursor_density_map_Extended.csv"
    ########################################################
    
    lstPrecursor = createGrid(m+2,n) #find grid for size m+2 by m+2
    lstSuccessor = findSuccessorGrid(lstPrecursor, m, n) #find coords for m by m 
    results = np.zeros(((len(lstSuccessor)+1),6))
    #results = [[summation,number,lowest,highest,mean],...]
    
    
    for l in results:
        l[2] = 1       
    for i in range(len(results)):
        results[i,2] = 1 
        results[i,5] = (1/len(lstSuccessor))*i
            
    
    f = open(fileName, 'w', newline ='')

    writer = csv.writer(f)
    writer.writerow(("Precursor Density Summation","Precursor Count",
                     "Lowest Density","Highest Density","Mean","Successor Density"))
    writer.writerow("")
    
    f.close()
    
    #itterate through all possible combinations
    counter = 0
    for i in range(len(lstPrecursor)+1):
        
        #reset res for each loop
        res = np.zeros(((len(lstSuccessor)+1),6))
        #results = [[summation,number,lowest,highest,mean],...]
        for l in res:
            l[2] = 1     
        for x in range(len(res)):
            res[x,2] = 1 
            res[x,5] = (1/len(lstSuccessor))*x
        
        #only run if less than 500000000 combinations to check
        if math.comb(len(lstPrecursor),i) < 500000000:
            r = i
            combination(lstPrecursor,len(lstPrecursor),r,lstSuccessor,m,res)
    
        
        #write inidividual segment for each precursor density
        f = open(fileName, 'a', newline ='')
        writer = csv.writer(f)
        for c in res:
            if c[1] !=0: #only calculate mean if there was a least one value of that successor density   
                c[4] = c[0]/c[1] #calculate mean
            writer.writerow(c)
        writer.writerow("")
        f.close()
        
        #append results to final total
        for y in range(len(res)):
            results[y,0] = results[y,0] + res[y,0]
            results[y,1] = results[y,1] + res[y,1]
            if res[y,2] < results[y,2]:
                results[y,2] = res[y,2]
            if res[y,3] > results[y,3]:
                results[y,3] = res[y,3]
        
        print("Current Precursor length: ",i)
    
    f = open(fileName,'a',newline = '')
    writer = csv.writer(f)
    for i in results:
        i[4] = i[0]/i[1] #calculate mean
        writer.writerow(i)
    f.close()
    
    playsound("ding.wav") #know when done
                