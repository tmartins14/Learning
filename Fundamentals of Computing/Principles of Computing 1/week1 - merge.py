"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
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

