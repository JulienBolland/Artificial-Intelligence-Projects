import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

w_list = [1, 3, 5]
p_list = [0.01, 0.25, 0.5, 0.75, 1.0]

for w in w_list:
    for p in p_list:
        entropy = []
        for i in range(10,91):
            sample = pd.read_csv("results/Entropy_w{}_p{}_{}.csv".format(w,p,i))
            entropy.append(np.array(sample))
        average = np.mean(entropy, axis=0)
        std = np.std(entropy, axis=0)
        plt.plot(range(50),average)

    plt.title('Evolution of entropy for w = {}'.format(w), fontsize = '12')
    plt.legend(['p = 0.01','p = 0.25','p = 0.5','p = 0.75', 'p = 1.0'], fontsize = '8')
    plt.xlabel("Number of time steps", fontsize='15')
    plt.ylabel("Entropy", fontsize='15')
    plt.savefig("graph/GraphEntropy{}.png".format(w))
    plt.close()
