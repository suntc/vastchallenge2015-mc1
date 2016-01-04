'''
Created on 2016-1-4

@author: sun tianchen
'''

import datetime
import pickle
from connection import connection
from statics import pcheckinDic, translate

class SliceVector(object):
    def __init__(self,snum):
        self.slices = []
        for i in range(0,snum):
            self.slices.append(Slice())
        self.startIndex = 0
        self.endIndex = 0
        self.actionVector = []
    def add(self,s):
        self.slices.append(s)
    def slicesProcess(self):
        for s in self.slices:
            s.process()
    def calcActionVec(self):
        prevState = -1
        for i, s in enumerate(self.slices):
            if i < self.startIndex or i > self.endIndex:
                self.actionVector.append(-1)
            else:
                if s.state == -1:#null state
                    self.actionVector.append(prevState)
                else:
                    self.actionVector.append(s.state)
                    prevState = s.state
                    
class Slice(object):
    def __init__(self):
        self.info = []
        self.state = 0 ###normal movement state
        self.track = []
    def add(self,tup):
        self.info.append(tup)###(t,type,x,y)
    def process(self):
        if len(self.info) == 0:###no movement
            self.state = -1
            return
        for item in self.info:
            type = item[1]
            coord = str(item[2]) + ',' + str(item[3])
            self.track.append([item[2],item[3]])
            if type == "check-in":
                self.state = translate[coord][0]###site id
                return
            else:###movement
                if coord in pcheckinDic.keys():
                    self.state = translate[coord][0]
                    return

def getIndex(intv,t):
    intv = datetime.timedelta(seconds = intv)
    duration = datetime.datetime(2000,1,2,0,0,0) - datetime.datetime(2000,1,1,8,0,0)
    passtime = datetime.datetime(2000,1,1,t.hour,t.minute,t.second) - datetime.datetime(2000,1,1,8,0,0)
    return passtime.seconds / intv.seconds

def slices(intv):
    conn, cur = connection()
    sql = """
          select timestamp, id, type, x, y
          from parkmovement1
          order by id, timestamp
          """
    #cur.execute(sql,(5000,))
    cur.execute(sql)
    fetchRes = cur.fetchall();
    ###calculate slice num
    interval = datetime.timedelta(seconds = intv)
    duration = datetime.datetime(2000,1,2,0,0,0) - datetime.datetime(2000,1,1,8,0,0)
    snum = duration.seconds / interval.seconds
    ###prepare loop
    idcount = 0
    actions = {}
    curid = ""
    for item in fetchRes:
        t = item[0]
        id = item[1]
        type = item[2]
        x = int(item[3])
        y = int(item[4])
        if id == curid:###process the same person
            index = getIndex(intv, t)
            actions[id].slices[index].add((t,type,x,y))
            actions[id].endIndex = index
        else:###new person
            curid = id
            idcount += 1
            print "slices: ",idcount
            actions.setdefault(id,SliceVector(snum))###create slicevector
            index = getIndex(intv, t)
            actions[id].startIndex = index
            actions[id].endIndex = index
            actions[id].slices[index].add((t,type,x,y))
    return actions

def actionVector():
    actionVec = {}
    actions = slices(300)#5 minutes as interval
    for key in actions:
        sv = actions[key]
        sv.slicesProcess()
        sv.calcActionVec()
        actionVec.setdefault(key,sv.actionVector)
    print len(actionVec)
    output = open("actionVec.pkl","wb")
    pickle.dump(actionVec, output)
    output.close()
    
if __name__ == "__main__":
    #actions = slices(300)
    actionVector()
    #input = open("actionVec.pkl","rb")
    #actionVec = pickle.load(input)
    #print actionVec
    #print getIndex(300,datetime.datetime(2000,1,1,8,6,2))