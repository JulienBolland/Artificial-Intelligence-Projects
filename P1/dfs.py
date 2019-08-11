from pacman_module.game import Agent
from pacman_module.pacman import Directions


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
            # If we execute get_action for the first time
            visitedNodes = []
            self.actionDone = self.dfsAlgo(state, visitedNodes)

        return self.actionDone.pop()

    def dfsAlgo(self, state, visitedNodes):
        position = state.getPacmanPosition()
        food = state.getNumFood()
        # Actualise the visited nodes by actual position
        visitedNodes.append([position, food])

        # If the goal is fullfilled, we win
        if state.isWin():
            return []

        # Otherwise we generate the successors
        for successors in state.generatePacmanSuccessors():
            # If the successors has been already visited,
            # we do nothing
            if [successors[0].getPacmanPosition(),
               successors[0].getNumFood()] in visitedNodes:
                continue
                # Recursion
            nextNode = self.dfsAlgo(successors[0], visitedNodes)
            # If nextNode is a node with successors, we return it
            if nextNode is not None:
                nextNode.append(successors[0].getPacmanState().getDirection())
                return nextNode
