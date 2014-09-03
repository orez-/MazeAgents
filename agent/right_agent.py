import board
from constants import *


class RightAgent(object):
    def __init__(self):
        self.facing = RIGHT
        self.memory = board.Maze(3, 3)
        self.x = 0
        self.y = 0

    def see(self, information):
        for (x, y, direction), wall in information.iteritems():
            self.memory.set_wall(x, y, direction, wall)

    def act(self):
        dir_lookup = {
            UP: (0, -1),
            RIGHT: (1, 0),
            DOWN: (0, 1),
            LEFT: (-1, 0),
        }
        for direction in [RIGHT, UP, LEFT, DOWN]:
            direction = (self.facing + direction) % 4
            if self.passable(direction):
                self.facing = direction
                self.x, self.y = map(sum, zip(dir_lookup[direction], (self.x, self.y)))
                return direction
        return None

    def passable(self, direction):
        is_wall = self.memory.is_wall(self.x, self.y, direction)
        if is_wall is None:
            return False
        return not is_wall

    def __str__(self):
        maze = self.memory
        string = []
        for y in xrange(maze.top, maze.bottom + 1):
            for x in xrange(maze.left, maze.right + 1):
                wall = maze.walls.get((x, y))
                if self.x == x and self.y == y:
                    string.append("0")
                elif wall is None:
                    string.append(" ")
                else:
                    string.append("#" if wall else ".")
            string.append("\n")
        return ''.join(string)
