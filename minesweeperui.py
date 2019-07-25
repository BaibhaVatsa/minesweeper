from minesweepermap import MinesweeperMap
import colorama
import enum


class MenuOptions(enum.Enum):
    PLAY = "1"
    EXPORT = "2"
    HOWTO = "3"
    ABOUT = "4"
    EXIT = "5"


class MinesweeperUI:
    def __init__(self):
        colorama.init(autoreset=True)

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
        self.print_header("Reveal mode: r")
        print("Reveals the value of the given tile.")
        print(("If the underlying value is 0, it means there are no bombs in the nearby 8 tiles, 1 means that 1 of the"
               " 8 neighboring tiles is a bomb, and similarly moving forward. If the underlying value is a bomb, the number of"
               " lives remaining goes down by 1. If the number of lives is already at 0, the game ends. A revealed tile cannot"
               " be flagged."))
        print("For example: \"r 0 0\" will reveal the value of the tile at the coordinates (0, 0).")
        self.print_whitespace(1)

    def print_flag_instructions(self):
        self.print_header("Flag mode: f")
        print("Flags the given tile")
        print(("A flagged tile can be unflagged or revealed (the latter will automatically do the former but not"
               " vice-versa) anytime. Flagging a flagged tile, unflags it. A revealed tile cannot be flagged. Flagging a tile"
               " has no effect on number of lives remaining irrespective of the value of the tile underneath. This mode is"
               " meant to help you \"flag\" potential bombs."))
        print("For example: \"f 0 0\" will flag the value of the tile at the coordinates (0, 0).")
        print("             \"f 0 0\" later will unflag the tile at the coordinates (0, 0).")
        self.print_whitespace(1)

    def print_quit_instructions(self):
        self.print_header("Quit: q")
        print("Quits the game at any time. Goes back to the menu.")
        print("For example: \"q\" will quit the game that instant and get you back to the menu.")
        self.print_whitespace(1)

    def print_coordinate_instructions(self):
        self.print_header("Entering coordinates: [x coordinate] [y coordinate]")
        print(("[x coordinate] is the number of the row of the cell and [y coordinate] is the number of the"
               " column of the cell. 0 (x coordinate) 0 (y coordinate) is the top left corner of the map. Coordinates"
               " are 0 indexed."))
        print("For example: \"0 1\" is the cell at the intersection of the 2nd column and the 1st row.")
        self.print_whitespace(1)

    def print_winning_conditions(self):
        self.print_header("Win conditions")
        print("If all non-bomb cells have been revealed, the game is won.")
        self.print_whitespace(1)

    def print_losing_conditions(self):
        self.print_header("Lose conditions")
        print("If the number of lives goes below 0, the game is lost.")
        self.print_whitespace(2)

    def print_instructions(self):
        self.print_header("HOW TO PLAY")
        self.print_whitespace(1)
        print(": [mode] [x coordinate] [y coordinate]")
        self.print_whitespace(1)
        self.print_coordinate_instructions()
        self.print_reveal_instructions()
        self.print_flag_instructions()
        self.print_quit_instructions()
        self.print_winning_conditions()
        self.print_losing_conditions()
        self.print_whitespace(1)
        self.go_back_to_menu()

    def print(self):
        self.print_stats()
        self.print_whitespace(2)
        self.print_map()
        self.print_whitespace(2)

    def print_all_revealed(self):
        print(self.game.map_revealed())
        self.print_whitespace(1)

    def print_map(self):
        print(self.game.get_map_str())
        self.print_whitespace(1)

    def print_stats(self):
        self.print_header(self.game.get_stats_str())
        self.print_whitespace(1)

    def print_whitespace(self, num):
        for _ in range(num):
            print()

    def print_header(self, str):
        print(colorama.Style.BRIGHT + str)

    def print_menu(self):
        self.print_header("MENU")
        self.print_whitespace(2)
        print("1: Play")
        self.print_whitespace(1)
        print("2: Export a Map")
        self.print_whitespace(1)
        print("3: How to Play Instructions")
        self.print_whitespace(1)
        print("4: About")
        self.print_whitespace(1)
        print("5: Exit")
        self.print_whitespace(1)

    def export_map(self):
        import time
        fil = open(str(int(round(time.time() * 1000)))+".txt", "w")
        self.game.export_map(out=fil.write)
        fil.close()
        self.go_back_to_menu()

    def play(self):
        result = self.game.play(out=print)
        if result != 1:
            print("Solution: ")
            self.print_all_revealed()

        self.go_back_to_menu()

    def go_back_to_menu(self):
        input("Press enter to go back to the menu...")
        self.print_whitespace(1)

    def print_about(self):
        self.print_header("ABOUT")
        print(("Minesweeper is a game I used to play a lot as a kid. Wrote this implementation in Summer '19"
               " to just see how writing it would be. The source code can be found at github.com/BaibhaVatsa/minesweeper."
               " Feedback and suggestions are very much welcome! Hope you have fun playing this! :D"))
        self.print_whitespace(1)
        self.go_back_to_menu()

    def choose_option(self) -> str:
        self.print_menu()
        choice = input("Choose option: ")
        self.print_whitespace(1)
        valid_options = [x.value for x in MenuOptions]
        while choice not in valid_options:
            print("Please choose from valid options")
            self.print_whitespace(1)        
            self.print_menu()
            choice = input("Choose option: ")
            self.print_whitespace(1)
        return choice

    def print_thankyou(self):
        self.print_header("THANK YOU for playing!")
        print("Feel free to reach out at @BaibhavVatsa on Twitter")

    def is_valid_size(self, size) -> (bool, int):
        try:
            size_val = int(size)
            if size_val > 0:
                return True, size_val
            return False, 0
        except:
            return False, 0

    def get_size(self):
        size = input("Choose size of the Minesweeper Grid (> 0): ")
        self.print_whitespace(1)
        valid_int, self.size_value = self.is_valid_size(size)
        while not valid_int:
            print("Please choose valid size (> 0)")
            size = input("Choose size of the Minesweeper Grid: ")
            self.print_whitespace(1)
            valid_int, self.size_value = self.is_valid_size(size)

    def declare_minesweeper_map(self):
        self.get_size()
        self.game = MinesweeperMap(self.size_value)

    def run(self):
        self.print_welcome()
        choice = self.choose_option()
        while choice != MenuOptions.EXIT.value:
            if choice == MenuOptions.PLAY.value or choice == MenuOptions.EXPORT.value:
                self.declare_minesweeper_map()
                if choice == MenuOptions.PLAY.value:
                    self.play()
                else:
                    self.export_map()
            elif choice == MenuOptions.HOWTO.value:
                self.print_instructions()
            elif choice == MenuOptions.ABOUT.value:
                self.print_about()
            choice = self.choose_option()
        self.print_thankyou()
