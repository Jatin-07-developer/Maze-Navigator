import curses
from curses import wrapper
import queue
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
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "X"]
]


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    path = find_path(maze, "O", "X", stdscr)

    if path:
        print_maze(stdscr, maze, path)
        stdscr.refresh()
        find_path(maze, stdscr)
        stdscr.getch()


def print_maze(stdscr, maze, path=None):
    if path is None:
        path = []

    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    path = set(path)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):

            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, BLUE)


def findStart(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return (i, j)

    return None


def find_path(maze, start, end, stdscr):

    start_pos = findStart(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()
    visited.add(start_pos)

    while not q.empty():
        current_pos, path = q.get()
        row, column = current_pos

        stdscr.clear()
        print_maze(stdscr, maze, path)
        stdscr.refresh()
        time.sleep(0.1)

        if maze[row][column] == end:
            return path

        neighbours = findNeighbours(maze, row, column)

        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)

    return None


def findNeighbours(maze, row, column):
    neighbours = []

    if row > 0:
        neighbours.append((row - 1, column))
    if row + 1 < len(maze):
        neighbours.append((row + 1, column))
    if column > 0:
        neighbours.append((row, column - 1))
    if column + 1 < len(maze[0]):
        neighbours.append((row, column + 1))

    return neighbours


wrapper(main)
