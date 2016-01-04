'''
Created on 2016-1-4

@author: sun tianchen
'''
from connection import connection
import datetime

def pseudoCheckin(distance, threshold, limit = 6000000):#threshold -- seconds
    conn, cur = connection()
    sites = {}
    sql = """
          select timestamp, id, type, x, y
          from parkmovement1
          order by id, timestamp
          limit %s
          """
    cur.execute(sql,(limit,))
    fetchRes = cur.fetchall();
    idcount = 0
    threshold = datetime.timedelta(seconds = threshold)
    curid = ""
    curtime = 0
    curtype = ""
    curcoord = ""
    for item in fetchRes:
        t = item[0]
        id = item[1]
        type = item[2]
        coord = str(item[3]) + ',' + str(item[4])
        if id == curid:
            if curtype == "check-in":#last record is check-in
                curtype = type
                curid = id
                curtime = t
                curcoord = coord
            else:
                if type != "check-in":#duration between 2 movements
                    duration = t - curtime
                    if duration > threshold:
                        sites.setdefault(curcoord,0)
                        sites[curcoord] += 1
                curtype = type
                curid = id
                curtime = t
                curcoord = coord
        else:
            idcount += 1
            print idcount
            curid = id
            curtype = type
            curcoord = coord
    print len(sites)
    print sort_by_value(sites)
    print sites
    
def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    return [ (backitems[i][1],backitems[i][0]) for i in range(0,len(backitems))] 

def checkins():
    sites = []
    conn, cur = connection()
    cur.execute("select DISTINCT x, y from parkmovement1 where type = 'check-in' ORDER BY x")
    fetchRes = cur.fetchall();
    for item in fetchRes:
        coord = str(item[0]) + ',' + str(item[1])
        sites.append(coord)
    return sites

if __name__ == "__main__":
    #pseudoCheckin(0,600,6000000)
    scheckinDic = {'58,63': 1, '3,66': 304, '57,73': 200, '29,67': 1463, '23,66': 575, '26,59': 8, '76,22': 16, '21,35': 1, '92,81': 4, '34,68': 8, '59,89': 309, '76,61': 539, '73,20': 81, '21,33': 1156, '17,48': 1, '52,28': 578, '43,56': 5, '22,34': 1488, '42,37': 2, '17,43': 1, '28,66': 8, '47,79': 427, '17,47': 1513, '57,64': 1554, '69,67': 1520, '78,37': 6, '87,81': 2, '57,80': 1443, '43,59': 1, '58,72': 1, '48,87': 6, '43,78': 8, '81,77': 1, '23,54': 6, '64,30': 2, '87,48': 4, '16,49': 4, '43,75': 526, '87,68': 589, '54,50': 1, '68,57': 2, '42,60': 1465, '87,63': 3, '44,25': 1525, '87,67': 1, '84,78': 744, '17,67': 10, '86,69': 1, '22,27': 926, '32,33': 22, '35,15': 216, '6,43': 11, '76,73': 778, '82,80': 3, '46,29': 4, '85,86': 2, '19,39': 5, '92,77': 274, '42,20': 531, '69,72': 1420, '78,24': 1, '59,46': 227, '69,58': 1356, '55,50': 802, '79,25': 1209, '15,40': 634}
    sites = checkins()
    print sites
    for item in sites:
        if item in scheckinDic.keys():
            scheckinDic.pop(item)
    for item in scheckinDic.keys():
        if scheckinDic[item] < 80:
            scheckinDic.pop(item)
            
    print len(scheckinDic)
    print sort_by_value(scheckinDic)
    print scheckinDic
