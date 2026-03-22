# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

import time

from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor
from .utils import render_board
import heapq

def heuristic(state : dict[Coord, CellState]):
    vectors = [(v.r, v.c) for v in state if state[v].color == PlayerColor.BLUE]
    # The heuristic is the minimum of the number of unique rows and columns that contain blue stacks.
    h = min(len({v[0] for v in vectors}), len({v[1] for v in vectors}))

    return h

def distance(coord1 : Coord, coord2 : Coord):
    return abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)

def f_score(state, g_score):
    return g_score + heuristic(state)

def make_hashable(state : dict[Coord, CellState]):
    # Convert the state dictionary to a frozenset of items for hashing
    return tuple(sorted((i, j) for i, j in state.items()))

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
    for coord, cellstate in state.items():
        if(cellstate.color == PlayerColor.RED): #Must be red
            for direction in Direction:
                action, new_state = stack_movement(state, coord, direction)
                if (action is not None):
                    result.append((action, new_state))
                
                if (cellstate.height > 1): 
                    action, new_state = stack_cascade(state, coord, direction)
                    if(action is not None):
                        result.append((action, new_state))
                    
    return result
                    


def stack_movement(state, coord, direction):
    new_state = dict(state)
    try:
        target = coord + direction #The red target coord
    
    except ValueError:#out of bound
        return None, None
    

    #MOVE to empty place
    if(target not in new_state):
        new_state[target] = new_state.pop(coord)
        return MoveAction(coord, direction), new_state
    
    #Move to another red stack
    elif(target in new_state and new_state[target].color == PlayerColor.RED):
        new_state[target] = CellState(
            PlayerColor.RED, new_state[target].height + new_state[coord].height
            )#Pile up
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

    return None, None #RED stack cannot make an movement.


def push_stack(newstate, pushcoord, stack, direction):
    try:
        next_coord = pushcoord + direction
    except ValueError:#out of bound
        return None, None

    if next_coord in newstate: #if there is a stack
        push_stack(newstate, next_coord, newstate.pop(next_coord), direction)
    
    newstate[next_coord] = stack #if empty

def stack_cascade(state, coord, direction):
    new_state = dict(state)
    step = new_state[coord].height #How much a red stack can cascade

    if step <= 1: return None, None

    new_state.pop(coord)

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

def reconstruct_path(parents, current, path):
    if parents[current][0] is None:
        return path
    path.append(parents[current][1])
    return reconstruct_path(parents, parents[current][0], path)


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
    exe_time = time.time()
    state_pq = []
    path = []
    cost_to_state = {make_hashable(board): 0}
    parents = {make_hashable(board): (None, None)}  # Maps state to (parent_state, action_to_get_there)
    index = 0
    heapq.heappush(state_pq, (f_score(board, 0), index, make_hashable(board)))
    print(render_board(board, ansi= True))
    
    while state_pq:
        priority, _, cur_hashable_state = heapq.heappop(state_pq)
        cur_state = rev_hashable(cur_hashable_state)

        if priority > cost_to_state[cur_hashable_state] + heuristic(cur_state):
            continue  # Skip if we have already found a better path to this state

        

        if is_goal(cur_state):
            print(f"number of states explored: {len(parents)}")
            print(f"Execution time: {time.time() - exe_time:.2f} seconds")
            return reconstruct_path(parents, cur_hashable_state, path)[::-1] # Reverse the path to get the correct order from start to goal
        
        for action, next_state in get_next_states(cur_state):
            hashable_next_state = make_hashable(next_state)
            cost_to_next = cost_to_state[cur_hashable_state] + 1
            # if the next state has not been explored or we found a cheaper path to it 
            # update the cost and parent information and add it to the priority queue
            if (hashable_next_state not in cost_to_state) or (cost_to_next < cost_to_state[hashable_next_state]):
                cost_to_state[hashable_next_state] = cost_to_next
                parents[hashable_next_state] = (cur_hashable_state, action)
                index +=1
                heapq.heappush(state_pq, (f_score(next_state, cost_to_state[hashable_next_state]), index, hashable_next_state))
    print("No solution found.")
    print(f"number of states explored: {len(cost_to_state)}")
    print(f"Execution time: {time.time() - exe_time:.2f} seconds")
    return 