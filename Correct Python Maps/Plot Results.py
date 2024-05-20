# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:12:09 2024

@author: robcr
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
import math
    
#(m+2)^d + 1 precursor densities
#m^d + 1 successor densities
# +1 for blank lines
#2 initial lines

def DensityComparison(m,d,fileName,FigureTitle):

    with open(fileName,'r', newline ='') as data:

        reader = csv.reader(data, delimiter=' ')
        
        currentLine = 1
        BlockCounter = 1
        #PrecursorTotal = (m+2)**d + 1 #upper limit for precursor
        #SuccessorTotal = m**d + 1 #upper limit for successor
        Begin = 2 + (((m+2)**d + 1)*(m**d + 2)) #where cumulative results begin
        LowerDensity = np.zeros(m**d + 1)
        UpperDensity = np.zeros(m**d + 1)
        Mean = np.zeros(m**d + 1)
        SuccessorDensity = np.zeros(m**d + 1)
        for row in reader:
            if currentLine > Begin:
                r = row[0].split(",")
                LowerDensity[BlockCounter-1] = float(r[2])
                UpperDensity[BlockCounter-1] = float(r[3])
                Mean[BlockCounter-1] = float(r[4])
                SuccessorDensity[BlockCounter-1] = float(r[5])
                BlockCounter+=1

            currentLine+=1  
    data.close()

    plt.title(FigureTitle)
    plt.xlabel("Successor Density")
    plt.ylabel("Precursor Density")
    plt.plot(SuccessorDensity,Mean,label = "Mean")
    plt.scatter(SuccessorDensity,Mean)
    plt.plot(SuccessorDensity,UpperDensity,label = "Upper Bound",color='red')
    plt.scatter(SuccessorDensity,UpperDensity,color='red')
    plt.plot(SuccessorDensity,LowerDensity,label = "Lower Bound",color='red',linestyle='dashed')
    plt.scatter(SuccessorDensity,LowerDensity,color='red')
    plt.grid()
    plt.legend()
    plt.fill_between(SuccessorDensity,LowerDensity,UpperDensity,color='green',alpha=0.2)
    plt.show()
    
def DensityDistibution(m,d,fileName,FigureTitle):
    
    plt.title(FigureTitle)
    plt.xlabel("Successor Density")
    plt.ylabel("Precursor Count")
    
    with open(fileName,'r', newline ='') as data:

        reader = csv.reader(data, delimiter=' ')
        
        currentLine = 1
        BlockCounter = 1
        PreCounter = 0
        #PrecursorTotal = (m+2)**d + 1 #upper limit for precursor
        #SuccessorTotal = m**d + 1 #upper limit for successor
        Count = np.zeros(m**d + 1)
        dDensity = 1 / ((m+2)**d + 1)
        cDensity = 0
        SuccessorDensity = np.zeros(m**d + 1)
        for row in reader:
            if currentLine > 2 and BlockCounter <= (m**d + 1):
                r = row[0].split(",")
                Count[BlockCounter-1] = float(r[1])
                SuccessorDensity[BlockCounter-1] = float(r[5])
                BlockCounter+=1
            elif BlockCounter > (m**d + 1):
                #l = "d = " + str(PreCounter / ((m+2)**d))
                plt.plot(SuccessorDensity,Count,color = 'g',alpha = cDensity)
                #plt.scatter(SuccessorDensity,Count)
                BlockCounter = 1
                PreCounter+= 1
                cDensity+= dDensity

            currentLine+=1  
        
        plt.grid()
        plt.yscale("log")
        #plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.show()
    data.close()
    
def BinomialDistributionComparison(m,d,FigureTitle):
    density = np.zeros(((m+2)**d + 1))
    sampleMaximum = np.zeros(((m+2)**d + 1))
    for i in range(((m+2)**d + 1)):
        density[i] = i/((m+2)**d)
        sampleMaximum[i] = math.comb((m+2)**d,i)
        
    
    #2d3m minimum sample sizes
    #sampleMinimum = [1,1,1,1147,9473,26526,5766,3635,3252,3449,4743,9564,32727,229098,
     #               267063,489615,23538,32400,20000,2762,315,1,1,1,1,1]
    
    #2d2m minimum sample sizes
    sampleMinimum = [1,1,1,418,70,39,57,213,2141,34,374,57,1,1,1,1,1]
    
    function = []
    for i in range(((m+2)**d + 1)):
        if density[i] > 0.5:
            x = 1 - density[i]
        else: 
            x = density[i]
        mult = 1 - (((15/136)*(x**2))+((2101/1360)*x))
        function.append(math.ceil(math.comb((m+2)**d,i)*mult))
    
    plt.title(FigureTitle)
    plt.xlabel("Precursor Density")
    plt.ylabel("Number of Samples")
    plt.plot(density,sampleMinimum,label = "Minimum Sample Size for 95% accuracy")
    plt.scatter(density,sampleMinimum)
    plt.plot(density,sampleMaximum,label = "Maximum Possible Sample Size")
    plt.scatter(density,sampleMaximum)
    plt.plot(density,function,label = "Sample Estimation function")
    plt.scatter(density,function)
    plt.grid()
    #plt.yscale("log")
    plt.legend()
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    plt.show()
    

if __name__ == "__main__":
    #####################################
    m=3
    d=2
    fileName="2d3mRandomBinomial.csv"
    FigureTitle = "2d3mRandomBinomial"
    #####################################
    
    DensityComparison(m,d,fileName,FigureTitle)
    #DensityDistibution(m,d,fileName,FigureTitle)
    #BinomialDistributionComparison(m, d, FigureTitle)
    
