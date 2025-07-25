class Node:
    def __init__(self, time, left_side, umbrella_start, parent=None, move=""):
        self.time = time
        self.left_side = left_side
        self.umbrella_start = umbrella_start
        self.parent = parent
        self.move = move

    def __lt__(self, other):
        return self.time < other.time

    def get_key(self):
        return (self.left_side, self.umbrella_start)

def reconstructPath(node):
    path = []
    while node:
        path.insert(0, (node.time, node.move, node.left_side))
        node = node.parent
    return path

def goalTest(node, limit):
    return not node.left_side and node.time <= limit

def isSafe(node, limit):
    return node.time <= limit

def removeSeen(nodes, visited_costs):
    unseen = []
    for node in nodes:
        key = node.get_key()
        if key not in visited_costs or node.time < visited_costs[key]:
            unseen.append(node)
    return unseen

def moveGen(node, everyone, crossing_times):
    next_nodes = []
    ctime = node.time
    cpeople = node.left_side

    if node.umbrella_start:
        people_list = sorted(list(cpeople))
        for i in range(len(people_list)):
            group = (people_list[i],)
            move_time = max(crossing_times[person] for person in group)
            new_time = ctime + move_time
            new_people = cpeople - set(group)
            move_desc = f"{' and '.join(sorted(list(group)))} cross to end"
            next_nodes.append(Node(new_time, frozenset(new_people), False, node, move_desc))
        for i in range(len(people_list)):
            for j in range(i + 1, len(people_list)):
                group = (people_list[i], people_list[j])
                move_time = max(crossing_times[person] for person in group)
                new_time = ctime + move_time
                new_people = cpeople - set(group)
                move_desc = f"{' and '.join(sorted(list(group)))} cross to end"
                next_nodes.append(Node(new_time, frozenset(new_people), False, node, move_desc))

    else:
        people_at_end = everyone - cpeople
        for person in people_at_end:
            move_time = crossing_times[person]
            new_time = ctime + move_time
            new_people = cpeople | {person}
            move_desc = f"{person} returns to start"
            next_nodes.append(Node(new_time, frozenset(new_people), True, node, move_desc))
            
    return next_nodes

def solve_puzzle(crossing_times, time_allowed):
    everyone = frozenset(crossing_times.keys())
    
    nodes_to_visit = [Node(0, everyone, True, move="Initial State")]
    
    visited_costs = {}

    while nodes_to_visit:
        nodes_to_visit.sort()
        current = nodes_to_visit.pop(0)

        key = current.get_key()
        if key in visited_costs and visited_costs[key] <= current.time:
            continue
        
        visited_costs[key] = current.time

        if goalTest(current, time_allowed):
            return reconstructPath(current)

        children = moveGen(current, everyone, crossing_times)
        safe_children = [child for child in children if isSafe(child, time_allowed)]
        
        for child in safe_children:
            nodes_to_visit.append(child)
            
    return None

if __name__ == "__main__":
    person_times = {
        'Amogh': 5,
        'Ameya': 10,
        'Grandmother': 20,
        'Grandfather': 25,
    }
    time_limit = 60

    print("Solving the Bridge Crossing Problem")
    print(f"Time Limit: {time_limit} minutes\n")

    final_path = solve_puzzle(person_times, time_limit)

    if final_path:
        print(f"Solution found in {final_path[-1][0]} minutes!")
        for time, move, start_people in final_path:
            end_people = sorted(list(set(person_times.keys()) - start_people))
            print(f"Time: {time:2d} | Start Side: {sorted(list(start_people)) if start_people else '[]'} | End Side: {end_people}")
    else:
        print("Could not find a solution within the time.")