"""
    0 1 2
    3 4 5
    6 7 8
"""
class DFS:
    def __init__(self, startState):
        self.visited = set()
        self.stack = []
        self.goalState = 12345678
        self.parentMap = {}
        self.startState = startState
        print(startState)
    
    def dfs(self):
        self.stack.append(self.startState)
        while(len(self.stack) > 0):
            currentState = self.stack.pop()
            if(currentState == self.goalState):
                return True
            if(currentState in self.visited):
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
            
            children = sorted(children, key=lambda x: x[0], reverse=True)
            for child in children:
                # child = [childNumber, childState]
                # if child[0] != -1 and child[1] not in self.visited and child[1] not in self.stack:
                if child[0] != -1 and child[1] not in self.visited:
                    self.stack.append(child[1])
                    self.parentMap[child[1]] = currentState
    
    def getUpChild(self,state):
        strState = str(state)
        if(len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if(zeroIndex < 3):
            return [-1,-1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex-3])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex-3]
            stateList[zeroIndex-3] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]
    
    def getDownChild(self,state):
        strState = str(state)
        if(len(strState)< 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if(zeroIndex > 5):
            return [-1,-1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex+3])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex+3]
            stateList[zeroIndex+3] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]
    
    def getLeftChild(self, state):
        strState = str(state)
        if(len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')        
        if(zeroIndex % 3 == 0):     # 0, 3, 6
            return [-1,-1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex-1])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex-1]
            stateList[zeroIndex-1] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]
    
    def getRightChild(self, state):
        strState = str(state)
        if(len(strState) < 9):
            strState = "0" + strState
        zeroIndex = strState.index('0')
        if(zeroIndex % 3 == 2):     # 2, 5, 8
            return [-1,-1]
        else:
            newState = strState
            childNumber = int(newState[zeroIndex+1])
            stateList = list(newState)
            stateList[zeroIndex] = stateList[zeroIndex+1]
            stateList[zeroIndex+1] = '0'
            newState = ''.join(stateList)
            return [childNumber, int(newState)]
    
    def getPath(self):
        path = []
        currentState = self.goalState
        while currentState in self.parentMap:
            path.append(currentState)
            currentState = self.parentMap[currentState]
        path.append(currentState)
        path.reverse()
        return path
    

"""
    1 2 5
    3 4 0
    6 7 8
"""
def printGame(state):
    state = str(state)
    if(len(state) < 9):
        state = '0' + state
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()
startState = 125340678
dfsMethod = DFS(startState)

dfsMethod.dfs()
path = dfsMethod.getPath()
# print(path)
for state in path:
    printGame(state)

