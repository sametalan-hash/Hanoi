import copy
import sys

TOTAL_DISCS = 5
SOLVED_TOWER = list(range(TOTAL_DISCS, 0, -1))

def main():
    tower = {"A": copy.copy(SOLVED_TOWER), "B": [], "C": []}

    while True:
        displayTowers(tower)
        fromTower, toTower = getPlayerMove(tower)

        # Move the disk
        disk = tower[fromTower].pop()
        tower[toTower].append(disk)

        # Check win condition
        if tower['B'] == SOLVED_TOWER or tower['C'] == SOLVED_TOWER:
            displayTowers(tower)
            print("You have solved the puzzle. Congratulations!")
            sys.exit()

# Get player move
def getPlayerMove(towers):
    while True:
        print("Enter the letters of 'from' and 'to' towers or QUIT")
        print("ex.., AB to move a disk from A to B")
        response = input("> ").upper().strip()

        if response == "QUIT":
            print("Thanks for playing!")
            sys.exit()

        if response not in ("AB", "AC", "BA", "BC", "CA", "CB"):
            print("Please enter a valid combination of letters")
            continue

        fromTower, toTower = response[0], response[1]

        if len(towers[fromTower]) == 0:
            print("You selected an empty tower with no disks")
            continue
        elif len(towers[toTower]) == 0:
            return fromTower, toTower
        elif towers[toTower][-1] < towers[fromTower][-1]:
            print("Cannot put larger disks on smaller disks")
            continue
        else:
            return fromTower, toTower

# Display towers
def displayTowers(towers):
    for level in range(TOTAL_DISCS - 1, -1, -1):
        for tower in (towers["A"], towers["B"], towers["C"]):
            if level >= len(tower):
                displayDisk(0)
            else:
                displayDisk(tower[level])
            print(" ", end="")  # space between towers
        print()  # new line after each level

    # Display labels
    emptySpace = ' ' * TOTAL_DISCS
    print(f"{emptySpace}A{emptySpace}{emptySpace}B{emptySpace}{emptySpace}C\n")

# Display a single disk
def displayDisk(width):
    emptySpace = " " * (TOTAL_DISCS - width)
    if width == 0:
        print(f"{emptySpace}||{emptySpace}", end="")
    else:
        disk = "|" * width
        numLabel = str(width).rjust(2, "_")
        print(f"{emptySpace}{disk}{numLabel}{disk}{emptySpace}", end="")

if __name__ == "__main__":
    main()
