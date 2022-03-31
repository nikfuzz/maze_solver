import curses
from curses import wrapper
from collections import deque
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(stdscr, maze, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, 'X', RED)
            else:
                stdscr.addstr(i, j*2, val, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == start:
                return i,j
    return None


def find_path(maze, stdscr):
    start = 'O'
    end = 'X'

    start_pos = find_start(maze, start)

    q = deque()
    q.append((start_pos, [start_pos]))

    visited = set()

    while q:
        curr_pos, path = q.popleft()
        row, col = curr_pos

        stdscr.clear()
        print_maze(stdscr, maze, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:

            neighbor_row, neighbor_col = neighbor

            if neighbor in visited or maze[neighbor_row][neighbor_col] == '#':
                continue

            new_path = path + [neighbor]
            q.append((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    neighbors = []

    # up
    if row > 0: 
        neighbors.append((row-1, col))

    # down
    if row + 1 < len(maze):
        neighbors.append((row+1, col))

    # left
    if col > 0: 
        neighbors.append((row, col-1))

    # right
    if col + 1 < len(maze[0]):
        neighbors.append((row, col+1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)