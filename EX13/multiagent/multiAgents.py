# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    scores_map = []
    for action in legalMoves:
      scores_map.append(([self.evaluationFunction(gameState, action)], action))

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    # calculate distance from ghosts
    dists_from_ghosts = [manhattanDistance(ghost.getPosition(), newPos) for ghost in newGhostStates]
    min_dist_from_ghosts = min(dists_from_ghosts) if dists_from_ghosts else 0

    # calculate distance from food
    dists_from_food = []
    for x in range(oldFood.width):
      for y in range(oldFood.height):
        if oldFood[x][y]:
          dists_from_food.append(manhattanDistance((x, y), newPos))
    min_dist_from_food = min(dists_from_food) if dists_from_food else 0

    grid_size = oldFood.height + oldFood.width  # maximal manhattan distance for this layout

    if min_dist_from_ghosts < 3:    # Ghost is very close... RUN!
      score = min_dist_from_ghosts
    else:                           # Ghosts are far - go find food
      score = grid_size - min_dist_from_food

    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

  @staticmethod
  def max_action(*args):
    valid_args = [x for x in args if x[0] is not None]  # filter None values for cost in tuple (cost, action)

    if not valid_args:
      return None, None

    return max(valid_args)  # max works on the first value of the tuple

  @staticmethod
  def min_action(*args):
    valid_args = [x for x in args if x[0] is not None]  # filter None values for cost in tuple (cost, action)

    if not valid_args:
      return None, None

    return min(valid_args)  # min works on the first value of the tuple

  @staticmethod
  def is_max_agent(agentIndex):
    return agentIndex == 0  # agentIndex=0 means Pacman

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    res = self.value(gameState, 0, 0)
    return res[1]

  def value(self, gameState, depth, agentIndex):

    if agentIndex == gameState.getNumAgents():
      depth += 1

    if depth == self.depth or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState), None

    if agentIndex == gameState.getNumAgents():
      agentIndex = 0

    min_max_action_function = self.max_action if self.is_max_agent(agentIndex) else self.min_action
    return self.min_max_value(gameState, depth, agentIndex, min_max_action_function)

  def min_max_value(self, gameState, depth, agentIndex, min_max_action_function):
    v = (None, None)

    for action in gameState.getLegalActions(agentIndex):
      new_state_value = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)[0]
      v = min_max_action_function(v, (new_state_value, action))
    return v

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    res = self.value(gameState, 0, 0, None, None)
    return res[1]

  @staticmethod
  def max_int_action(*args):
    valid_args = [x for x in args if x is not None]  # filter None values for cost in tuple (cost, action)

    if not valid_args:
      return None, None

    return max(valid_args)  # max works on the first value of the tuple

  @staticmethod
  def min_int_action(*args):
    valid_args = [x for x in args if x is not None]  # filter None values for cost in tuple (cost, action)

    if not valid_args:
      return None, None

    return min(valid_args)  # min works on the first value of the tuple

  def value(self, gameState, depth, agentIndex, alpha, beta):

    if agentIndex == gameState.getNumAgents():
      depth += 1

    if depth == self.depth or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState), None

    if agentIndex == gameState.getNumAgents():
      agentIndex = 0

    if self.is_max_agent(agentIndex):
      return self.max_value(gameState, depth, agentIndex, alpha, beta)
    else:
      return self.min_value(gameState, depth, agentIndex, alpha, beta)

  def max_value(self, gameState, depth, agentIndex, alpha, beta):
    v = (None, None)

    for action in gameState.getLegalActions(agentIndex):
      new_state_value = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)[0]
      v = self.max_action(v, (new_state_value, action))
      alpha = self.max_int_action(alpha, v[0])
      if beta is not None and alpha is not None and alpha > beta:
        return v
    return v

  def min_value(self, gameState, depth, agentIndex, alpha, beta):
    v = (None, None)

    for action in gameState.getLegalActions(agentIndex):
      new_state_value = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)[0]
      v = self.min_action(v, (new_state_value, action))
      beta = self.min_int_action(beta, v[0])
      if beta is not None and alpha is not None and alpha > beta:
        return v
    return v


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    res = self.value(gameState, 0, 0)
    return res[1]

  def value(self, gameState, depth, agentIndex):

    if agentIndex == gameState.getNumAgents():
      depth += 1

    if depth == self.depth or gameState.isWin() or gameState.isLose():
      return self.evaluationFunction(gameState), None

    if agentIndex == gameState.getNumAgents():
      agentIndex = 0

    if self.is_max_agent(agentIndex):
      return self.max_value(gameState, depth, agentIndex)
    else:
      return self.expectimax_value(gameState, depth, agentIndex)

  def max_value(self, gameState, depth, agentIndex):
    v = (None, None)

    for action in gameState.getLegalActions(agentIndex):
      new_state_value = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)[0]
      v = self.max_action(v, (new_state_value, action))
    return v

  def expectimax_value(self, gameState, depth, agentIndex):
    cost = 0
    num_legal_actions = len(gameState.getLegalActions(agentIndex))
    for action in gameState.getLegalActions(agentIndex):
      cost += self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)[0]
    return cost*1.0 / num_legal_actions, None

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

