from enum import Enum
from dataclasses import dataclass
import sys
from time import sleep

@dataclass(frozen=True, eq=True)
class Point:
    X: int
    Y: int

class CellSate(Enum):
    ALIVE = 0
    DEAD = 1

@dataclass(frozen=True, eq=True)
class Board:
    cells: dict[Point, CellSate]
    boundry: Point

def is_within_boundry(point: Point, boundry: Point):
    return point.X in range(0, boundry.X+1) and point.Y in range(0, boundry.Y+1)

def new_state(cell: Point, board: Board) -> CellSate:
    alive_cells = 0
    points_to_tet = [
        Point(X=cell.X, Y=cell.Y-1),
        Point(X=cell.X, Y=cell.Y+1),
        Point(X=cell.X-1, Y=cell.Y-1),
        Point(X=cell.X-1, Y=cell.Y),
        Point(X=cell.X-1, Y=cell.Y+1),
        Point(X=cell.X+1, Y=cell.Y-1),
        Point(X=cell.X+1, Y=cell.Y),
        Point(X=cell.X+1, Y=cell.Y+1),
    ]
    for p in points_to_tet:
        if not is_within_boundry(p, board.boundry):
            continue
        alive_cells += 1 if board.cells[p] == CellSate.ALIVE else 0

    if board.cells[cell] == CellSate.ALIVE:
        return CellSate.ALIVE if alive_cells in [2,3] else CellSate.DEAD
    return CellSate.ALIVE if alive_cells == 3 else CellSate.DEAD 


def frame(current_board: Board) -> Board:
    new_cells: dict[Point, Cell] = dict()
    for p in current_board.cells:
        new_cells[p] = new_state(p, current_board)
    return Board(new_cells, current_board.boundry)

def draw(board: Board):
    x = board.boundry.X
    y = board.boundry.Y
    first_x, first_y = True, True
    for y_i in range(y+1):
        sys.stdout.write("\t|")
        for x_j in range(x+1):
            symbol = "X"
            if board.cells[Point(x_j, y_i)] == CellSate.ALIVE:
                symbol = "O"
            sys.stdout.write(f"{symbol}|")
        sys.stdout.write("\n")
    print("\t=======")


def loop(board):
    while True:
        draw(board)
        board = frame(board)
        sleep(2)

loop(Board(boundry=Point(2,2), cells={
    Point(0, 0):  CellSate.DEAD,
    Point(1, 0):  CellSate.ALIVE,
    Point(2, 0):  CellSate.DEAD,
    Point(0, 1):  CellSate.DEAD,
    Point(1, 1):  CellSate.ALIVE,
    Point(2, 1):  CellSate.DEAD,
    Point(0, 2):  CellSate.DEAD,
    Point(1, 2):  CellSate.ALIVE,
    Point(2, 2):  CellSate.DEAD,
}))
