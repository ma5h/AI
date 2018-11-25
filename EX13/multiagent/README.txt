
Question 1: Reflex Agent
========================
The reflex agent is simple - if ghosts are too close then escape from it, otherwise head to the direction of
the closest food location.
The distance from the ghost is an easy part because it needs to be maximized but the distance from food needs to be
minimized. To calculate the distance from food I calculated the max manhattanDistance available in layout be summing
layout width and height and from that subtracted the Pacman's distance from closest food. This formula maximizes the
distance from food and works quite good.


Question 2: MinimaxAgent
========================
Implemented in MinimaxAgent::value this method returns a tuple of (score, action) for the current move.
Some of the methods are implemented in the super class MultiAgentSearchAgent.


Question 3: AlphaBetaAgent
==========================
Implemented in AlphaBetaAgent::value works similar to MinimaxAgent except it prunes branches that will not change the
outcome calculated thus far. This agent doesn't preform as well because it overly pessimistic and prefers the act of
suicide in order to not harm the final score.


Question 4: ExpectimaxAgent
===========================
Implemented in ExpectimaxAgent::value calculates the mean score from ghosts based on their available actions. This, in
comparison to the previous agent is a more successful game plan.
