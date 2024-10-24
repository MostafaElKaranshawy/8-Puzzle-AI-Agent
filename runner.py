from bfs import BFS
import time
import tkinter as tk
from tkinter import ttk, messagebox


# Sample 8-puzzle solver methods (replace with actual algorithm implementations)
def solve8Puzzle(method, initialState):
    # Replace with the actual puzzle solving logic
    # This is a placeholder for the sequence of states leading to the solution.
    if method == "BFS":
        bfs = BFS(initialState)
        startTime = time.time()
        bfs.solve()
        endTime = time.time()
        path, pathDirections = bfs.getPath()
        details = bfs.getDetails()
        details["Running Time"] = endTime - startTime
        return [path, pathDirections], details
    else:
        return None, None


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver")
        self.root.configure(bg='black')

        self.solution = []
        self.currentStep = -1
        self.gridCells = []
        self.details = {
            "Cost of the Path": 0,
            "Number of Nodes Expanded": 0,
            "Search Depth": 0,
            "Max Search Depth": 0,
            "Running Time": 0
        }

        # Dropdown for selecting solving method
        # Frame for the method selection
        methodFrame = tk.Frame(root, bg='black')
        methodFrame.pack(pady=10)  # Add some vertical spacing

        self.methodLabel = tk.Label(methodFrame, text="Select Method:", bg='black', fg='white')
        self.methodLabel.pack(side=tk.LEFT)

        self.methodVar = tk.StringVar()
        self.methodDropdown = ttk.Combobox(methodFrame, textvariable=self.methodVar)
        self.methodDropdown['values'] = ["BFS", "DFS", "IDS", "A*"]  # Add more methods as needed
        self.methodDropdown.current(0)
        self.methodDropdown.pack(side=tk.LEFT)  # Pack it next to the label

        # Frame for the initial state input
        initialStateFrame = tk.Frame(root, bg='black')
        initialStateFrame.pack(pady=10)  # Add some vertical spacing

        self.initialStateLabel = tk.Label(initialStateFrame, text="Enter Initial State as 012345678", bg='black', fg='white')
        self.initialStateLabel.pack(side=tk.LEFT)

        self.initialStateEntry = tk.Entry(initialStateFrame)
        self.initialStateEntry.pack(side=tk.LEFT)  # Pack it next to the label


        # Frame for buttons
        buttonFrame = tk.Frame(root, bg='black')
        buttonFrame.pack(pady=20)

        # Show Game button
        self.showGameButton = tk.Button(buttonFrame, text="Show Game", command=self.showGame, bg='black', fg='white')
        self.showGameButton.pack(side=tk.LEFT, padx=10)  # Add some padding to the left and right

        # Start solving button
        self.solveButton = tk.Button(buttonFrame, text="Start Solving", command=self.startSolving, bg='black', fg='white')
        self.solveButton.pack(side=tk.LEFT, padx=10)  # Add some padding to the left and right

        # State label
        self.stateLabel = tk.Label(root, text="Initial State", bg='black', fg='white', font=("Helvetica", 16))
        self.stateLabel.pack(pady=10)

        # Grid display area
        self.gridFrame = tk.Frame(root, bg='black')
        self.gridFrame.pack()

        # Create a 3x3 grid for the puzzle
        for row in range(3):
            rowCells = []
            for col in range(3):
                label = tk.Label(self.gridFrame, text="", font=("Helvetica", 32), width=4, height=2, bg='white')
                label.grid(row=row, column=col, padx=5, pady=5)
                rowCells.append(label)
            self.gridCells.append(rowCells)

        # Navigation buttons
        self.prevButton = tk.Button(root, text="Prev", command=self.prevStep, state=tk.DISABLED, bg='black',
                                     fg='white')
        self.prevButton.pack(side=tk.LEFT, padx=20)

        self.nextButton = tk.Button(root, text="Next", command=self.nextStep, state=tk.DISABLED, bg='black',
                                     fg='white')
        self.nextButton.pack(side=tk.LEFT, padx=20)

        # Show solution details button
        self.detailsButton = tk.Button(root, text="Show Solution Details", state=tk.DISABLED, command=self.showDetails, bg='black',
                                        fg='white')
        self.detailsButton.pack(pady=20)

    def parseInitialState(self):
        try:
            inputValues = self.initialStateEntry.get()  # Get input and strip whitespace
            strInput = str(inputValues)

            # Validations
            if len(strInput) < 9:
                strInput = '0' + strInput

            if len(strInput) != 9:
                raise ValueError("Input must be exactly 9 characters long.")

            if not strInput.isdigit():
                raise ValueError("Input must contain only digits.")

            digitSet = set(strInput)
            if digitSet != set("012345678"):
                raise ValueError("Input must contain all digits from 0 to 8 exactly once.")

            return int(inputValues)

        except ValueError as e:
            print(e)
            messagebox.showerror("Error", f"Invalid input: {e}")
            return None

    def showGame(self):
        initialState = self.parseInitialState()
        if not initialState:
            return

        initialState = str(initialState)
        if len(initialState) < 9:
            initialState = '0' + initialState
        initialState = [initialState[i:i + 3] for i in range(0, 9, 3)]

        for row in range(3):
            for col in range(3):
                value = initialState[row][col]
                if value == '0':
                    print("yessss")
                    self.gridCells[row][col].config(text="", bg='lightBlue')
                else:
                    self.gridCells[row][col].config(text=str(value), bg='white')
    
    def startSolving(self):
        self.solution = []
        self.details = []

        initialState = self.parseInitialState()
        if not initialState:
            return

        self.solveButton['state'] = tk.DISABLED
        self.showGameButton['state'] = tk.DISABLED
        self.showGame()

        method = self.methodVar.get()

        self.solution, self.details = solve8Puzzle(method, initialState)

        self.solveButton['state'] = tk.NORMAL
        self.showGameButton['state'] = tk.NORMAL
        if not self.solution:
            messagebox.showerror("Error", "No solution found!")
            return

        self.currentStep = 0
        self.updateGridDisplay()
        self.prevButton['state'] = tk.DISABLED
        self.nextButton['state'] = tk.NORMAL
        self.detailsButton['state'] = tk.NORMAL
        if self.currentStep == len(self.solution[0]) - 1:
            self.nextButton['state'] = tk.DISABLED

    def updateGridDisplay(self):
        # solution = [path, pathDirections]
        if self.solution:
            currentState = str(self.solution[0][self.currentStep])
            nextStep = self.solution[1][self.currentStep]
            if nextStep != "Goal State Reached!":
                nextStep = "Next Step is: " + nextStep

            self.stateLabel.config(text=nextStep)
            if len(currentState) < 9:
                currentState = '0' + currentState
            currentState = [currentState[i:i + 3] for i in range(0, 9, 3)]
            for row in range(3):
                for col in range(3):
                    value = currentState[row][col]
                    if value == '0':
                        self.gridCells[row][col].config(text="", bg='lightBlue')
                    else:
                        self.gridCells[row][col].config(text=str(value), bg='white')

    def nextStep(self):
        if self.currentStep < len(self.solution[0]) - 1:
            self.currentStep += 1
            self.updateGridDisplay()
            self.prevButton['state'] = tk.NORMAL
        if self.currentStep == len(self.solution[0]) - 1:
            self.nextButton['state'] = tk.DISABLED

    def prevStep(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateGridDisplay()
            self.nextButton['state'] = tk.NORMAL
        if self.currentStep == 0:
            self.prevButton['state'] = tk.DISABLED

    def showDetails(self):
        if self.details:
            details = "\n".join([f"{key}: {value}" for key, value in self.details.items()])
            messagebox.showinfo("Solution Details", details)
        else:
            messagebox.showinfo("Solution Details", "No solution available.")


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
