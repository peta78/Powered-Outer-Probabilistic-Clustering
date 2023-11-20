import matplotlib.pyplot as plt

def display(labelsWithSamples, title):
        fig = plt.gcf()
        fig.set_size_inches(12, 7)

        colors = ['b','g','r','c','m','y','k']
        labelsWithSamples = sorted(labelsWithSamples, key=lambda s: s[0])

        for i in range(len(labelsWithSamples)):
                for j in range(len(labelsWithSamples[i][1])):
                        if labelsWithSamples[i][1][j] == 1:
                                plt.plot(j, i, colors[labelsWithSamples[i][0] % 7] + 'o', markersize=1)

        plt.title(title)
        plt.show()

        
