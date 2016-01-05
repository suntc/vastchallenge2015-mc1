'''
Created on 2016-1-5

@author: sun
'''

import pickle

class GridVector():
    def __init__(self,id,count):
        self.siteid = id
        self.grids = []
        for i in range(0,count):
            self.grids.append(Grid())
        
class Grid():
    def __init__(self):
        self.ids = []
        self.count = 0
    def add(self,id):
        self.ids.append(id)
        self.count += 1
        

def indexConvert(intv,gridlen,i):
    return i / (gridlen/intv) ### i / 6 -- 0~191/6 = 0~31

def siteVector(gcount):### gcount = 32 -- 32 grids each
    GridVectors = {} ###dict, id: GridVector(siteid, grids)
    siteVector = {} ### id: [[count,ids],[count,ids],...]
    ### init site vector
    sitenum = 84
    for i in range(1,sitenum + 1):
        GridVectors.setdefault(i,GridVector(i,gcount))
    ### load action vector
    input = open("actionVec.pkl","rb")
    actionVec = pickle.load(input)
    input.close()
    for key in actionVec:
        action = actionVec[key]
        for i, item in enumerate(action):
            index = indexConvert(300, 1800, i)
            if item == -1 or item == 0: ### null or movement
                continue
            else:
                GridVectors[item].grids[index].add(key)
    for key in GridVectors:
        grids = GridVectors[key].grids
        siteVector.setdefault(key,[])
        for g in grids:
            siteVector[key].append([g.count,g.ids])
    output = open("siteVector.pkl","wb")
    pickle.dump(siteVector,output)
    output.close()
              
if __name__ == "__main__":
    siteVector(32)