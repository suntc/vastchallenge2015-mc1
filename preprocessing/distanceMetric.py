'''
Created on 2016-1-4

@author: sun
'''

import numpy as np
import pickle
import sys
from leven import levenshtein

### parkmovement1 has 3557 ids
### 4 run cases: (0,800),(800,1600),(1600,2400),(2400,3557)

def getEditDistance(strA,strB):
    lenA=len(strA)
    lenB=len(strB)
    c=np.zeros((lenA+1,lenB+1))
    for i in range(lenA+1):
        c[i][0]=i
    for i in range(lenB+1):
        c[0][i]=i
    for j in range(1,lenB+1):#outer is column
        for i in range(1,lenA+1):#inner is row
            ii=i-1
            jj=j-1
            if(strA[ii]==strB[jj]):
                c[i][j]=c[i-1][j-1]
            else:
                c[i][j]=min(c[i-1][j],c[i][j-1],c[i-1][j-1])+1
    return c[lenA][lenB]

def distanceMetric(start,end):
    input = open("actionList.pkl","rb")
    actions = pickle.load(input)
    actionStrings = []
    for item in actions:
        actionstring = ""
        for i in item:
            if i == -1:
                i = 255
            actionstring += chr(i)
        actionStrings.append(actionstring)
        
    if end > len(actions):
        end = len(actions)
    distanceMextric = []
    for i in range(start,end):
        print "process: " , i
        dist = []
        for j in range(0,len(actionStrings)):
            distance = levenshtein(actionStrings[i], actionStrings[j])
            #print distance
            dist.append(distance)
        distanceMextric.append(dist)
    output = open("distMetric" + str(start) + ".pkl","wb")
    pickle.dump(distanceMextric,output)
    output.close()
    
if __name__ == "__main__":
    #start = int(sys.argv[1])
    #end = int(sys.argv[2])
    distanceMetric(0, 3557)