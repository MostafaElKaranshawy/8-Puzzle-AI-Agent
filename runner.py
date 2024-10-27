from bfs import BFS
from dfs import DFS
from ids import IDS
from AStarEuclidean import AStarEuclidean
from AStarManhattan import AStarManhattan

import time
import tkinter as tk
from tkinter import ttk, messagebox


# Methods handler
def solve_8Puzzle(method, initial_state):
    if method == "BFS":
        bfs = BFS(initial_state)
        start_time = time.time()
        bfs.bfs()
        end_time = time.time()
        path, path_directions = bfs.get_path()
        details = bfs.get_details()
        details["Running Time"] = end_time - start_time
        return [path, path_directions], details
    elif method == "DFS":
        dfs = DFS(initial_state)
        start_time = time.time()
        dfs.dfs()
        end_time = time.time()
        path, path_directions = dfs.get_path()
        details = dfs.get_details()
        details["Running Time"] = end_time - start_time
        return [path, path_directions], details
    elif method == "IDS":
        ids = IDS(initial_state)
        start_time = time.time()
        ids.ids()
        end_time = time.time()
        path, path_directions = ids.get_path()
        details = ids.get_details()
        details["Running Time"] = end_time - start_time
        return [path, path_directions], details
    elif method == "A* Euclidean":
        a_star_euclidean = AStarEuclidean(initial_state)
        start_time = time.time()
        a_star_euclidean.a_star_euclidean()
        end_time = time.time()
        path, path_directions = a_star_euclidean.get_path()
        details = a_star_euclidean.get_details()
        details["Running Time"] = end_time - start_time
        return [path, path_directions], details
    elif method == "A* Manhattan":
        a_star_manhattan = AStarManhattan(initial_state)
        start_time = time.time()
        a_star_manhattan.a_star_manhattan()
        end_time = time.time()
        path, path_directions = a_star_manhattan.get_path()
        details = a_star_manhattan.get_details()
        details["Running Time"] = end_time - start_time
        return [path, path_directions], details
    else:
        return None, None


# Game GUI runner class
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
            "Max Search Depth": 0,
            "Running Time": 0
        }

        # Dropdown for selecting solving method
        # Frame for the method selection
        method_frame = tk.Frame(root, bg='black')
        method_frame.pack(pady=10)  # Add some vertical spacing

        self.method_label = tk.Label(method_frame, text="Select Method:", bg='black', fg='white')
        self.method_label.pack(side=tk.LEFT)

        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(method_frame, textvariable=self.method_var)
        self.method_dropdown['values'] = ["BFS", "DFS", "IDS", "A* Euclidean", "A* Manhattan"]
        self.method_dropdown.current(0)
        self.method_dropdown.pack(side=tk.LEFT)  # Pack it next to the label

        # Frame for the initial state input
        initial_state_frame = tk.Frame(root, bg='black')
        initial_state_frame.pack(pady=10)  # Add some vertical spacing

        self.initial_state_label = tk.Label(initial_state_frame, text="Enter Initial State as 012345678", bg='black',
                                            fg='white')
        self.initial_state_label.pack(side=tk.LEFT)

        self.initial_state_entry = tk.Entry(initial_state_frame)
        self.initial_state_entry.pack(side=tk.LEFT)  # Pack it next to the label

        # Frame for buttons
        button_frame = tk.Frame(root, bg='black')
        button_frame.pack(pady=20)

        # Show Game button
        self.show_game_button = tk.Button(button_frame, text="Show Game", command=self.show_game, bg='black',
                                          fg='white')
        self.show_game_button.pack(side=tk.LEFT, padx=10)  # Add some padding to the left and right

        # Start solving button
        self.solve_button = tk.Button(button_frame, text="Start Solving", command=self.handle_solving, bg='black',
                                      fg='white')
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

        self.goal_button = tk.Button(root, text="Goal State", command=self.show_goal, state=tk.DISABLED, bg='black',
                                     fg='white')
        self.goal_button.pack(side=tk.LEFT, padx=20)

        # Solution details button
        self.details_button = tk.Button(root, text="Show Solution Details", state=tk.DISABLED,
                                        command=self.show_details,
                                        bg='black',
                                        fg='white')
        self.details_button.pack(pady=20)

    def parse_initial_state(self):
        try:
            input_values = self.initial_state_entry.get()  # Get input and strip whitespace
            str_input = str(input_values)

            # Input Validations
            if len(str_input) < 9:
                str_input = '0' + str_input

            if len(str_input) != 9:
                raise ValueError("Input must be exactly 9 characters long.")

            if not str_input.isdigit():
                raise ValueError("Input must contain only digits.")

            digit_set = set(str_input)
            if digit_set != set("012345678"):
                raise ValueError("Input must contain all digits from 0 to 8 exactly once.")

            return int(input_values)

        except ValueError as e:
            print(e)
            messagebox.showerror("Error", f"Invalid input: {e}")
            return None

    # Display the initial state of the puzzle
    def show_game(self):
        initial_state = self.parse_initial_state()
        if not initial_state:
            return
        self.solution = []
        self.details = []
        self.current_step = -1
        self.prev_button['state'] = tk.DISABLED
        self.next_button['state'] = tk.DISABLED
        self.goal_button['state'] = tk.DISABLED
        self.details_button['state'] = tk.DISABLED

        initial_state = str(initial_state)
        if len(initial_state) < 9:
            initial_state = '0' + initial_state
        initial_state = [initial_state[i:i + 3] for i in range(0, 9, 3)]

        for row in range(3):
            for col in range(3):
                value = initial_state[row][col]
                if value == '0':
                    self.grid_cells[row][col].config(text="", bg='lightBlue')
                else:
                    self.grid_cells[row][col].config(text=str(value), bg='white')

    # Handle the solving process, reset previous solutions and details
    def handle_solving(self):
        self.solution = []
        self.details = []
        self.current_step = -1
        self.prev_button['state'] = tk.DISABLED
        self.next_button['state'] = tk.DISABLED
        self.goal_button['state'] = tk.DISABLED
        self.details_button['state'] = tk.DISABLED
        self.show_game_button['state'] = tk.DISABLED
        self.show_game()
        initial_state = self.parse_initial_state()
        if not initial_state:
            return
        if not self.check_solvable(initial_state):
            messagebox.showerror("Error", "Puzzle is not solvable!")
            self.show_game_button['state'] = tk.NORMAL
            return
        method = self.method_var.get()
        if method is None:
            messagebox.showerror("Error", "You should select a method first!")
            return
        self.start_solving(method, initial_state)

    # Start solving the puzzle
    def start_solving(self, method=None, initial_state=None):
        # Check for the method and initial state inputs
        if method is None:
            messagebox.showerror("Error", "You should select a method first!")
            return
        if initial_state is None:
            messagebox.showerror("Error", "You should enter an initial state first!")
            return

        # Solve the puzzle
        self.solution, self.details = solve_8Puzzle(method, initial_state)

        self.solve_button['state'] = tk.NORMAL
        self.show_game_button['state'] = tk.NORMAL

        # No solution found or an error occurred
        if not self.solution:
            messagebox.showerror("Error", "No solution found!")
            return

        # Solution found
        self.current_step = 0
        self.update_grid_display()
        self.prev_button['state'] = tk.DISABLED
        self.next_button['state'] = tk.NORMAL
        self.goal_button['state'] = tk.NORMAL
        self.details_button['state'] = tk.NORMAL
        if self.current_step == len(self.solution[0]) - 1:
            self.next_button['state'] = tk.DISABLED

    # Update the grid display with the current state
    def update_grid_display(self):
        # solution is [path, path_directions]
        if self.solution:
            current_state = str(self.solution[0][self.current_step])
            next_step = self.solution[1][self.current_step]
            if next_step != "Goal State Reached!":
                next_step = "Next Step is: " + next_step

            self.state_label.config(text=next_step)
            if len(current_state) < 9:
                current_state = '0' + current_state
            current_state = [current_state[i:i + 3] for i in range(0, 9, 3)]

            # update the grid display
            for row in range(3):
                for col in range(3):
                    value = current_state[row][col]
                    if value == '0':
                        self.grid_cells[row][col].config(text="", bg='lightBlue')
                    else:
                        self.grid_cells[row][col].config(text=str(value), bg='white')

    # handle next step button
    def next_step(self):
        if self.current_step < len(self.solution[0]) - 1:
            self.current_step += 1
            self.update_grid_display()
            self.prev_button['state'] = tk.NORMAL
        if self.current_step == len(self.solution[0]) - 1:
            self.next_button['state'] = tk.DISABLED

    # handle previous step button
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_grid_display()
            self.next_button['state'] = tk.NORMAL
        if self.current_step == 0:
            self.prev_button['state'] = tk.DISABLED

    # show the solution details
    def show_details(self):
        if self.details:
            details = "\n".join([f"{key}: {value}" for key, value in self.details.items()])
            messagebox.showinfo("Solution Details", details)
        else:
            messagebox.showinfo("Solution Details", "No solution available.")

    # check if the puzzle is solvable
    def check_solvable(self, puzzle):
        inv_count = 0
        puzzle = str(puzzle)
        for i in range(len(puzzle)):
            if puzzle[i] == '0':
                continue
            for j in range(i + 1, len(puzzle)):
                if puzzle[j] and puzzle[i] and puzzle[i] > puzzle[j] != '0':
                    inv_count += 1
        return inv_count % 2 == 0

    # show the goal state (move directly to the goal state)
    def show_goal(self):
        self.current_step = len(self.solution[0]) - 1
        self.update_grid_display()
        self.next_button['state'] = tk.DISABLED
        self.prev_button['state'] = tk.NORMAL


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
