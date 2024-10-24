from queue import Queue


class BFS:
    def __init__(self, startState):
        self.visited = set()
        self.queue = Queue()
        self.goalState = 12345678
        self.parentMap = {}
        self.startState = startState
        self.path = []
        self.pathDirections = []

    def solve(self):
        self.queue.put(self.startState)
        while (self.queue.qsize() > 0):
            currentState = self.queue.get()
            if currentState == self.goalState:
                return True
            if currentState in self.visited:
                continue
            self.visited.add(currentState)

            children = self.getAllChildren(currentState)
            children.sort()

            for child in children:
                if child not in self.visited and child not in list(self.queue.queue):
                    self.queue.put(child)
                    self.parentMap[child] = currentState
        return False

    def getAllChildren(self, board):
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

        # Down Child
        if zero_index <= 5:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index + 3] = new_board[zero_index + 3], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        # Left Child
        if zero_index % 3 != 0:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index - 1] = new_board[zero_index - 1], new_board[zero_index]
            children.append( int(''.join(new_board)) )

        # Right Child
        if zero_index % 3 != 2:
            new_board = list(str_board)
            new_board[zero_index], new_board[zero_index + 1] = new_board[zero_index + 1], new_board[zero_index]
            children.append(  int(''.join(new_board)))

        return children

    def getPath(self):
        self.path = []
        currentState = self.goalState
        previosState = currentState
        while currentState in self.parentMap:
            self.path.append(currentState)
            currentState = self.parentMap[currentState]
        self.path.append(currentState)

        self.path.reverse()
        self.pathDirections = self.getPathDirections()

        return self.path, self.pathDirections

    def getPathDirections(self):
        parent = self.path[0]
        pathDirections = []
        for i in range(1, len(self.path)):
            child = self.path[i]
            direction = self.getDirection(parent, child)
            parent = child
            pathDirections.append(direction)
        pathDirections.append("Goal State Reached!")
        return pathDirections

    def getDirection(self, parent, child):
        parent = str(parent)
        if (len(parent) < 9):
            parent = '0' + parent
        child = str(child)
        if (len(child) < 9):
            child = '0' + child

        zeroDiff = child.index('0') - parent.index('0')
        if zeroDiff == 3:
            return "DOWN"
        if zeroDiff == -3:
            return "UP"
        if zeroDiff == 1:
            return "RIGHT"
        if zeroDiff == -1:
            return "LEFT"
        return ""

    def getMaxDepth(self):
        return len(self.path)-1

    def getNodesExpanded(self):
        return len(self.visited)+1

    def getCostOfPath(self):
        return len(self.path)-1

    def getDetails(self):
        costOfPath = self.getCostOfPath()
        numberOfNodesExpanded = self.getNodesExpanded()
        searchDepth = self.getMaxDepth()
        maxSearchDepth = self.getMaxDepth()
        return {
            "Cost of the Path": costOfPath,
            "Number of Nodes Expanded": numberOfNodesExpanded,
            "Search Depth": searchDepth,
            "Max Search Depth": maxSearchDepth,
        }
