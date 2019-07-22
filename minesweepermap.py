# import the required modules
import random
import math
from datetime import datetime
import enum


@enum.unique
class State(enum.Enum):
    CLEAR = 0
    REVEALED = 1
    FLAGGED = 2


class Map:
    def __init__(self):
        self.val = 0
        self.state = State.CLEAR


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

    def reveal(self, x, y, num_revealed=0):
        already_revealed = True
        if self.map[x][y].state != State.REVEALED:
            already_revealed = False

            if self.map[x][y].state == State.FLAGGED:
                self.flags -= 1

            self.map[x][y].state = State.REVEALED

            if self.map[x][y].val == 0:
                if x < self.size - 1 and self.map[x + 1][y].state != State.REVEALED:
                    _, num_revealed = self.reveal(x + 1, y, num_revealed)

                if x > 0 and self.map[x - 1][y].state != State.REVEALED:
                    _, num_revealed = self.reveal(x - 1, y, num_revealed)

                if y > 0 and self.map[x][y - 1].state != State.REVEALED:
                    _, num_revealed = self.reveal(x, y - 1, num_revealed)

                if y < self.size - 1 and self.map[x][y + 1].state != State.REVEALED:
                    _, num_revealed = self.reveal(x, y + 1, num_revealed)

                if x > 0 and y > 0 and self.map[x - 1][y - 1].state != State.REVEALED:
                    _, num_revealed = self.reveal(x - 1, y - 1, num_revealed)

                if x > 0 and y < self.size - 1 and self.map[x - 1][y + 1].state != State.REVEALED:
                    _, num_revealed = self.reveal(x - 1, y + 1, num_revealed)

                if x < self.size - 1 and y > 0 and self.map[x + 1][y - 1].state != State.REVEALED:
                    _, num_revealed = self.reveal(x + 1, y - 1, num_revealed)

                if x < self.size - 1 and y < self.size - 1 and self.map[x + 1][y + 1].state != State.REVEALED:
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

    def flag(self, x, y):
        if self.map[x][y].state == State.REVEALED:
            print("Invalid location: Already revealed")
        elif self.map[x][y].state == State.FLAGGED:
            self.map[x][y].state = State.CLEAR
            self.flags -= 1
        else:
            self.map[x][y].state = State.FLAGGED
            self.flags += 1

    def accept_input(self):
        move = input(":")
        err, m, x, y = self.validate_move(move)
        while err == False:
            print("Please enter valid input")
            move = input(":")
            err, m, x, y = self.validate_move(move)
        return m, x, y

    def get_stats_str(self):
        stats_str = ""
        stats_str += "Lives remaining: " + str(self.lives) + "\t"
        stats_str += "Turns taken: " + str(self.turns) + "\t"
        stats_str += "Flagged places: " + str(self.flags) + "\t"
        stats_str += "Number of Mines: " + str(self.num_mines)
        stats_str += "\n"

    def get_map_str(self):
        map_str = ""
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j].state == State.FLAGGED:
                    map_str += "[|>]\t"
                elif self.map[i][j].state == State.REVEALED:
                    map_str += str(self.map[i][j].val if self.map[i][j].val != -1 else "[X] ") + "\t"
                else:
                    map_str += "[ ] \t"
            map_str += "\n"
        return map_str

    def get_play_str(self):
        play_str = ""
        play_str += self.get_stats_str()
        play_str += self.get_map_str()

    def map_revealed(self):
        map_revealed_str = ""
        for i in range(self.size):
            for j in range(self.size):
                map_revealed_str += str(self.map[i][j].val if self.map[i][j].val != -1 else "[X]") + "\t"
            map_revealed_str += "\n"

    def export_map(self, out):
        self.generate_map(self.size//2, self.size//2)
        out(self.map_revealed())

    def play(self, out=print):
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
                            out("1 life lost!")
                            out("\n")
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
                out(self.get_play_str())
                out("\n")
                m, x, y = self.accept_input()

        if m == "q":
            result = 0
            out("Be back soon!")
        else:
            out("Congrats!" if result == 1 else "Better luck next time!")
        out("\n")

        return result
