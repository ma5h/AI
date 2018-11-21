import util
import sys


class CannibalsMissionariesProblem:
    state_machine = {}

    def __init__(self):
        #  (C, M, 0) | C>=2) -> {(C-2 ,M, 1), (C-1, M, 1)}
        self.__update_state_machine__((2, 0, 0), {(0, 0, 1), (1, 0, 1)})
        self.__update_state_machine__((2, 1, 0), {(0, 1, 1), (1, 1, 1)})
        self.__update_state_machine__((2, 2, 0), {(0, 2, 1), (1, 2, 1)})
        self.__update_state_machine__((2, 3, 0), {(0, 3, 1), (1, 3, 1)})

        self.__update_state_machine__((3, 0, 0), {(1, 0, 1), (2, 0, 1)})
        self.__update_state_machine__((3, 1, 0), {(1, 1, 1), (2, 1, 1)})
        self.__update_state_machine__((3, 2, 0), {(1, 2, 1), (2, 2, 1)})
        self.__update_state_machine__((3, 3, 0), {(1, 3, 1), (2, 3, 1)})

        #  (C, M, 0) | M>=2) -> {(C, M-2, 1), (C, M-1, 1)}
        self.__update_state_machine__((0, 2, 0), {(0, 0, 1), (0, 1, 1)})
        self.__update_state_machine__((1, 2, 0), {(1, 0, 1), (1, 1, 1)})
        self.__update_state_machine__((2, 2, 0), {(2, 0, 1), (2, 1, 1)})
        self.__update_state_machine__((3, 2, 0), {(3, 0, 1), (3, 1, 1)})

        self.__update_state_machine__((0, 3, 0), {(0, 1, 1), (0, 2, 1)})
        self.__update_state_machine__((1, 3, 0), {(1, 1, 1), (1, 2, 1)})
        self.__update_state_machine__((2, 3, 0), {(2, 1, 1), (2, 2, 1)})
        self.__update_state_machine__((3, 3, 0), {(3, 1, 1), (3, 2, 1)})

        #  (C, M, 0) | C>=1) -> {(C-1, M, 1)}
        self.__update_state_machine__((1, 0, 0), {(0, 0, 1)})
        self.__update_state_machine__((1, 1, 0), {(0, 1, 1)})
        self.__update_state_machine__((1, 2, 0), {(0, 2, 1)})
        self.__update_state_machine__((1, 3, 0), {(0, 3, 1)})

        #  (C, M, 0) | M>=1) -> {(C, M - 1, 1)}
        self.__update_state_machine__((0, 1, 0), {(0, 0, 1)})
        self.__update_state_machine__((1, 1, 0), {(1, 0, 1)})
        self.__update_state_machine__((2, 1, 0), {(2, 0, 1)})
        self.__update_state_machine__((3, 1, 0), {(3, 0, 1)})

        #  (C, M, 0) | M>=1 ^ C>=1) -> {(C-1, M-1, 1)}
        self.__update_state_machine__((1, 1, 0), {(0, 0, 1)})
        self.__update_state_machine__((2, 1, 0), {(1, 0, 1)})
        self.__update_state_machine__((3, 1, 0), {(2, 0, 1)})

        self.__update_state_machine__((1, 2, 0), {(0, 1, 1)})
        self.__update_state_machine__((2, 2, 0), {(1, 1, 1)})
        self.__update_state_machine__((3, 2, 0), {(2, 1, 1)})

        self.__update_state_machine__((1, 3, 0), {(0, 2, 1)})
        self.__update_state_machine__((2, 3, 0), {(1, 2, 1)})
        self.__update_state_machine__((3, 3, 0), {(2, 2, 1)})

        #  (C, M, 1) | C<=1) -> {(C+2, M, 0), (C+1, M, 0)}
        self.__update_state_machine__((0, 0, 1), {(2, 0, 0), (1, 0, 0)})
        self.__update_state_machine__((0, 1, 1), {(2, 1, 0), (1, 1, 0)})
        self.__update_state_machine__((0, 2, 1), {(2, 2, 0), (1, 2, 0)})
        self.__update_state_machine__((0, 3, 1), {(2, 3, 0), (1, 3, 0)})

        self.__update_state_machine__((1, 0, 1), {(3, 0, 0), (2, 0, 0)})
        self.__update_state_machine__((1, 1, 1), {(3, 1, 0), (2, 1, 0)})
        self.__update_state_machine__((1, 2, 1), {(3, 2, 0), (2, 2, 0)})
        self.__update_state_machine__((1, 3, 1), {(3, 3, 0), (2, 3, 0)})

        #  (C, M, 1) | M<=1) -> {(C, M+2, 0), (C, M+1, 0)}
        self.__update_state_machine__((0, 0, 1), {(0, 2, 0), (0, 1, 0)})
        self.__update_state_machine__((1, 0, 1), {(1, 2, 0), (1, 1, 0)})
        self.__update_state_machine__((2, 0, 1), {(2, 2, 0), (2, 1, 0)})
        self.__update_state_machine__((3, 0, 1), {(3, 2, 0), (3, 1, 0)})

        self.__update_state_machine__((0, 1, 1), {(0, 3, 0), (2, 2, 0)})
        self.__update_state_machine__((1, 1, 1), {(1, 3, 0), (2, 2, 0)})
        self.__update_state_machine__((2, 1, 1), {(2, 3, 0), (2, 2, 0)})
        self.__update_state_machine__((3, 1, 1), {(3, 3, 0), (2, 2, 0)})

        #  (C, M, 1) | C<=2) -> {(C+1, M, 0)}
        self.__update_state_machine__((2, 0, 1), {(3, 0, 0)})
        self.__update_state_machine__((2, 1, 1), {(3, 1, 0)})
        self.__update_state_machine__((2, 2, 1), {(3, 2, 0)})
        self.__update_state_machine__((2, 3, 1), {(3, 3, 0)})

        #  (C, M, 1) | M<=2) -> {(C, M+1, 0)}
        self.__update_state_machine__((0, 2, 1), {(0, 3, 0)})
        self.__update_state_machine__((1, 2, 1), {(1, 3, 0)})
        self.__update_state_machine__((2, 2, 1), {(2, 3, 0)})
        self.__update_state_machine__((3, 2, 1), {(3, 3, 0)})

        #  (C, M, 1) | M<=2 ^ C<=2) -> {(C+1, M+1, 0)}
        self.__update_state_machine__((0, 0, 1), {(1, 1, 0)})
        self.__update_state_machine__((1, 0, 1), {(2, 1, 0)})
        self.__update_state_machine__((2, 0, 1), {(3, 1, 0)})

        self.__update_state_machine__((0, 1, 1), {(1, 2, 0)})
        self.__update_state_machine__((1, 1, 1), {(2, 2, 0)})
        self.__update_state_machine__((2, 1, 1), {(3, 2, 0)})

        self.__update_state_machine__((0, 2, 1), {(1, 3, 0)})
        self.__update_state_machine__((1, 2, 1), {(2, 3, 0)})
        self.__update_state_machine__((2, 2, 1), {(3, 3, 0)})

    def __update_state_machine__(self, k, v):
        if k in self.state_machine:
            self.state_machine[k] |= v
        else:
            self.state_machine[k] = v

    def get_successors(self, state):
        successors = []
        for s in self.state_machine[state]:
            if CannibalsMissionariesProblem.is_valid_state(s):
                successors.append(s)
        return successors

    @staticmethod
    def get_start_state():
        return 3, 3, 0

    @staticmethod
    def is_goal_state(state):
        return state in [(0, 0, 0), (0, 0, 1)]

    @staticmethod
    def is_valid_state(state):
        c, m, b = state
        return (m >= c or m == 0) and (3-m >= 3-c or m == 3)


def greedy_heuristic(state, problem):
    if not problem.is_valid_state(state):
        return sys.maxint

    c, m, b = state

    if m > 0 and (m != 2 or c != 2):
        return 2 * (m + c) + b
    else:
        return 2 * (m + c) + b - 1


def breadth_first_search():
    res = frontier_search(CannibalsMissionariesProblem(), util.Queue())
    print "breadth_first_search: " + str(res)


def frontier_search(problem, frontier_ds):
    start_node = problem.get_start_state()
    if problem.is_goal_state(start_node):
        return [start_node]

    frontier_ds.push(start_node)
    frontier_set = {start_node}  # !! non empty set initialization
    explored = set()  # !! empty set initialization
    node_discovery_dict = {}

    while True:
        if frontier_ds.isEmpty():
            print "no solution found :("
            return None  # no solution found :(

        node = frontier_ds.pop()
        frontier_set.remove(node)

        explored.add(node)

        for successor in problem.get_successors(node):
            if (successor not in explored) and (successor not in frontier_set):
                node_discovery_dict[successor] = (successor, node)
                if problem.is_goal_state(successor):
                    return build_actions_list(node_discovery_dict, successor)  # found the solution :)
                frontier_ds.push(successor)
                frontier_set.add(successor)


def greedy_first_search():
    #res = greedy_best_first_search(CannibalsMissionariesProblem(), greedy_heuristic)

    res = frontier_search_with_heuristic(CannibalsMissionariesProblem(), util.PriorityQueue(), greedy_heuristic)
    print "greedy_first_search: " + str(res)


def greedy_best_first_search(problem, heuristic):
    start_node = problem.get_start_state()
    if problem.is_goal_state(start_node):
        return [start_node]

    node_discovery_dict = {}
    best_node = start_node

    c, m, b = best_node
    print "h(" + str(c) + "," + str(m) + "," + str(b) + ")=" + str(heuristic(best_node, problem))

    while True:
        new_best_node = None
        best_node_cost = sys.maxint

        #  print "successors: " + str(problem.get_successors(best_node))
        for successor in problem.get_successors(best_node):
            curr_successor_cost = heuristic(successor, problem)
            #  print "curr_successor_cost: " + str(curr_successor_cost)
            if best_node_cost > curr_successor_cost:
                best_node_cost = curr_successor_cost
                new_best_node = successor

        if new_best_node is None:
            print "no solution found :("
            return None  # no solution found :(

        node_discovery_dict[new_best_node] = (new_best_node, best_node)
        best_node = new_best_node

        c,m,b=best_node
        print "h(" + str(c) + "," + str(m) + "," + str(b) + ")=" + str(heuristic(best_node, problem))

        if problem.is_goal_state(best_node):
            return build_actions_list(node_discovery_dict, best_node)  # found the solution :)


def frontier_search_with_heuristic(problem, frontier, heuristic):
    start_node = problem.get_start_state()
    if problem.is_goal_state(start_node):
        return [start_node]

    frontier.push(start_node, heuristic(start_node, problem))
    frontier_set = {start_node}  # !! non empty set initialization
    explored = set()             # !! empty set initialization
    # (node) -> (node, parent, path cost)
    node_discovery_dict = {}  # empty dict

    while True:
        if frontier.isEmpty():
            print "no solution found :("
            return None  # no solution found :(

        node = frontier.pop()
        frontier_set.remove(node)

        if problem.is_goal_state(node):
            return build_actions_list(node_discovery_dict, node)

        explored.add(node)

        for successor in problem.get_successors(node):
            new_successor_path_cost = heuristic(successor, problem)

            if (successor not in explored) and (successor not in frontier_set):
                node_discovery_dict[successor] = (successor, node, new_successor_path_cost)
                frontier.push(successor, new_successor_path_cost)
                frontier_set.add(successor)
            elif successor in frontier_set:
                old_successor_path_cost = node_discovery_dict[successor][2]
                if new_successor_path_cost < old_successor_path_cost:
                    node_discovery_dict[successor] = (successor, node, new_successor_path_cost)


def build_actions_list(node_discovery_dict, final_node):
    actions_list = []
    node = final_node

    while node in node_discovery_dict:
        action = node_discovery_dict.get(node)[0]
        if action:
            actions_list.append(action)
        node = node_discovery_dict.get(node)[1]

    actions_list.append(node)  # add start_state
    actions_list.reverse()
    return actions_list


breadth_first_search()  # [(3, 3, 0), (2, 2, 1), (2, 3, 0), (0, 3, 1), (1, 3, 0), (1, 1, 1), (2, 2, 0), (2, 0, 1), (3, 0, 0), (1, 0, 1), (1, 1, 0), (0, 0, 1)]
greedy_first_search()  # [(3, 3, 0), (2, 2, 1), (2, 3, 0), (0, 3, 1), (1, 3, 0), (1, 1, 1), (2, 2, 0), (2, 0, 1), (3, 0, 0), (1, 0, 1), (2, 0, 0), (0, 0, 1)]
