# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:20:42 2024

@author: robcr
"""

from scipy.stats import binom
import math

#math.comb(len(lstPrecursor),i)
#binom.cdf(k=6,n=10,p=0.7) #n=samplesize, k=how may probability calculated for p=probability of success

def BinomialCDF(m,d,counter):
    
    while True:
        try:
            choose = float(input("Enter Probability for {0}d{1}m part {2}:\t"))
            print("Choose: {0}".format(choose))
            break
        except IndexError:
            print("Incorrect Input I")
        except ValueError:
            print("Incorrect Input")
                          
    for i in range(1,(math.comb((m+2)**d,counter)+1)):
        probability = 1 - binom.cdf(k=0,n=i,p=choose)
        if probability >= 0.95:
            return i
    print("Failure")
    return math.comb((m+2)**d,counter)

if __name__ == "__main__":
    
    ###############################
    m = 1
    d = 2
    ###############################
    results = []
    
    for counter in range(((m+2)**d) + 1):
        #find 0.95 probabilty for each bound
        results.append((counter/((m+2)**d),BinomialCDF(m,d,counter)))
        
    for r in results:
        print("Density: {0},\t Sample Size: {1}".format(r[0],r[1]))
        