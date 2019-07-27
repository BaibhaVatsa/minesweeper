# Minesweeper

Implementation of Minesweeper game and agent in Python 3.

## Screenshots

<img src="./screenshots/play.jpg" width="500" alt="A Game of 5x5 Map in progress"/>

A Game of 5x5 Map in progress
<br>
<img src="./screenshots/exportedmap.jpg" width="500" alt="Sample exported 20x20 Map"/>

Sample exported 20x20 Map

## Modules

pyminesweeper
- MinesweeperMap
   - Contains the functions to create the minesweeper grid and help connect to a frontend
- MinesweeperUI
   - Contains terminal UI for playing the game and functions to create a customised game UI

## Installing

```
pip install python-minesweeper
```

## How to Play

```python
import pyminesweeper
game = pyminesweeper.MinesweeperUI()
game.run()
```

## Planned additions

- [X] board representation
- [X] board generation
- [X] modifiable size
- [X] human playable
- [X] first click always safe
- [X] number of lives
- [X] different modes
- [X] detailed instructions
- [X] decouple base and ui to separate files
- [X] refactor
- [X] screenshots
- [X] scoreboard
- [X] formatted output
- [X] export maps
- [X] save progress
- [ ] load maps
- [ ] working agent

## Development

All kinds of contributions are very welcome.
<br>
Source: [python-minesweeper](https://github.com/BaibhaVatsa/python-minesweeper)
