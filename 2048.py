"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    new_line = [0] * len(line)
    merged = [False] * len(line)
    pos = 0
    for item in line:
        if not item == 0:
            if new_line[pos - 1] == item and merged[pos - 1] == False:
                new_line[pos - 1] = item * 2
                merged[pos - 1] = True
            else:
                new_line[pos] = item
                pos += 1
    return new_line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()
        self.init_tiles = {}
        up_init = []
        down_init = []
        right_init = []
        left_init = []
        for col in range(self.grid_width):
            up_init.append((0, col))
            down_init.append((self.grid_height - 1, col))
        for row in range(self.grid_height):
            left_init.append((row, 0))
            right_init.append((row, self.grid_width - 1))
        self.dir_dict = {UP: up_init, DOWN: down_init,
                         RIGHT: right_init, LEFT: left_init}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # self.grid = [[0] * self.grid_width] * self.grid_height
        self.grid = []
        for dummy_row in range(self.grid_height):
            new_row = []
            for dummy_col in range(self.grid_width):
                new_row.append(0)
            self.grid.append(new_row)
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = ''
        for row in range(self.grid_height):
            grid_string += str(self.grid[row]) + '\n'
        return grid_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        change_check = False
        for tile in self.dir_dict[direction]:
            if direction == UP or direction == DOWN:
                temp_list = []
                for step in range(self.grid_height):
                    temp_list.append(self.grid[tile[0] + step * OFFSETS[direction][0]]
                                     [tile[1] + step * OFFSETS[direction][1]])
                if not temp_list == merge(temp_list):
                    change_check = True
                temp_list = merge(temp_list)
                for step in range(self.grid_height):
                    self.grid[tile[0] + step * OFFSETS[direction][0]] \
                        [tile[1] + step * OFFSETS[direction][1]] \
                        = temp_list[step]
            if direction == LEFT or direction == RIGHT:
                temp_list = []
                for step in range(self.grid_width):
                    temp_list.append(self.grid[tile[0] + step * OFFSETS[direction][0]]
                                     [tile[1] + step * OFFSETS[direction][1]])
                if not temp_list == merge(temp_list):
                    change_check = True
                temp_list = merge(temp_list)
                for step in range(self.grid_width):
                    self.grid[tile[0] + step * OFFSETS[direction][0]] \
                        [tile[1] + step * OFFSETS[direction][1]] \
                        = temp_list[step]
        if change_check == True:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        col = random.choice(range(self.grid_width))
        row = random.choice(range(self.grid_height))
        if self.grid[row][col] == 0:
            if random.random() >= 0.9:
                self.grid[row][col] = 4
            else:
                self.grid[row][col] = 2
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))