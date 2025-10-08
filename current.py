import tkinter as tk
import random

GRID_SIZE = 5
CELL_SIZE = 80

SAFE_COLOR = "white"
FIRE_COLOR = "red"
PIT_COLOR = "black"
AGENT_COLOR = "blue"
VISITED_COLOR = "lightblue"

class CurrentAISim:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.pack()

        # Create world with random dangers
        self.world = [["safe"]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.world[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = "fire"
        self.world[random.randint(0, GRID_SIZE-1)][random.randint(0, GRID_SIZE-1)] = "pit"

        self.agent_pos = [0, 0]
        self.visited_safe = set()
        self.mistakes = 0
        self.steps = 0
        self.total_safe_cells = sum(row.count("safe") for row in self.world)

        self.draw_world()
        self.root.after(50, self.step)

    def draw_world(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = self.world[i][j]
                color = SAFE_COLOR if cell=="safe" else FIRE_COLOR if cell=="fire" else PIT_COLOR
                if (i, j) in self.visited_safe:
                    color = VISITED_COLOR
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        bx, by = self.agent_pos[1]*CELL_SIZE + CELL_SIZE//2, self.agent_pos[0]*CELL_SIZE + CELL_SIZE//2
        self.canvas.create_oval(bx-20, by-20, bx+20, by+20, fill=AGENT_COLOR)
        self.canvas.create_text(GRID_SIZE*CELL_SIZE//2, 10,
                                #text=f"Visited {len(self.visited_safe)}/{self.total_safe_cells} safe cells | Mistakes: {self.mistakes}",
                                font=("Arial", 14), fill="black")

    def step(self):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)  # truly random neighbor exploration
        moved = False

        for dx, dy in directions:
            nx, ny = self.agent_pos[0]+dx, self.agent_pos[1]+dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                self.agent_pos = [nx, ny]
                moved = True
                break

        cell = self.world[self.agent_pos[0]][self.agent_pos[1]]
        if cell == "safe":
            self.visited_safe.add(tuple(self.agent_pos))
        else:
            self.mistakes += 1
            print(f"⚠️ AI stepped on {cell} (trial-and-error)")

        self.steps += 1
        self.draw_world()

        if len(self.visited_safe) < self.total_safe_cells:
            self.root.after(50, self.step)
        else:
            print(f"✅ Current AI visited all {self.total_safe_cells} safe cells in {self.steps} steps with {self.mistakes} mistakes!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Current AI Simulation")
    app = CurrentAISim(root)
    root.mainloop()
