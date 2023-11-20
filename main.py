from sklearn.cluster import KMeans
import numpy as np
import random
from disp import display
from datetime import datetime
from popc import popc

def createDataSet(numClust, numFeat, numSamples, caseNum):
        ret = []
        feat_belongs = {}
        if caseNum == 1:
                for i in range(numFeat):
                        feat_belongs[i] = random.randrange(numClust)
                for i in range(numSamples):
                        clust_num = random.randrange(numClust)
                        feats = [0 for j in range(numFeat)]
                        for j in range(numFeat):
                                if feat_belongs[j] == clust_num:
                                        if random.random() < 0.8:
                                                feats[j] = 1
                        ret.append(feats)
        if caseNum == 2:
                for i in range(numFeat):
                        if i < 0.9 * numFeat:
                                feat_belongs[i] = random.randrange(numClust)
                        else:
                                feat_belongs[i] = -1
                for i in range(numSamples):
                        clust_num = random.randrange(numClust)
                        feats = [0 for j in range(numFeat)]
                        for j in range(numFeat):
                                if feat_belongs[j] == clust_num:
                                        if random.random() < 0.8:
                                                feats[j] = 1
                                if feat_belongs[j] == -1:
                                        if random.random() < 0.2:
                                                feats[j] = 1
                        ret.append(feats)
        if caseNum == 3:
                for i in range(numClust):
                        probs = []
                        for k in range(numFeat):
                                if k < numClust:
                                        if k == i:
                                                probs.append(1.0)
                                        else:
                                                probs.append(0.0)
                                else:
                                        probs.append(0.5)


                        for j in range(numSamples):
                                feats = [0 for j in range(numFeat)]
                                for k in range(numFeat):
                                        if random.random() < probs[k]:
                                                feats[k] = 1
                                ret.append(feats)

        return np.array(ret)

random.seed()
for ex in range(3):
        if ex == 0:
                X = createDataSet(7, 100, 200, 1)
        if ex == 1:
                X = createDataSet(7, 100, 200, 2)
        if ex == 2:
                X = createDataSet(7, 20, 30, 3)

        kmeans = KMeans(n_clusters=7, random_state=0).fit(X)
        result = []
        for i in range(len(X)):
                result.append([kmeans.labels_[i], X[i]])
        display(result, 'kmeans example {}'.format(ex + 1))
        print('kmeans number of clusters [it was requested]: ', 7)

        labels = popc(X)
        result = []
        for i in range(len(X)):
                result.append([labels[i], X[i]])
        display(result, 'popc example {}'.format(ex + 1))
        print('popc number of clusters: ', len(dict.fromkeys(labels, True)))
