from sklearn.cluster import KMeans
import numpy as np

def deltaIfRemoved(row, counts, countsAll, numClusters, multiplier, power):
        ret = 0.0

        for i in range(len(row)):
                if row[i] == 1:
                        ret -= pow((counts[i] * multiplier + 1.0) / (countsAll[i] * multiplier + numClusters + 0.0), power)
                        ret += pow(((counts[i] - 1.0) * multiplier + 1.0) / (countsAll[i] * multiplier + numClusters + 0.0), power)

        return ret

def deltaIfAdded(row, counts, countsAll, numClusters, multiplier, power):
        ret = 0.0

        for i in range(len(row)):
                if row[i] == 1:
                        ret += pow(((counts[i] + 1.0) * multiplier + 1.0) / (countsAll[i] * multiplier + numClusters + 0.0), power)
                        ret -= pow((counts[i] * multiplier + 1.0) / (countsAll[i] * multiplier + numClusters + 0.0), power)

        return ret

def popc(samples, multiplier = 1000.0, power = 10.0):
        kmeans = KMeans(n_clusters=int(len(samples)/2), random_state=0).fit(samples)

        labels = kmeans.labels_

        clusters = []
        clusters_counts = []
        counts_all = [0 for i in range(len(samples[0]))]
        for i in range(max(labels) + 1):
                clusters.append([])
                clusters_counts.append([0 for j in range(len(samples[0]))])

        for i in range(len(samples)):
                cs = samples[i]
                cl = labels[i]
                clusters[cl].append(i)

                for j in range(len(cs)):
                        if cs[j] == 1:
                                clusters_counts[cl][j] += 1
                                counts_all[j] += 1

        changed = True
        while changed:
                changed = False
                i = 0 
                while i < len(clusters):
                        j = 0
                        while j < len(clusters[i]):
                                largestGainWhere = -1
                                largestGain = -1.0
                                deltaBase = deltaIfRemoved(samples[clusters[i][j]], clusters_counts[i], counts_all, len(clusters), multiplier, power)
                                for k in range(len(clusters)):
                                        if i != k:
                                                delta = deltaBase + deltaIfAdded(samples[clusters[i][j]], clusters_counts[k], counts_all, len(clusters), multiplier, power)
                                                if delta > largestGain:
                                                        largestGain = delta
                                                        largestGainWhere = k
                                if largestGain > 0:
                                        changed = True
                                        cs = clusters[i][j]
                                        del clusters[i][j]
                                        clusters[largestGainWhere].append(cs)
                                        for k in range(len(samples[0])):
                                                if samples[cs][k] == 1:
                                                        clusters_counts[i][k] -= 1
                                                        clusters_counts[largestGainWhere][k] += 1
                                        j -= 1
                                j += 1
                        if len(clusters[i]) == 0:
                                del clusters[i]
                                del clusters_counts[i]
                                i -= 1
                        i += 1

        for i in range(len(clusters)):
                for j in range(len(clusters[i])):
                        labels[clusters[i][j]] = i
        
        return labels
