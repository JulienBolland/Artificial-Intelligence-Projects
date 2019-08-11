from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance


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
            self.actionDone = self.astarAlgo(state)

        return self.actionDone.pop()

    def astarAlgo(self, state):
        """
        Implements the a-star algorithm
        """
        visitedNodes = set()
        cost = 0
        queueOfStates = PriorityQueue()
        queueOfStates.push((state, cost), 0)
        dictionnary = dict()
        dictionnary[state] = (None)

        while not queueOfStates.isEmpty():
            _, (actualState, cost) = queueOfStates.pop()
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

                    dictionnary[successors[0]] = actualState():
                    if food == successors[0].getFood():
                        incrementedCost = 10
                    else:
                        incrementedCost = 1

                    heuristic = self.heuristicFunction(successors[0])
                    totalCost = cost + incrementedCost + heuristic*10
                    queueOfStates.push((successors[0], cost+incrementedCost),
                                       totalCost)

    def getWinPath(self, dictionnary, node):
        """
        This function returns a complete path, giving a node
        """
        pathForTheWin = []
        while dictionnary[node] is not None:
            pathForTheWin.append(node.getPacmanState().getDirection())
            node = dictionnary[node]

        return pathForTheWin

    def heuristicFunction(self, state):
        """
        This function computes the path cost between a node at a
        state and a goal node.
        """
        foodMatrix = state.getFood()
        position = state.getPacmanPosition()
        heuristics = set()
        for x in range(0, foodMatrix.width):
            for y in range(0, foodMatrix.height):
                if foodMatrix[x][y] is True:
                    manhattan = manhattanDistance(position, (x, y))
                    heuristics.add(manhattan)
        if not heuristics:
            return 0

        return max(heuristics)
