# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import game

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  return frontierSearch(problem, util.Stack())


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"

  return frontierSearch(problem, util.Queue())


def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  return frontierSearchWithCost(problem, util.PriorityQueue(), nullHeuristic)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  return frontierSearchWithCost(problem, util.PriorityQueue(), heuristic)
    

#print "Start:", problem.getStartState()                                             #  (5, 5)
#print "Is the start a goal?", problem.isGoalState(problem.getStartState())          # False
#print "Start's successors:", problem.getSuccessors(problem.getStartState())         # [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
#print "Start's successors cost:", problem.getCostOfActions([game.Directions.WEST])  # 1
def frontierSearch(problem, frontier):
  start_node = problem.getStartState()
  if problem.isGoalState(start_node):
    return []

  frontier.push(start_node)
  frontier_set = {start_node}  # !! non empty set initialization
  explored = set()             # !! empty set initialization
  node_discovery_dict = {}  # (5, 4) -> ('South', (5, 5))  //(5, 4) was reached by going South from (5, 5)

  while True:
    if frontier.isEmpty():
      return [game.Directions.STOP]

    node = frontier.pop()
    frontier_set.remove(node)

    explored.add(node)

    for successor in problem.getSuccessors(node):  # [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
      if (successor[0] not in explored) and (successor[0] not in frontier_set):
        node_discovery_dict[successor[0]] = (successor[1], node)
        if problem.isGoalState(successor[0]):
          return buildActionsList(node_discovery_dict, successor[0])
        frontier.push(successor[0])
        frontier_set.add(successor[0])


def frontierSearchWithCost(problem, frontier, heuristic):
  start_node = problem.getStartState()
  if problem.isGoalState(start_node):
    return []

  frontier.push(start_node, heuristic(start_node, problem))
  frontier_set = {start_node}  # !! non empty set initialization
  explored = set()             # !! empty set initialization
  # node_discovery_dict: (5, 4) -> ('South', (5, 5), cost)  //(5, 4) was reached by going South from (5, 5) with cost from start_node
  node_discovery_dict = {start_node: (None, None, 0)}

  while True:
    if frontier.isEmpty():
      return [game.Directions.STOP]

    node = frontier.pop()
    frontier_set.remove(node)

    if problem.isGoalState(node):
      return buildActionsList(node_discovery_dict, node)

    explored.add(node)

    for successor in problem.getSuccessors(node):  # [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
      new_successor_path_cost = node_discovery_dict[node][2] + successor[2] + heuristic(successor[0], problem)

      if (successor[0] not in explored) and (successor[0] not in frontier_set):
        node_discovery_dict[successor[0]] = (successor[1], node, new_successor_path_cost)
        frontier.push(successor[0], new_successor_path_cost)
        frontier_set.add(successor[0])
      elif successor[0] in frontier_set:
        old_successor_path_cost = node_discovery_dict[successor[0]][2]
        if new_successor_path_cost < old_successor_path_cost:
            node_discovery_dict[successor[0]] = (successor[1], node, new_successor_path_cost)


def buildActionsList(node_discovery_dict, final_node):
  actions_list = []
  node = final_node  # (7, 2)

  while node in node_discovery_dict:  # ('South', (5, 5))
    action = node_discovery_dict.get(node)[0]   # 'South'
    if action:
      actions_list.append(action)
    node = node_discovery_dict.get(node)[1]  # (5, 5)

  actions_list.reverse()
  return actions_list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch