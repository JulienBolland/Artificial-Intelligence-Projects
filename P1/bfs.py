from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Queue


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
            self.actionDone = self.bfsAlgo(state)

        return self.actionDone.pop()

    def bfsAlgo(self, state):
        """
        Implements the breadth-first algorithm
        """
        visitedNodes = set()
        queueOfStates = Queue()
        queueOfStates.push(state)
        dictionnary = dict()
        dictionnary[state] = (None)

        while not queueOfStates.isEmpty():
            actualState = queueOfStates.pop()

            # If the goal is fullfilled, we win
            if actualState.isWin():
                return self.getWinPath(dictionnary, actualState)

            if (actualState.getPacmanPosition(),
               actualState.getFood()) in visitedNodes:
                continue

            else:
                visitedNodes.add((actualState.getPacmanPosition(),
                                 actualState.getFood()))
                for successors in actualState.generatePacmanSuccessors():
                    dictionnary[successors[0]] = actualState
                    queueOfStates.push(successors[0])

    def getWinPath(self, dictionnary, actualNode):
        """
        This function returns a complete path, giving the actual node
        and the dictionnary containing all the nodes
        """
        pathForTheWin = []
        while dictionnary[actualNode] is not None:
            pathForTheWin.append(actualNode.getPacmanState().getDirection())
            actualNode = dictionnary[actualNode]

        return pathForTheWin
