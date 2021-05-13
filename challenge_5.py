import itertools

'''
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But -- oh no! -- one of the escape pods has
flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where
the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine
the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid.
You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell,
(2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those
4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.
Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next
state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula),
and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function
were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical
reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.
The solution will always be less than one billion (10^9).
'''

'''
-- Python cases --
Input:
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254
'''

def compute_2col_outcome(grid):
    h = len(grid)
    w = len(grid[0])
    new_grid = [False*(w-1) for i in range(h-1)]
    for i in range(h-1):
        for j in range(w-1):
            if grid[i][j] + grid[i+1][j] + grid[i][j+1] + grid[i+1][j+1] == 1:
                new_grid[i] = True
    return new_grid if len(new_grid) > 1 else new_grid[0]

def column_predecessors(col):
    res = []
    lst = list(itertools.product([0, 1], repeat=(len(col)+1) * 2))
    for elem in lst:
        square = []
        for i in range(0, len(elem), 2):
            square.append(elem[i:i+2])
        out = compute_2col_outcome(square)
        if out == col:
            res.append(square)
    return res

def solution(g):
    cols = [[row[i] for row in g] for i in range(len(g[0]))]
    pre_cols_prev = column_predecessors(cols.pop(0)) #for first col
    for col in cols:
        pre_cols_curr = column_predecessors(col)
        working_cols_curr = []
        for idx, pre_col_curr in enumerate(pre_cols_curr):
            for pre_col_prev in pre_cols_prev:
                if [i[-1] for i in pre_col_prev] == [i[0] for i in pre_col_curr]:
                    if pre_col_curr not in working_cols_curr:
                        working_cols_curr.append([p[:-1] + pre_col_curr[idx]  for idx, p in enumerate(pre_col_prev)])
        pre_cols_prev = working_cols_curr

    return len(pre_cols_prev)


if __name__ == '__main__':
    #compute_outcome([[True, False, False, False], [False, False, False, True], [False, False, True, False], [False, True, False, False]])
    #compute_outcome([[True, False], [False, False]])
    # lst = list(itertools.product([0, 1], repeat=9))
    # wanted_outcome = [[True, False], [False, False]]
    # for elem in lst:
    #     square = []
    #     square.append(elem[0:3])
    #     square.append(elem[3:6])
    #     square.append(elem[6:9])
    #     output = compute_outcome(square)
    #     if output == wanted_outcome:
    #         print square
    #print(column_predecessors([False, True, False]))
    #print(solution_naive([[True, False, True], [False, True, False], [True, False, True]]))
    print(solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]))
