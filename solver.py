

def empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                return (i, j)
    return False


def solve(grid):
    space = empty(grid)
    if space:
        row, col = space
    else:
        return True
    for i in range(1, 10):
        if correct(grid, (row, col), i):
            grid[row][col] = i
            if solve(grid):
                return True
            grid[row][col] = 0
    return False


def correct(grid, pos, num):
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and i != pos[0]:
            return False

    for i in range(len(grid)):
        if grid[pos[0]][i] == num and i != pos[1]:
            return False

    min_row = pos[0] // 3
    min_col = pos[1] // 3
    for i in range(min_row * 3, min_row * 3 + 3):
        for j in range(min_col * 3, min_col * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False

    return True
