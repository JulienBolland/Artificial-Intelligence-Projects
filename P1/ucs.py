from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue


class PacmanAgent(Agent):
    """
    An agent controlled by the depth-first seach algorithm.
    """
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.actionDone = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        if not self.actionDone:
            # If we execute get_action for the first time,
            # we compute de search
            self.actionDone = self.ucsAlgo(state)

        return self.actionDone.pop()

    def ucsAlgo(self, state):
        """
        Implements the uniform cost algorithm
        """
        visitedNodes = set()
        cost = 0
        queueOfStates = PriorityQueue()
        queueOfStates.push(state, cost)
        dictionnary = dict()
        dictionnary[state] = (None)

        while not queueOfStates.isEmpty():
            cost, actualState = queueOfStates.pop()
            position = actualState.getPacmanPosition()
            food = actualState.getFood()
            # If the goal is fullfilled, we win
            if actualState.isWin():
                return self.getWinPath(dictionnary, actualState)

            if (position, food) in visitedNodes:
                continue
            else:
                visitedNodes.add((position, food))
                for successors in actualState.generatePacmanSuccessors():

                    dictionnary[successors[0]] = actualState
                    if food == successors[0].getFood():
                        incrementedCost = 1
                    else:
                        incrementedCost = 0
                    totalCost = cost + incrementedCost
                    queueOfStates.push(successors[0], totalCost)

    def getWinPath(self, dictionnary, actualNode):
        """
        This function returns a complete path, giving the actual node
        """
        pathForTheWin = []
        while dictionnary[actualNode] is not None:
            pathForTheWin.append(actualNode.getPacmanState().getDirection())
            actualNode = dictionnary[actualNode]

        return pathForTheWin
