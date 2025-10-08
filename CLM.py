import tkinter as tk
import random

GRID_SIZE = 5
CELL_SIZE = 80

SAFE_COLOR = "white"
FIRE_COLOR = "red"
PIT_COLOR = "black"
AGENT_COLOR = "blue"
LEARNED_COLOR = "gray"
VISITED_COLOR = "lightblue"

class CLMSafeAI:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.pack()

        # Create world with random dangers
        self.world = [["safe"] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.world[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = "fire"
        self.world[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = "pit"

        self.agent_pos = [0, 0]
        self.memory = set()        # learned dangers
        self.visited_safe = set()  # visited safe cells
        self.steps = 0

        # Count total safe cells
        self.total_safe_cells = sum(row.count("safe") for row in self.world)

        self.draw_world()
        self.root.after(50, self.step)  # shorter delay for faster exploration

    def draw_world(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = self.world[i][j]
                color = SAFE_COLOR
                if cell == "fire":
                    color = FIRE_COLOR
                elif cell == "pit":
                    color = PIT_COLOR
                if cell in self.memory:
                    color = LEARNED_COLOR
                elif (i, j) in self.visited_safe:
                    color = VISITED_COLOR
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        bx, by = self.agent_pos[1]*CELL_SIZE + CELL_SIZE//2, self.agent_pos[0]*CELL_SIZE + CELL_SIZE//2
        self.canvas.create_oval(bx-20, by-20, bx+20, by+20, fill=AGENT_COLOR)

        # Display progress
        self.canvas.create_text(GRID_SIZE*CELL_SIZE//2, 10, 
                                #text=f"Visited {len(self.visited_safe)}/{self.total_safe_cells} safe cells", 
                                font=("Arial", 14), fill="black")

    def step(self):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        # Learn dangers nearby without stepping
        for dx, dy in directions:
            nx = self.agent_pos[0] + dx
            ny = self.agent_pos[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                cell = self.world[nx][ny]
                if cell in ["fire", "pit"] and cell not in self.memory:
                    print(f"⚠️ AI senses {cell} nearby and learns safely!")
                    self.memory.add(cell)

        # Mark current cell as visited if safe
        if self.world[self.agent_pos[0]][self.agent_pos[1]] == "safe":
            self.visited_safe.add(tuple(self.agent_pos))

        # Collect unvisited safe neighbors
        safe_moves = []
        for dx, dy in directions:
            nx = self.agent_pos[0] + dx
            ny = self.agent_pos[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (self.world[nx][ny] == "safe") and ((nx, ny) not in self.visited_safe) and ((nx, ny) not in self.memory):
                    safe_moves.append((nx, ny))

        # Randomly pick a move among unvisited safe neighbors, else pick any safe cell
        if safe_moves:
            self.agent_pos = random.choice(safe_moves)
        else:
            all_safe_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                              if self.world[i][j] == "safe" and (i, j) not in self.memory]
            if all_safe_cells:
                self.agent_pos = random.choice(all_safe_cells)

        self.steps += 1
        self.draw_world()

        # Continue until all safe cells are visited
        if len(self.visited_safe) < self.total_safe_cells:
            self.root.after(50, self.step)  # faster repeat
        else:
            print(f"✅ CLM AI safely visited all {self.total_safe_cells} safe cells in {self.steps} steps!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ChildLikeMastery(CLM) AI")
    app = CLMSafeAI(root)
    root.mainloop()
