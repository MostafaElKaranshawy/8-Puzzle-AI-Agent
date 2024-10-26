from queue import Queue

class BFS:
    def __init__(self, start_state):
        self.visited = set()
        self.queue = Queue()
        self.goal_state = 12345678
        self.parent_map = {}
        self.start_state = start_state
        self.path = []
        self.path_directions = []

    def solve(self):
        self.queue.put(self.start_state)
        while not self.queue.empty():

            current_state = self.queue.get()
            if current_state == self.goal_state:
                return True

            if current_state in self.visited:
                continue

            self.visited.add(current_state)

            children = self.get_all_children(current_state)
            # children.sort()

            for child in children:
                if child not in self.visited and child not in list(self.queue.queue):
                    self.queue.put(child)
                    self.parent_map[child] = current_state
        return False

    def get_all_children(self, board):
        str_board = str(board)
        if len(str_board) < 9:
            str_board = "0" + str_board
        zero_index = str_board.index('0')
        children = []

        # Up Child
        if zero_index >= 3:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index - 3] = new_board[zero_index - 3], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        # Left Child
        if zero_index % 3 != 0:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index - 1] = new_board[zero_index - 1], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        # Down Child
        if zero_index <= 5:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index + 3] = new_board[zero_index + 3], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        # Right Child
        if zero_index % 3 != 2:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index + 1] = new_board[zero_index + 1], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        return children


    def get_path(self):
        self.path = []
        current_state = self.goal_state
        while current_state in self.parent_map:
            self.path.append(current_state)
            current_state = self.parent_map[current_state]
        self.path.append(current_state)

        self.path.reverse()
        self.path_directions = self.get_path_directions()

        return self.path, self.path_directions

    def get_path_directions(self):
        parent = self.path[0]
        path_directions = []
        for i in range(1, len(self.path)):
            child = self.path[i]
            direction = self.get_direction(parent, child)
            parent = child
            path_directions.append(direction)
        path_directions.append("Goal State Reached!")
        return path_directions

    def get_direction(self, parent, child):
        parent = str(parent)
        if len(parent) < 9:
            parent = '0' + parent
        child = str(child)
        if len(child) < 9:
            child = '0' + child

        zero_diff = child.index('0') - parent.index('0')
        if zero_diff == 3:
            return "DOWN"
        if zero_diff == -3:
            return "UP"
        if zero_diff == 1:
            return "RIGHT"
        if zero_diff == -1:
            return "LEFT"
        return ""

    def get_max_depth(self):
        return len(self.path)-1

    def get_nodes_expanded(self):
        return len(self.visited)+1

    def get_cost_of_path(self):
        return len(self.path)-1

    def get_details(self):
        cost_of_path = self.get_cost_of_path()
        number_of_nodes_expanded = self.get_nodes_expanded()
        search_depth = self.get_max_depth()
        max_search_depth = self.get_max_depth()
        return {
            "Cost of the Path": cost_of_path,
            "Number of Nodes Expanded": number_of_nodes_expanded,
            "Search Depth": search_depth,
            "Max Search Depth": max_search_depth,
        }

# 1 0 3
# 2 4 6
# 5 7 8


start_board = 103246578
BFSMethod = BFS(start_board)

BFSMethod.solve()
path, path_directions = BFSMethod.get_path()

print(path)
print(path_directions)
print(BFSMethod.get_max_depth())
print(BFSMethod.get_nodes_expanded())
print(BFSMethod.get_cost_of_path())