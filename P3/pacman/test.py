from os import system

w_list = [1, 3, 5]
p_list = [0.01, 0.25, 0.5, 0.75, 1]
for w in w_list:
    for p in p_list:
        for i in range(10,91):
            system("python run.py --layout observer --agentfile randomagent.py --silentdisplay --bsagentfile beliefstateagent.py --ghostagent rightrandy --w {},{}  --p {} --hiddenghost".format(w,i,p))
