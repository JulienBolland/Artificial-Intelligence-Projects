from pacman_module.game import Agent
from pacman_module.pacman import Directions
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
        return self.alphabeta(state, -math.inf, math.inf,
                              0, visitedNodes, 0)

    def alphabeta(self, state, alpha, beta, player,
                  visitedNodes, depth):
        """
        Implementation of alpha-beta algorithm.

        Note : player = 0 when the player is pacman
               player = 1 when the player is ghost
        """
        # If the goal is fullfilled or if
        # we lose, we return the score obtained
        if state.isWin() or state.isLose():
            return state.getScore()

        # We have to check whether the player is
        # pacman or the ghost.
        # Here, we consider pacman
        if player == 0:
            # toBeDone is the action pacman has to do in order
            # to maximize its score.
            toBeDone = Directions.STOP
            # Initiliazing the sentinel
            maxValue = - math.inf
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
                # Recursion
                tmpValue = self.alphabeta(successors[0],
                                          alpha, beta,
                                          1, visitedCopy,
                                          depth)
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
                tmpValue = self.alphabeta(successors[0],
                                          alpha, beta,
                                          0, visitedCopy,
                                          depth + 1)
                # Actualisation of the minimum value found
                # and the value of beta
                if tmpValue != -math.inf and tmpValue < minValue:
                    minValue = tmpValue
                    if minValue <= alpha:
                        return minValue
                    beta = min(beta, minValue)

            return minValue
