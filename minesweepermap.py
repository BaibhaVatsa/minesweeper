# import the required modules
import random
import math
from datetime import datetime
import enum
import colorama

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
        colorama.init(autoreset=True)
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
        self.print_welcome()
        print(colorama.Style.BRIGHT + "HOW TO PLAY\n")
        print(": [mode] [x coordinate] [y coordinate]")
        print()
        self.print_coordinate_instructions()
        self.print_reveal_instructions()
        self.print_flag_instructions()
        self.print_quit_instructions()
        self.print_winning_conditions()
        self.print_losing_conditions()
        print()
        
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

    def print_welcome(self):
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + r"""
         __  __ _                                                   
        |  \/  (_)                                                  
        | \  / |_ _ __   ___  _____      _____  ___ _ __   ___ _ __ 
        | |\/| | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
        | |  | | | | | |  __/\__ \\ V  V /  __/  __/ |_) |  __/ |   
        |_|  |_|_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
                                                    | |              
                                                    |_|              

        """)

    def print_reveal_instructions(self):
        print(colorama.Style.BRIGHT + "Reveal mode: r")
        print("Reveals the value of the given tile.")
        print(("If the underlying value is 0, it means there are no bombs in the nearby 8 tiles, 1 means that 1 of the" 
        " 8 neighboring tiles is a bomb, and similarly moving forward. If the underlying value is a bomb, the number of"
        " lives remaining goes down by 1. If the number of lives is already at 0, the game ends. A revealed tile cannot"
        " be flagged."))
        print("For example: \"r 0 0\" will reveal the value of the tile at the coordinates (0, 0).") 
        print()

    def print_flag_instructions(self):
        print(colorama.Style.BRIGHT + "Flag mode: f")
        print("Flags the given tile")
        print(("A flagged tile can be unflagged or revealed (the latter will automatically do the former but not"
        " vice-versa) anytime. Flagging a flagged tile, unflags it. A revealed tile cannot be flagged. Flagging a tile" 
        " has no effect on number of lives remaining irrespective of the value of the tile underneath. This mode is" 
        " meant to help you \"flag\" potential bombs."))
        print("For example: \"f 0 0\" will flag the value of the tile at the coordinates (0, 0).")
        print("             \"f 0 0\" later will unflag the tile at the coordinates (0, 0).")
        print()

    def print_quit_instructions(self):
        print(colorama.Style.BRIGHT + "Quit: q")
        print("Quits the game at any time.")
        print("For example: \"q\" will quit the game that instant")
        print()

    def print_coordinate_instructions(self):    
        print(colorama.Style.BRIGHT + "Entering coordinates: [x coordinate] [y coordinate]")
        print(("[x coordinate] is the number of the row of the cell and [y coordinate] is the number of the"
        " column of the cell. 0 (x coordinate) 0 (y coordinate) is the top left corner of the map. Coordinates"
        " are 0 indexed."))
        print("For example: \"0 1\" is the cell at the intersection of the 2nd column and the 1st row.")
        print()
    
    def print_winning_conditions(self):
        print(colorama.Style.BRIGHT + "Win conditions")
        print("If all non-bomb cells have been revealed, the game is won.")
        print()
    
    def print_losing_conditions(self):
        print(colorama.Style.BRIGHT + "Lose conditions")
        print("If the number of lives goes below 0, the game is lost.")
        print()