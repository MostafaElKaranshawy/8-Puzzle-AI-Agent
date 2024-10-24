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
            print(currentState)
            print(self.goalState)
            print(currentState == self.goalState)
            if currentState == self.goalState:
                return True
            if currentState in self.visited:
                continue
            self.visited.add(currentState)

            children = []
            # Up Child Check and Add
            upChild = self.getUpChild(currentState)
            children.append(upChild)

            # Left Child Check and Add
            leftChild = self.getLeftChild(currentState)
            children.append(leftChild)

            # Down Child Check and Add
            downChild = self.getDownChild(currentState)
            children.append(downChild)

            # Right Child Check and Add
            rightChild = self.getRightChild(currentState)
            children.append(rightChild)

            children = sorted(children, key=lambda x: x[0])
            for child in children:
                # child = [childNumber, childState]
                if child[0] != -1 and child[1] not in self.visited and child[1] not in list(self.queue.queue):
                    self.queue.put(child[1])
                    self.parentMap[child[1]] = currentState

    def getUpChild(self, state):
        strState = str(state)
        if (len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if (zeroIndex < 3):
            return [-1, -1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex - 3])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex - 3]
            stateList[zeroIndex - 3] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]

    def getDownChild(self, state):
        strState = str(state)
        if (len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if (zeroIndex > 5):
            return [-1, -1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex + 3])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex + 3]
            stateList[zeroIndex + 3] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]

    def getLeftChild(self, state):
        strState = str(state)
        if (len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if (zeroIndex % 3 == 0):  # 0, 3, 6
            return [-1, -1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex - 1])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex - 1]
            stateList[zeroIndex - 1] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]

    def getRightChild(self, state):
        strState = str(state)
        if (len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if (zeroIndex % 3 == 2):  # 2, 5, 8
            return [-1, -1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex + 1])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex + 1]
            stateList[zeroIndex + 1] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]

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
        return len(self.visited)

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
