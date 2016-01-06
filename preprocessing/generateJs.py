'''
Created on 2016-1-5

@author: sun tianchen
'''

import statics
import pickle

def gridData():
    input = open("siteVector.pkl","rb")
    siteVector = pickle.load(input) ### id: [[count,ids],[count,ids],...]
    input.close()

    gridData = []
    siteInfo = statics.siteInfo ###dict, id: []
    gridSequence = statics.gridSequence ### [1,2,3...]
    for id in gridSequence:
        infoDic = {"id": 0,"type":0,"name":"hi","vector":[]}
        g = {"count":0,"ids":[]} ### vector[]'s member
        type = siteInfo[id][0]
        name = siteInfo[id][1]
        infoDic["id"] = id
        infoDic["type"] = type
        infoDic["name"] = name
        grids = siteVector[id]
        for item in grids:
            g = {"count":len(list(set(item[1]))),"ids":list(set(item[1])),"id":id} ### vector[]'s member
            infoDic["vector"].append(g)
        gridData.append(infoDic)
    output = open("../data/gridData.js","wb")
    print >> output, "var gridData = "
    print >> output, gridData
    output.close()

if __name__ == "__main__":
    gridData()