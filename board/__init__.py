import constants


class Maze(object):
    def __init__(self, width, height):
        self.left = 0
        self.top = 0
        self.right = width
        self.bottom = height
        self.walls = {}

    @staticmethod
    def _translate_coords(x, y, direction):
        dir_map = {
            constants.UP: (x, y - 1),
            constants.RIGHT: (x + 1, y),
            constants.DOWN: (x, y + 1),
            constants.LEFT: (x - 1, y),
            None: (x, y),
        }
        return dir_map[direction]

    def set_wall(self, x, y, direction=None, value=True):
        x, y = Maze._translate_coords(x, y, direction)
        # print x, y, direction, value
        self.walls[(x, y)] = bool(value)
        self.left = min(self.left, x)
        self.right = max(self.right, x)
        self.top = min(self.top, y)
        self.bottom = max(self.bottom, y)

    def is_wall(self, x, y, direction=None):
        x, y = Maze._translate_coords(x, y, direction)
        return self.walls.get((x, y), True)

    def __str__(self):
        string = []
        for y in xrange(self.top, self.bottom):
            for x in xrange(self.left, self.right):
                wall = self.walls.get((x, y))
                if wall is None:
                    string.append("?")
                else:
                    string.append("#" if wall else ".")
            string.append("\n")
        return ''.join(string)
