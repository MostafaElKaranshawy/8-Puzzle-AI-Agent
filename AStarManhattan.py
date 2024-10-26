from queue import PriorityQueue

class AStarManhattan:
    def __init__(self, start_board):
        self.visited = set()
        self.pq = PriorityQueue()
        self.goal_board = 12345678
        self.goal_rows_cols = {
                                '0': (0, 0), '1': (0, 1), '2': (0, 2),
                                '3': (1, 0), '4': (1, 1), '5': (1, 2),
                                '6': (2, 0), '7': (2, 1), '8': (2, 2)
        }
        self.parent_map = {}
        self.start_board = start_board
        self.path = []
        self.path_directions = []


    def a_star_manhattan(self):
        self.pq.put( (self.compute_cost_function(self.start_board, 0), (self.start_board, 0) ))
        while not self.pq.empty():
            current_state = self.pq.get()[1]  # get the state with the lowest cost from priority, state
            current_board = current_state[0]
            current_depth = current_state[1]

            if current_board == self.goal_board:
                return True

            if current_board in self.visited:
                continue

            self.visited.add(current_board)
            children_boards = self.get_all_children(current_board)
            # children_boards.sort()

            for child_board in children_boards:
                if child_board not in self.visited:
                    self.pq.put( (self.compute_cost_function(child_board, current_depth + 1), (child_board, current_depth + 1)) )
                    self.parent_map[child_board] = current_board
        return False


    def compute_cost_function(self, board, depth):
        return self.get_manhattan_distance(board) + depth


    def get_manhattan_distance(self, board):
        str_board = str(board)
        if len(str_board) < 9:
            str_board = "0" + str_board

        distance = 0
        for i in range(0, 9):
            if str_board[i] == '0':
                continue
            goal_row, goal_col = self.goal_rows_cols[str_board[i]]
            row_diff = (i // 3) - goal_row
            col_diff = (i % 3) - goal_col
            distance += ( abs(row_diff) + abs(col_diff) )
        return distance


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
        current_board = self.goal_board
        while current_board in self.parent_map:
            self.path.append(current_board)
            current_board = self.parent_map[current_board]
        self.path.append(current_board)
        
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
        return len(self.path) - 1  # -1 for removing the start node from the path
    
    def get_nodes_expanded(self):
        return len(self.visited) + 1    # +1 for expanding goal node
    
    def get_cost_of_path(self):
        return len(self.path) - 1   # -1 for removing the start node from the path


start_board = 103246578
AStarManhattanMethod = AStarManhattan(start_board)

AStarManhattanMethod.a_star_manhattan()
path, pathDirections = AStarManhattanMethod.get_path()
    
print(path)
print(pathDirections)   
print(AStarManhattanMethod.get_max_depth())
print(AStarManhattanMethod.get_nodes_expanded())
print(AStarManhattanMethod.get_cost_of_path())
# 103246578