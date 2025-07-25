class Node:
    def __init__(self, state, parent=None, move=""):
        self.state = state
        self.parent = parent
        self.move = move

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

def isSafe(state):
    return True

def goalTest(currentState, goalState):
    return currentState == goalState

def moveGen(node):
    children = []
    state = node.state
    empty = -1
    try:
        empty = state.index('_')
    except ValueError:
        return []

    for i, rabbit in enumerate(state):
        if rabbit == 'E':
            if i + 1 == empty or i + 2 == empty:
                newState = list(state)
                newState[i], newState[empty] = newState[empty], newState[i]
                if isSafe(newState):
                    children.append(Node(newState, node, f"E from {i} to {empty}"))
        elif rabbit == 'W':
            if i - 1 == empty or i - 2 == empty:
                newState = list(state)
                newState[i], newState[empty] = newState[empty], newState[i]
                if isSafe(newState):
                    children.append(Node(newState, node, f"W from {i} to {empty}"))
    return children

def reconstructPath(node):
    path = []
    while node:
        path.insert(0, (node.state, node.move))
        node = node.parent
    return path

def bfs(initial_state, goal_state):
    queue = [Node(initial_state)]
    visited = {tuple(initial_state)}

    while queue:
        currentNode = queue.pop(0)

        if goalTest(currentNode.state, goal_state):
            return reconstructPath(currentNode)

        children = moveGen(currentNode)
        for child in children:
            if tuple(child.state) not in visited:
                visited.add(tuple(child.state))
                queue.append(child)

    return None

def dfs(initial_state, goal_state):
    stack = [Node(initial_state)]
    visited = {tuple(initial_state)}

    while stack:
        currentNode = stack.pop()

        if goalTest(currentNode.state, goal_state):
            return reconstructPath(currentNode)

        children = moveGen(currentNode)
        for child in reversed(children):
            if tuple(child.state) not in visited:
                visited.add(tuple(child.state))
                stack.append(child)

    return None

if __name__ == "__main__":
    initial = ['E', 'E', 'E', '_', 'W', 'W', 'W']
    goal = ['W', 'W', 'W', '_', 'E', 'E', 'E']

    print(" Breadth-First Search (BFS)")
    print(f"Initial State: {' '.join(initial)}")
    print(f"Goal State:    {' '.join(goal)}\n")

    bfs_path = bfs(initial, goal)

    if bfs_path:
        print(f"BFS Solution Found in {len(bfs_path) - 1} steps:")
        for i, (state, move) in enumerate(bfs_path):
            print(f"Step {i:02d}: {' '.join(state)}  (Move: {move})")
    else:
        print("BFS could not find a solution.")


    print("Depth-First Search (DFS)")
    print(f"Initial State: {' '.join(initial)}")
    print(f"Goal State:    {' '.join(goal)}\n")
    
    dfs_path = dfs(initial, goal)

    if dfs_path:
        print(f"DFS Solution Found in {len(dfs_path) - 1} steps:")
        for i, (state, move) in enumerate(dfs_path):
            print(f"Step {i:02d}: {' '.join(state)}  (Move: {move})")
    else:
        print("DFS could not find a solution.")