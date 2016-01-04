'''
Created on 2016-1-4

@author: sun tianchen
'''

import pickle
import numpy as np
from sklearn.cluster import DBSCAN


def cluster():
    input = open("distMetric0.pkl","rb")
    distMetric = pickle.load(input)
    input.close()
    
    ids = []
    db = DBSCAN(eps=50,metric='precomputed',min_samples=2).fit(np.array(distMetric))
    y = db.labels_
    print len(y)
    n_clusters_ = len(set(y)) - (1 if -1 in y else 0)
    print n_clusters_
    print db.core_sample_indices_
    output = open("dbscanGroup.pkl","wb")
    pickle.dump(y,output)
    output.close()

    
if __name__ == "__main__":
    #cluster()
    
    input = open("dbscanGroup.pkl","rb")
    y = pickle.load(input)
    input.close()
    l = {}
    for item in y:
        l.setdefault(item,0)
        l[item] += 1
    print l
    print len(l)
    