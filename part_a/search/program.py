# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor
from .utils import render_board
import heapq

def heuristic(state):
    return 0  # Placeholder, replace with your heuristic calculation

def f_score(state, g_score):
    return g_score + heuristic(state)

def make_hashable(state : dict[Coord, CellState]):
    # Convert the state dictionary to a frozenset of items for hashing
    return tuple((i, j) for i, j in state.items())

def rev_hashable(hashable_state):
    # Convert the frozenset of items back to a dictionary
    return dict(hashable_state)

def is_goal(state : dict[Coord, CellState]):
    for i in state.values():
        if i.color == PlayerColor.BLUE:
            return False
    return True

def get_next_states(state : dict[Coord, CellState]):
    # Placeholder, replace with your logic to generate next states
    return []

def search(
    board: dict[Coord, CellState]
) -> list[Action] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to `CellState` instances (each with a `.color` and
            `.height` attribute).

    Returns:
        A list of actions (MoveAction, EatAction, or CascadeAction), or `None`
        if no solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    


    state_pq = []
    cost_to_state = {make_hashable(board): 0}
    parents = {make_hashable(board): (None, None)}  # Maps state to (parent_state, action_to_get_there)
    heapq.heappush(state_pq, (f_score(board, 0), make_hashable(board)))
    

    while state_pq:
        _, hashable_state = heapq.heappop(state_pq)
        current_state = rev_hashable(hashable_state)

        print(render_board(current_state, ansi=True))
        if is_goal(current_state):
            return #RECONSTRUCT_PATH(parents, current)

       
    #     for each (next_state, cost) in GET_NEIGHBORS(current):

    #         tentative_g = g_scores[current] + cost

    #         if next_state not in g_scores
    #            OR tentative_g < g_scores[next_state]:

    #             g_scores[next_state] = tentative_g
    #             parents[next_state] = current

    #             f_score = tentative_g + heuristic(next_state)
    #             insert or update next_state in open_set with f_score

    # return FAILURE   // no solution found

    
    

    
    return [
        CascadeAction(Coord(3, 3), Direction.Down)
    ]
