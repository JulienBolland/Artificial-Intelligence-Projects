# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions, GhostRules
import numpy as np
from pacman_module import util

#from scipy.stats import entropy


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'updateAndGetBeliefStates' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None
        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None
        # Uniform distribution size parameter 'w'
        # for sensor noise (see instructions)
        self.w = int(self.args.w)
        # Probability for 'leftturn' ghost to take 'EAST' action
        # when 'EAST' is legal (see instructions)
        self.p = self.args.p

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of (noised) ghost positions at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t} about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates
        # XXX: Your code here
        # Retrieving the matrix width and height
        (N, M) = beliefStates[0].shape
        for i in range(len(evidences)):  # Number of ghosts
            # Creating a temporary array
            tmpBS = np.zeros((N, M))
            # For the normalization
            constant = 0.0
            # Retrieving the coordinates of the evidences
            # on the ith ghost
            (e1, e2) = evidences[i]
            # List containing the coordinates of the square
            # surrounding a case [x,y]
            c_list = []
            # Computing the transition matrix for  the ith ghost
            transition = self.transitionModel(N, M, beliefStates[i])
            # As the map is surrounded by walls, these walls contain also
            # coordinates. Therefore the 'playable' area is a matrix of
            # size (N-2*w, M-2*w)
            for x in range(self.w, N-self.w):
                for y in range(self.w, M-self.w):
                    # Building the square of size 2*w + 1 around
                    # the current case checked [x,y]
                    for j in range(x - self.w, x + self.w + 1):
                        for k in range(y - self.w, y + self.w + 1):
                            c_list.append((j, k))
                    if (e1, e2) in c_list:
                        # Probality of being in the square of
                        # size (2*w + 1)
                        p_s_knowing_e = 1/(((2*self.w)+1)**2)
                    else:
                        p_s_knowing_e = 0
                    # Building the new beliefStates matrix
                    tmpBS[x][y] = p_s_knowing_e*transition[x][y]
                    constant += tmpBS[x][y]
                    # Reseting the list
                    c_list = []
            # Normalization
            tmpBS /= constant
            beliefStates[i] = tmpBS.copy()
        # XXX: End of your code
        self.beliefGhostStates = beliefStates
        return beliefStates

    def transitionModel(self, N, M, BS):
        """
        This method computes the transition model given
        a belief state of a ghost.

        Arguments:
        ----------
        - 'N' and 'M' : respectively the width and height of the maze
        - 'BS' : the beliefStates matrix for one ghost

        Return:
        -------
        """
        transition = np.zeros((N, M))
        for x in range(self.w, N-self.w):
            for y in range(self.w, M-self.w):
                # If the checked case is a wall,
                # we do nothing
                if self.walls[x][y]:
                    continue
                # Computing the legal moves
                legal = []
                if(self.walls[x-1][y] is False):
                    legal.append(Directions.WEST)
                if(self.walls[x+1][y] is False):
                    legal.append(Directions.EAST)
                if(self.walls[x][y-1] is False):
                    legal.append(Directions.SOUTH)
                if(self.walls[x][y+1] is False):
                    legal.append(Directions.NORTH)

                dist = util.Counter()
                # Computes the probability of each moves
                if Directions.EAST in legal:
                    # Select EAST with probability p
                    dist[Directions.EAST] = self.p+(1 - self.p) / (len(legal))
                    for a in legal:
                        if a != Directions.EAST:
                            dist[a] = (1 - self.p) / (len(legal))
                else:
                    for a in legal:
                        dist[a] = 1.0/len(legal)

                # Computing the transition model
                transition[x-1][y] += dist[Directions.WEST]*BS[x][y]
                transition[x+1][y] += dist[Directions.EAST]*BS[x][y]
                transition[x][y-1] += dist[Directions.SOUTH]*BS[x][y]
                transition[x][y+1] += dist[Directions.NORTH]*BS[x][y]
        return transition

    def _computeNoisyPositions(self, state):
        """
            Compute a noisy position from true ghosts positions.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        w = self.args.w
        w2 = 2*w+1
        div = float(w2 * w2)
        new_positions = []
        for p in positions:
            (x, y) = p
            dist = util.Counter()
            for i in range(x - w, x + w + 1):
                for j in range(y - w, y + w + 1):
                    dist[(i, j)] = 1.0 / div
            dist.normalize()
            new_positions.append(util.chooseFromDistribution(dist))
        return new_positions

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

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """

        # XXX : You shouldn't care on what is going on below.
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()
        return self.updateAndGetBeliefStates(
            self._computeNoisyPositions(state))
