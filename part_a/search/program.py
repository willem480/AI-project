# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction
from .utils import render_board
import heapq

def heuristic(state):
    h2 = 0
    red = [] 
    blue = []
    for coord, cellstate in state.items():
        if(cellstate.color == PlayerColor.Blue): #if color is blue
            blue.append(coord) #take blue

    for coord, cellstate in state:
        if(cellstate.color == PlayerColor.Red):
            red.append(coord)

    if(blue == None):
        return 0
    
    if(red == None):
        return float('inf')
    
    #h1:THe number of blue stacks
    h1 = len(blue)
    #h2: The sum of cloest distance of blue stack to cloest red stack
    for node_blue in blue:
        min = 0
        for node_red in red:
           distance = abs(node_blue.r - node_red.r) + abs(node_blue.c - node_red.c)
           if (min < distance):
               min = distance  
        h2 += min

    w1 = 0.6
    w2 = 0.8

    return  w1 * h1 + w2 * h2# Placeholder, replace with your heuristic calculation

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
    result = []
    # for coord,cellstate in state.items():
    #     if cellstate.color == PlayerColor.RED:
    #         if cellstate.height > 1:
    #             result.append((state, CascadeAction(coord, Direction.Down), 1))
                
    return result

def stack_movement(state, coord, direction):
    new_state = dict(state)
    try:
        target = coord + direction #The red target coord
    
    except ValueError:#out of bound
        return
    

    #MOVE to empty place
    if(target not in new_state):
        new_state[target] = new_state.pop(coord)
        return MoveAction(coord, direction), new_state
    
    #Move to another red stack
    elif(target in new_state and new_state[target].color == PlayerColor.RED):
        new_state[target] = CellState
        (PlayerColor.Red, new_state[target].height + new_state[coord].height)#Pile up
        new_state.pop(coord)

        return MoveAction(coord, direction), new_state
    
    #Eat
    elif(target in new_state and new_state[target].color == PlayerColor.BLUE):
        if(new_state[coord].height >= new_state[target].height):
            new_state[target] = CellState(PlayerColor.RED, new_state[coord].height)#Eat
            new_state.pop(coord)
            return EatAction(coord, direction), new_state
        else:
            return None, None

    return None, None #Red stack cannot make an movement.


def push_stack(newstate, pushcoord, stack, direction):
    try:
        next_coord = pushcoord + direction
    except ValueError:#out of bound
        return

    if next_coord in newstate: #if there is a stack
        push_stack(newstate, next_coord, newstate.pop(next_coord), direction)
    
    newstate[next_coord] = stack #if empty



def stack_cascade(state, coord, direction):
    new_state = dict(state)
    step = new_state[coord].height #How much a red stack can cascade
    prev = new_state.pop(coord) #red stack move one rid forward
    for move in range(1, step + 1):
        try:
            target = Coord(coord.r + direction.r * move, 
                           coord.c + direction.c * move)
        except ValueError: #out of bound
            continue #For red stack game continue

        if target in new_state:
            push_stack(new_state, target, new_state.pop(target), direction)#push engine start

        new_state[target] = CellState(PlayerColor.RED, 1)

        
    return CascadeAction(coord, direction), new_state


    



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
        priority, hashable_state = heapq.heappop(state_pq)

        if priority > cost_to_state[hashable_state]:
            continue  # Skip if we have already found a better path to this state

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
