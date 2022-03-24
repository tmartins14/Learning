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
    new_line = [i for i in line if i != 0]
    
    for line_num in range(len(new_line)):
        if line_num < len(new_line)-1 and new_line[line_num] == new_line[line_num+1]:
            new_line[line_num] = 2 * new_line[line_num]
            new_line[line_num+1] = 0
    
    new_line2 = [i for i in new_line if i != 0]
    zeros = [0]*(len(line)-len(new_line2))
    merged_line = new_line2 + zeros
    
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        
        self._init_lines = {
            UP:[(0, col) for col in range(grid_width)], 
            DOWN:[(grid_height-1, col) for col in range(grid_width)],
            LEFT:[(row, 0) for row in range(grid_height)],
            RIGHT:[(row, grid_width-1) for row in range(grid_height)]
        }
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0*col*row for col in range(self._grid_width)]
                           for row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return '\n'.join(''.join(str(i).center(5) for i in row) for row in self._grid)
        #return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        changes = 0

        
        num_steps_dict = {
            UP: self._grid_height,
            DOWN: self._grid_height,
            LEFT: self._grid_width,
            RIGHT: self._grid_width
        }

        num_steps = num_steps_dict[direction]
        offset_direction = OFFSETS[direction]
        
        init_line = self._init_lines[direction]


        for start_cell in init_line:  
            temp_line = []

            for step in range(num_steps):
                row = start_cell[0] + step * offset_direction[0]
                col = start_cell[1] + step * offset_direction[1]
                temp_line.append(self.get_tile(row, col))

            temp_line2 = merge(temp_line)

            for step in range(num_steps):
                row = start_cell[0] + step * offset_direction[0]
                col = start_cell[1] + step * offset_direction[1]
                
                if self._grid[row][col] != temp_line2[step]:
                    changes += 1
                    
                self.set_tile(row, col, temp_line2[step])
        
        
        if changes > 0:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        if random.randrange(0, 10) > 8:
            new_val = 4
        else:
            new_val = 2
        
        zeros = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._grid[row][col] == 0:
                    zeros.append((row, col))

        rand_cell = random.choice(zeros)
        self._grid[rand_cell[0]][rand_cell[1]] = new_val

    
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        
        self._grid[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        
        return self._grid[row][col]



poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
