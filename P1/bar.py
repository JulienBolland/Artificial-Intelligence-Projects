import matplotlib.pyplot as pt
import numpy as np

RT = np.array([[.0039649,.0059237,.0031412,.0029848],#small
             [.0951441,4.1806731,3.1323082,2.9518239],#medium
             [.2370159,1.1696217,1.01638818,.7432537]])#large

score = np.array([[502,502,502,502],#small
                  [344,570,570,570],#medium
                  [306,434,434,434]])#large

nodes = np.array([[15,15,15,14],#small
                  [364,16688,12517,8388],#medium
                  [525,1966,1908,1073]])#large

pt.figure(figsize=(6,5))
pt.title("Expanded nodes for the medium layout")
pt.xlabel("Algorithms")
pt.ylabel("Number of expanded nodes)")

nb_algo = 4
bar_width = .5
bar_positions = np.arange(4)

for i in range(0,4):
    pt.bar(bar_positions[i], nodes[1][i], width = bar_width)

algo = ['dfs', 'bfs', 'ucs', 'A*']
#maps = ['small','medium','large']

pt.xticks(bar_positions, ["%s" % algo[i] for i in range(0,4)])
#pt.legend(["%s" % algo[i] for i in range(0,4)])
pt.show()
