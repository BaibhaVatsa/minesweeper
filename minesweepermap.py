import random
import math
from datetime import datetime
import enum

@enum.unique
class State(enum.Enum):
    clear = 0
    revealed = 1
    flagged = 2

class Map:
    def __init__(self):
        self.val = 0
        self.state = State.clear

class MinesweeperMap:
    def __init__(self, size):
        self.size = size
        self.init_map()
        self.turns = 0
        self.flags = 0
        self.lives = 3

    def init_map(self):
        self.map = [[Map() for _ in range(self.size)] for _ in range(self.size)]

    def generate_map(self, x, y):
        self.generate_bombs(x, y)
        self.generate_hints()

    def generate_bombs(self, x, y):    
        self.num_mines = math.ceil(0.15 * (self.size ** 2))
        random.seed(datetime.now())

        for _ in range(self.num_mines):
            i = random.randrange(0, self.size)
            j = random.randrange(0, self.size)
            random.seed(datetime.now())

            while self.map[i][j].val == -1 or (x == i and y == j):
                i = random.randrange(0, self.size)
                j = random.randrange(0, self.size)
                random.seed(datetime.now())

            self.map[i][j].val = -1

    def generate_hints(self):        
        i, j = 0, 0
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].val != -1:
                    self.map[i][j].val += self.nearby_bombs(i, j)

    def nearby_bombs(self, i, j):
        num_bombs = 0
        if i > 0:
            num_bombs += 1 if self.map[i - 1][j].val == -1 else 0
        
        if i < self.size - 1:
            num_bombs += 1 if self.map[i + 1][j].val == -1 else 0
        
        if j > 0:
            num_bombs += 1 if self.map[i][j - 1].val == -1 else 0
        
        if j < self.size - 1:
            num_bombs += 1 if self.map[i][j + 1].val == -1 else 0
        
        if i > 0 and j > 0:
            num_bombs += 1 if self.map[i - 1][j - 1].val == -1 else 0
        
        if i > 0 and j < self.size - 1:
            num_bombs += 1 if self.map[i - 1][j + 1].val == -1 else 0
        
        if i < self.size - 1 and j > 0:
            num_bombs += 1 if self.map[i + 1][j - 1].val == -1 else 0
        
        if i < self.size - 1 and j < self.size - 1:
            num_bombs += 1 if self.map[i + 1][j + 1].val == -1 else 0
        
        return num_bombs

    def print_map(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].state == State.flagged:
                    print("[|>]", end="\t")
                elif self.map[i][j].state == State.revealed:
                    print(self.map[i][j].val if self.map[i][j].val != -1 else "[X] ", end="\t")    
                else:                
                    print("[ ] ", end="\t")
            print("\n")
    
    def reveal(self, x, y, num_revealed = 0):
        already_revealed = True
        if self.map[x][y].state != State.revealed:
            already_revealed = False

            if self.map[x][y].state == State.flagged:
                self.flags -= 1

            self.map[x][y].state = State.revealed

            if self.map[x][y].val == 0:
                if x < self.size - 1 and self.map[x + 1][y].state != State.revealed:
                    _, num_revealed = self.reveal(x + 1, y, num_revealed)

                if x > 0 and self.map[x - 1][y].state != State.revealed:
                    _, num_revealed = self.reveal(x - 1, y, num_revealed)
                
                if y > 0 and self.map[x][y - 1].state != State.revealed:
                    _, num_revealed = self.reveal(x, y - 1, num_revealed)
                
                if y < self.size - 1 and self.map[x][y + 1].state != State.revealed:
                    _, num_revealed = self.reveal(x, y + 1, num_revealed)
                
                if x > 0 and y > 0 and self.map[x - 1][y - 1].state != State.revealed:
                    _, num_revealed = self.reveal(x - 1, y - 1, num_revealed)
                
                if x > 0 and y < self.size - 1 and self.map[x - 1][y + 1].state != State.revealed:
                    _, num_revealed = self.reveal(x - 1, y + 1, num_revealed)
                
                if x < self.size - 1 and y > 0 and self.map[x + 1][y - 1].state != State.revealed:
                    _, num_revealed = self.reveal(x + 1, y - 1, num_revealed)
                
                if x < self.size - 1 and y < self.size - 1 and self.map[x + 1][y + 1].state != State.revealed:
                    _, num_revealed = self.reveal(x + 1, y + 1, num_revealed)
                    
        return self.map[x][y].val, num_revealed + (0 if already_revealed else 1)    
 
    def validate_input(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size
    
    def validate_mode(self, m):
        return m == "r" or m == "f" or m == "q"

    def validate_move(self, move):
        move_list = move.split()
        if len(move_list) == 3:
            m = move_list[0]
            if self.validate_mode(move_list[0]):
                try:
                    x, y = int(move_list[1]), int(move_list[2])
                    if self.validate_input(x, y):
                        return True, m, x, y
                except:
                    pass
        elif len(move_list) == 1 and move_list[0] == "q":
            return True, "q", -1, -1
        return False, "", -1, -1

    def print(self):
        self.print_stats()
        print("\n")
        self.print_map()
        print("\n")
    
    
    def print_stats(self):
        print("Lives remaining: " + str(self.lives), end="\t")
        print("Turns taken: " + str(self.turns), end = "\t")
        print("Flagged places: " + str(self.flags), end="\t")
        print("Number of Mines: " + str(self.num_mines))

    def print_instructions(self):
        print("  Welcome to MINESWEEPER!")
        print("---------------------------")
        print("How to play:", end=" ")
        print("After \":\" write \"r\" or \"f\" for reveal or flag followed by two valid coordinates x and y of the location you wish to be revealed or flagged.")
        print("For example if you want to reveal the location at (2, 3) it will be \":r 2 3\" and if you want to flag the location at (2, 3) it will be \":f 2 3\"")

    def flag(self, x, y):
        if self.map[x][y].state == State.revealed:
            print("Invalid location: Already revealed")
        elif self.map[x][y].state == State.flagged:
            self.map[x][y].state = State.clear
            self.flags -= 1
        else:
            self.map[x][y].state = State.flagged
            self.flags += 1
    
    def print_all_revealed(self):
        for i in range(self.size):
            for j in range(self.size):
                print((self.map[i][j].val if self.map[i][j].val != -1 else "[X]"), end="\t")
            print()

    def accept_input(self):
        move = input(":")
        err, m, x, y = self.validate_move(move)
        while err == False:
            print("Please enter valid input")
            move = input(":")
            err, m, x, y = self.validate_move(move)
        return m, x, y

    def play(self):
        self.print_instructions()
        result = 0
        
        m, x, y = self.accept_input()
        
        if not m == "q":

            while not m == "r":
                self.flag(x, y)
                m, x, y = self.accept_input()
                    
            self.generate_map(x, y)
            remaining_loc = (self.size ** 2) - self.num_mines

            while not m == "q":
                
                if m == "r":
                    val, locs_revealed = self.reveal(x, y)
                    if val == -1:
                        if self.lives > 0:
                            self.lives -= 1
                            print("1 life lost!")
                        else:
                            result = -1
                    else:
                        remaining_loc -= locs_revealed
                        if remaining_loc == 0:
                            result = 1
                            break
                else:
                    self.flag(x, y)

                self.turns += 1        

                self.print()

                m, x, y = self.accept_input()

        self.print_all_revealed()
        if m == "q":
            print("Be back soon!")
        else:    
            print("Congrats!" if result == 1 else "Better luck next time!")
