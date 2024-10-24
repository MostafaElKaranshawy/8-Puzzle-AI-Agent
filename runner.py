from bfs import BFS
import time
import tkinter as tk
from tkinter import ttk, messagebox


# Sample 8-puzzle solver methods (replace with actual algorithm implementations)
def solve_8_puzzle(method, initial_state):
    # Replace with the actual puzzle solving logic
    # This is a placeholder for the sequence of states leading to the solution.
    if method == "BFS":
        bfs = BFS(initial_state)
        start_time = time.time()
        bfs.solve()
        end_time = time.time()
        path, pathDirections = bfs.getPath()
        details = bfs.getDetails()
        details["running_time"] = end_time - start_time
        return [path, pathDirections], details
    else:
        return None, None


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver")
        self.root.configure(bg='black')

        self.solution = []
        self.current_step = -1
        self.grid_cells = []
        self.details = {
            "Cost of the Path": 0,
            "Number of Nodes Expanded": 0,
            "Search Depth": 0,
            "Max Search Depth": 0,
            "running_time": 0
        }
        # Dropdown for selecting solving method
        # Frame for the method selection
        method_frame = tk.Frame(root, bg='black')
        method_frame.pack(pady=10)  # Add some vertical spacing

        self.method_label = tk.Label(method_frame, text="Select Method:", bg='black', fg='white')
        self.method_label.pack(side=tk.LEFT)

        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(method_frame, textvariable=self.method_var)
        self.method_dropdown['values'] = ["BFS", "DFS", "IDS", "A*"]  # Add more methods as needed
        self.method_dropdown.current(0)
        self.method_dropdown.pack(side=tk.LEFT)  # Pack it next to the label

        # Frame for the initial state input
        initial_state_frame = tk.Frame(root, bg='black')
        initial_state_frame.pack(pady=10)  # Add some vertical spacing

        self.initial_state_label = tk.Label(initial_state_frame, text="Enter Initial State as 012345678", bg='black', fg='white')
        self.initial_state_label.pack(side=tk.LEFT)

        self.initial_state_entry = tk.Entry(initial_state_frame)
        self.initial_state_entry.pack(side=tk.LEFT)  # Pack it next to the label


# Frame for buttons
        button_frame = tk.Frame(root, bg='black')
        button_frame.pack(pady=20)

        # Show Game button
        self.showGame = tk.Button(button_frame, text="Show Game", command=self.showGame, bg='black', fg='white')
        self.showGame.pack(side=tk.LEFT, padx=10)  # Add some padding to the left and right

        # Start solving button
        self.solve_button = tk.Button(button_frame, text="Start Solving", command=self.start_solving, bg='black', fg='white')
        self.solve_button.pack(side=tk.LEFT, padx=10)  # Add some padding to the left and right

        # State label
        self.state_label = tk.Label(root, text="Initial State", bg='black', fg='white', font=("Helvetica", 16))
        self.state_label.pack(pady=10)

        # Grid display area
        self.grid_frame = tk.Frame(root, bg='black')
        self.grid_frame.pack()

        # Create a 3x3 grid for the puzzle
        for row in range(3):
            row_cells = []
            for col in range(3):
                label = tk.Label(self.grid_frame, text="", font=("Helvetica", 32), width=4, height=2, bg='white')
                label.grid(row=row, column=col, padx=5, pady=5)
                row_cells.append(label)
            self.grid_cells.append(row_cells)

        # Navigation buttons
        self.prev_button = tk.Button(root, text="Prev", command=self.prev_step, state=tk.DISABLED, bg='black',
                                     fg='white')
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_step, state=tk.DISABLED, bg='black',
                                     fg='white')
        self.next_button.pack(side=tk.LEFT, padx=20)

        # Show solution details button
        self.details_button = tk.Button(root, text="Show Solution Details", state=tk.DISABLED, command=self.show_details, bg='black',
                                        fg='white')
        self.details_button.pack(pady=20)

    def parse_initial_state(self):
        """Parses the initial state input from the user into a 2D list."""
        try:
            input_values = self.initial_state_entry.get()  # Get input and strip whitespace
            strInput = str(input_values)

            # Validations
            if len(strInput) < 9:
                strInput = '0' + strInput

            if len(strInput) != 9:
                raise ValueError("Input must be exactly 9 characters long.")

            if not strInput.isdigit():
                raise ValueError("Input must contain only digits.")

            digit_set = set(strInput)
            if digit_set != set("012345678"):
                raise ValueError("Input must contain all digits from 0 to 8 exactly once.")

            return int(input_values)

        except ValueError as e:
            print(e)
            messagebox.showerror("Error", f"Invalid input: {e}")
            return None


    def showGame(self):
        initial_state = self.parse_initial_state()
        if not initial_state:
            return
        initial_state = str(initial_state)
        if len(initial_state) < 9:
            initial_state = '0' + initial_state
        initial_state = [initial_state[i:i + 3] for i in range(0, 9, 3)]
        for row in range(3):
            for col in range(3):
                value = initial_state[row][col]
                self.grid_cells[row][col].config(text=str(value) if value != 0 else "")
    def start_solving(self):
        initial_state = self.parse_initial_state()
        if not initial_state:
            return
        method = self.method_var.get()
        self.solution, self.details = solve_8_puzzle(method, initial_state)
        if not self.solution:
            messagebox.showerror("Error", "No solution found!")
            return

        self.current_step = 0
        self.update_grid_display()
        self.prev_button['state'] = tk.DISABLED
        self.next_button['state'] = tk.NORMAL
        self.details_button['state'] = tk.NORMAL

    def update_grid_display(self):
        # solution = [path, pathDirections]
        if self.solution:
            current_state = str(self.solution[0][self.current_step])
            nextStep = self.solution[1][self.current_step]
            if nextStep != "Goal State Reached!":
                nextStep = "Next Step is: " + nextStep

            self.state_label.config(text=nextStep)
            if len(current_state) < 9:
                current_state = '0' + current_state
            current_state = [current_state[i:i + 3] for i in range(0, 9, 3)]
            for row in range(3):
                for col in range(3):
                    value = current_state[row][col]
                    self.grid_cells[row][col].config(text=str(value) if value != 0 else "")

    def next_step(self):
        if self.current_step < len(self.solution[0]) - 1:
            self.current_step += 1
            self.update_grid_display()
            self.prev_button['state'] = tk.NORMAL
        if self.current_step == len(self.solution[0]) - 1:
            self.next_button['state'] = tk.DISABLED

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_grid_display()
            self.next_button['state'] = tk.NORMAL
        if self.current_step == 0:
            self.prev_button['state'] = tk.DISABLED

    def show_details(self):
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
