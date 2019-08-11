import matplotlib.pyplot as pt
import numpy as np
#            minimax / alphabeta / h-minimax
RT = np.array([[.76634,.06948,.0197618],#smarty
             [.74431,.08949,0.020444],#greedy
             [.785838,.066234,.025944]])#dumby

score = np.array([[526,526,526],#small
                  [526,526,526],#medium
                  [526,526,526]])#large

nodes = np.array([[6423,479,94],#small
                  [6423,479,94],#medium
                  [6423,479,94]])#large

pt.figure(figsize=(6,5))
pt.title("Expanded nodes for a smarty ghost")
pt.xlabel("Algorithms")
pt.ylabel("Score")

nb_algo = 3
bar_width = .5
bar_positions = np.arange(nb_algo)

for i in range(0,nb_algo):
    pt.bar(bar_positions[i], nodes[0][i], width = bar_width)

algo = ['minimax', 'alpha-bêta', 'h-minimax']
#maps = ['small','medium','large']

pt.xticks(bar_positions, ["%s" % algo[i] for i in range(0,nb_algo)])
#pt.legend(["%s" % algo[i] for i in range(0,4)])
pt.show()
