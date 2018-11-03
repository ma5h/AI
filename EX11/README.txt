
Question 1: DFS
===============
Is DFS the cheapest solution? No.
As we learned in class DFS is not the cheapest solution for a search problem.
The First path to the goal that the DFS will find depends on the node's scan order, that's also explains the comment
in the question that we can get a cost of 130 or 244.

To implement DFS I used the algorithm described in the text book in Figure 3.11, found in my code under 'frontierSearch'.
The function frontierSearch has two parameters:
#1 problem
#2 frontier data structure - I intent to reuse this function for DFS and BFS and the difference is in the frontier
   management. For DFS I used Stack/LIFO this data structure uses the last node that was pushed - this allows the 'depth first' approach.
Other data structures I used are:
frontier_set - To implement graph search it's necessary to validate that the same node isn't entered to the
               frontier again, otherwise loopy path may be added and invalidate the search result. Since the Stack
               data structure doesn't support membership testing I added a set that will keep the current frontier nodes.
explored - A set that keeps the already explored nodes. This data structure needed for the same reasons as the frontier_set.


Question 2: BFS
===============
Is BFS the cheapest solution? Yes.
BFS is a costly algorithm but it's also optimal, each node discovered by the shortest path.
As in BFS I used the frontierSearch function but this time using the Queue/FIFO data structure.
All other explanations are the same as DFS.


Question 3: UCS
===============
To implement UCS I used the algorithm described in the text book in Figure 3.14, found in my code under 'frontierSearchWithCost'.
The function frontierSearchWithCost has three parameters:
#1 problem
#2 frontier data structure - For USC I used PriorityQueue/Min-Heap. Using Min-Heap allows to easily extract the lowest
                             calculated distance needed for Dijkstra's algorithm.
#3 heuristic - This parameter is actually not needed for the USC and uses the nullHeuristic.
               I added this parameter to reuse this code for AStar.
Other data structures I used are (in addition to those explained in DFS):
node_discovery_dict - I use this dictionary to later reconstruct the actions needed to be taken to get from start-start to goal-state.
                      Each entry consist of: (node) -> (action from parent, parent, cost from start_node).
                      During the algorithm execution the entries in this dictionary might get updated if a better path is found.


Question 4: AStar
=================
As in UCS I used the frontierSearchWithCost with PriorityQueue/Min-Heap.
For AStar the heuristic is a key component and it used to improve the path cost prediction.
All other explanations are the same as UCS.


OpenMaze
========
What will happen in the openMaze?
Assumptions: Open Maze is a full square grid, without obstacles, with a single start state and a single goal state.
DFS: Far from optimum, DFS will develop nodes with disregard to the goal location but will eventually find it.
BFS: Develop the nodes in every direction until the goal is found.
UCS: For constant cost act as BFS, otherwise develop the nodes in the direction of the lowest cost until the goal is found.
AStar: At first develop nodes at every direction, but soon enough, if the heuristic is good, peruse the right path.


Question 5: CornersProblem
==========================
The representation that I chose for this problem is a tuple of (current-position, corners-left-to-visit). Using this
representation it is easy to determine if goal state is reached simply by checking if the corners-left-to-visit is empty.
The start state has all four corners and in 'getSuccessors' I check if current position is a corner, if so then this
corner is removed from the corners-left-to-visit.


Question 6: CornersHeuristic
============================
I was able to reach the following results using my heuristic:
        >> python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
        Path found with total cost of 106 in 0.0 seconds
        Search nodes expanded: 781
        Pacman emerges victorious! Score: 434

As described above my state included the current-position and the corners-left-to-visit, both of them was used by the
heuristic function.
CornersHeuristic implementation:
    1. The heuristic calculates for the current-position the Manhattan Distance to each corner from corners-left-to-visit
    2. Then the nearest corner is chosen as the next destination
    3. The distance from current-position to nearest corner is added to the heuristic cost
    4. current-position is set to be the nearest corner, iterate back to step 1 until all corners are visited

The relaxation I used for this heuristic is ignoring the walls and considering only the steps that must be taken in
order to reach all corners.
I believe that this heuristic is both admissible and consistent since it uses the Manhattan Distance.
Manhattan Distance is the minimum steps needed to reach the destination, and the sum of all the Manhattan Distance
path costs to reach all the corners is necessarily the lower bound of the actual cost.


Question 7: FoodHeuristic
=========================
I was able to reach the following results using my heuristic:
        >> python pacman.py -l trickySearch -p AStarFoodSearchAgent
        Path found with total cost of 68 in 2.7 seconds
        Search nodes expanded: 6925
        Pacman emerges victorious! Score: 562

I reused the code in CornersHeuristic for the FoodHeuristic by calling the CornersHeuristic with the food points as the
corners.
If the CornersHeuristic is admissible and consistent so is FoodHeuristic.


Question 8: findPathToClosestDot
================================
AnyFoodSearchProblem::isGoalState in this function the test is if the current state has a food in it. This validation
is done by checking the food matrix supplied by the problem.

ClosestDotSearchAgent::findPathToClosestDot run the AStar search on the AnyFoodSearch problem
