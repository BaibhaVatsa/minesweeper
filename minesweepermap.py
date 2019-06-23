import random
import math
import enum

class Map:
    def __init__(self):
        self.val = 0
        self.revealed = False

class MinesweeperMap:
    def __init__(self, size):
        self.size = size
        self.result = 0
        self.init_map()
        self.generate_map()
        self.turns = 0
        self.lives = 3

    def init_map(self):
        self.map = [[Map() for _ in range(self.size)] for _ in range(self.size)]

    def generate_map(self):
        self.generate_bombs()
        self.generate_hints()

    def generate_bombs(self):    
        num_mines = math.ceil(0.15 * (self.size ** 2))
        random.seed(num_mines)
        i = random.randrange(0, self.size)
        j = random.randrange(0, self.size)
        for _ in range(num_mines):
            while self.map[i][j].val == -1:
                i = random.randrange(0, self.size)
                j = random.randrange(0, self.size)
            self.map[i][j].val = -1
            num_mines -= 1
            random.seed(num_mines)

    def generate_hints(self):        
        i, j = 0, 0
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].val != -1:
                    self.map[i][j].val += self.nearby_bombs(i, j)

    def nearby_bombs(self, i, j):
        num_bombs = 0
        if (i - 1) >= 0:
            num_bombs += 1 if self.map[i - 1][j].val == -1 else 0
        if (i + 1) < self.size:
            num_bombs += 1 if self.map[i + 1][j].val == -1 else 0
        if (j - 1) >= 0:
            num_bombs += 1 if self.map[i][j - 1].val == -1 else 0
        if (j + 1) < self.size:
            num_bombs += 1 if self.map[i][j + 1].val == -1 else 0
        if (i - 1) >= 0 and (j - 1) >= 0:
            num_bombs += 1 if self.map[i - 1][j - 1].val == -1 else 0
        if (i - 1) >= 0 and (j + 1) < self.size:
            num_bombs += 1 if self.map[i - 1][j + 1].val == -1 else 0
        if (i + 1) < self.size and (j - 1) >= 0:
            num_bombs += 1 if self.map[i + 1][j - 1].val == -1 else 0
        if (i + 1) < self.size and (j + 1) < self.size:
            num_bombs += 1 if self.map[i + 1][j + 1].val == -1 else 0
        return num_bombs

    def print_map(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].revealed:
                    print(self.map[i][j].val if self.map[i][j].val != -1 else "[X]", end="\t")    
                else:                
                    print("[ ]", end="\t")
            print("\n")
    
    def remaining_locations(self):
        locations = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].val != -1 and not self.map[i][j].revealed:
                    locations += 1
        if locations == 0:
            self.result = 1

    #TODO recursion
    def reveal(self, i, j):
        if self.map[i][j].val != -1: 
            self.map[i][j].revealed = True
            
            i_this, j_this = i, j
            while (i_this - 1) >= 0 and self.map[i - 1][j].val == 0:
                self.map[i_this - 1][j].revealed = True
                i_this -= 1
            if (i_this - 1) >= 0:
                self.map[i - 1][j].revealed = True if self.map[i - 1][j].val != -1 else False      
            
            i_this = i
            while (i_this + 1) < self.size and self.map[i_this + 1][j].val == 0:
                self.map[i_this + 1][j].revealed = True
                i_this += 1
            if (i_this + 1) < self.size:
                self.map[i_this + 1][j].revealed = True if self.map[i_this + 1][j].val != -1 else False
            
            i_this = i
            while (j_this - 1) >= 0 and self.map[i][j_this - 1].val == 0:
                self.map[i][j_this - 1].revealed = True
                j_this -= 1
            if (j_this - 1) >= 0:
                self.map[i][j_this - 1].revealed = True if self.map[i][j_this - 1].val != -1 else False
            
            j_this = j
            while (j_this + 1) < self.size and self.map[i][j_this + 1].val == 0:
                self.map[i][j_this + 1].revealed = True
                j_this += 1
            if (j_this + 1) < self.size:
                self.map[i][j_this + 1].revealed = True if self.map[i][j_this + 1].val != -1 else False
            
            j_this = j
            while (i_this - 1) >= 0 and (j_this - 1) >= 0 and self.map[i_this - 1][j_this - 1].val == 0:
                self.map[i_this - 1][j_this - 1].revealed = True
                i_this -= 1
                j_this -= 1
            if (i_this - 1) >= 0 and (j_this - 1) >= 0:
                self.map[i_this - 1][j_this - 1].revealed = True if self.map[i_this - 1][j_this - 1].val != -1 else False
            
            i_this, j_this = i, j            
            while (i_this - 1) >= 0 and (j_this + 1) < self.size and self.map[i_this - 1][j_this + 1].val == 0:
                self.map[i_this - 1][j_this + 1].revealed = True
                i_this -= 1 
                j_this += 1
            if (i_this - 1) >= 0 and (j_this + 1) < self.size:
                self.map[i_this - 1][j_this + 1].revealed = True if self.map[i_this - 1][j_this + 1].val != -1 else False
            
            i_this, j_this = i, j            
            while (i_this + 1) < self.size and (j_this + 1) < self.size and self.map[i_this + 1][j_this + 1].val == 0:
                self.map[i_this + 1][j_this + 1].revealed = True
                i_this += 1
                j_this += 1
            if (i_this + 1) < self.size and (j_this + 1) < self.size:
                self.map[i_this + 1][j_this + 1].revealed = True if self.map[i_this + 1][j_this + 1].val != -1 else False
            
            i_this, j_this = i, j            
            while (i_this + 1) < self.size and (j_this - 1) >= 0 and self.map[i_this + 1][j_this - 1].val == 0:
                self.map[i_this + 1][j_this - 1].revealed = True
                i_this += 1
                j_this -= 1
            if (i_this + 1) < self.size and (j_this - 1) >= 0:
                self.map[i_this + 1][j_this - 1].revealed = True if self.map[i_this + 1][j_this - 1].val != -1 else False
        else:
            self.result = -1

    def play(self):
        i, j = 0, 0
        while self.result == 0:
            self.print_map()
            i = int(input("i coord: "))
            j = int(input("j coord: "))
            self.reveal(i, j)
            self.remaining_locations()
        self.map[i][j].revealed = True
        self.print_map()
        print("\nCongrats!" if self.result == 1 else "\nBetter luck next time!")
