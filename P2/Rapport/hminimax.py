from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance
import math


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

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
        visitedNodes = set()
        return self.hminimax(state, -math.inf, math.inf,
                             0, visitedNodes, 0)

    def hminimax(self, state, alpha, beta,
                 player, visitedNodes, depth):
        """
        Implementation of the h-minimax algorithm.
        """
        # Initiliazing the maximum depth the recursion
        # can have
        maxDepth = 6
        # If the goal is fullfilled or if
        # we lose or if the maxDepth is obtained,
        # we return the score obtained
        if state.isWin() or state.isLose()\
           or depth == maxDepth:
            return state.getScore() - self.astarAlgo(state)

        # We have to check whether the player is
        # pacman or the ghost.
        # Here, we consider pacman
        if player == 0:
            # toBeDone is the action pacman has to do in order
            # to maximize its score.
            toBeDone = Directions.STOP
            # Initiliazing the sentinel
            maxValue = -math.inf
            # Generate the leaf nodes of the game tree
            for successors in state.generatePacmanSuccessors():
                # Check whether successors is a node already visited
                if (successors[0].getPacmanPosition(),
                   successors[0].getGhostPosition(1),
                   successors[0].getFood(),
                   player) in visitedNodes:
                    continue
                visitedNodes.add((successors[0].getPacmanPosition(),
                                 successors[0].getGhostPosition(1),
                                 successors[0].getFood(),
                                 player))
                # We create a copy of the set containing
                # the nodes already visited, in order to
                # use it in the recursion because several
                # nodes can be the same but have to be
                # checked too
                visitedCopy = visitedNodes.copy()
                # Recursion for an incremented depth
                tmpValue = self.hminimax(successors[0],
                                         alpha, beta,
                                         1, visitedCopy,
                                         depth + 1)
                # Actualisation of the maximum value found
                # and the value of alpha
                if tmpValue != math.inf and tmpValue > maxValue:
                    maxValue = tmpValue
                    toBeDone = successors[1]
                if maxValue >= beta:
                    return maxValue
                alpha = max(alpha, maxValue)
            # If the recursion is finished, depth = 0
            if depth == 0:
                return toBeDone

            return maxValue

        # Here, we consider the ghost
        elif player == 1:
            # Initiliazing the sentinel
            minValue = math.inf
            # Generate the leaf nodes of the game tree
            for successors in state.generateGhostSuccessors(1):
                if (successors[0].getPacmanPosition(),
                   successors[0].getGhostPosition(1),
                   successors[0].getFood(),
                   player) in visitedNodes:
                    continue
                visitedNodes.add((successors[0].getPacmanPosition(),
                                 successors[0].getGhostPosition(1),
                                 successors[0].getFood(),
                                 player))
                visitedCopy = visitedNodes.copy()
                # Recursion for an incremented depth
                tmpValue = self.hminimax(successors[0],
                                         alpha, beta,
                                         0, visitedCopy,
                                         depth + 1)

                if tmpValue != -math.inf and tmpValue < minValue:
                    minValue = tmpValue
                if minValue <= alpha:
                    return minValue
                beta = min(beta, minValue)

            return minValue

    def astarAlgo(self, state):
        """
        Implements the a-star algorithm
        """
        cost = 0
        visitedNodes = set()
        queueOfStates = PriorityQueue()
        queueOfStates.push((state, cost), 0)
        dictionnary = dict()
        dictionnary[state] = (None)
        foods = state.getFood()

        while not queueOfStates.isEmpty():
            _, (actualState, cost) = queueOfStates.pop()
            position = actualState.getPacmanPosition()
            food = actualState.getFood()

            if foods != actualState.getFood():
                return self.getWinDistance(dictionnary, actualState)

            if (position, food) in visitedNodes:
                continue
            else:
                visitedNodes.add((position, food))
                for successors in actualState.generatePacmanSuccessors():

                    dictionnary[successors[0]] = actualState
                    if food == successors[0].getFood():
                        incrementedCost = 10
                    else:
                        incrementedCost = 1

                    heuristic = self.heuristicFunction(successors[0])
                    totalCost = cost + incrementedCost + heuristic*10
                    queueOfStates.push((successors[0], cost+incrementedCost),
                                       totalCost)

        return 0

    def getWinDistance(self, dictionnary, node):
        """
        This function returns a complete path, giving a node
        """
        distanceForTheWin = 0
        while dictionnary[node] is not None:
            node = dictionnary[node]
            distanceForTheWin += 1

        return distanceForTheWin

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

        return min(heuristics)
