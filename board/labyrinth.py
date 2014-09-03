import random
# from constants import *
import board


class EmptyMaze(board.Maze):
    """Rectangular open area with surrounding walls."""
    def __init__(self, width, height):
        super(EmptyMaze, self).__init__(width, height)

        for y in xrange(height):
            for x in xrange(width):
                self.set_wall(x, y, value=False)


class RectangleLabyrinth(board.Maze):
    def __init__(self, width, height):
        hwidth = (width + 1) // 2
        hheight = (height + 1) // 2

        # Snip the extra: since we expect an odd number of squares,
        # we're just going to fill in the last even row with walls
        # that can never be seen anyway.
        super(RectangleLabyrinth, self).__init__(width + 1, height + 1)

        # Start with a giant hunk of marble. Create a CellSet for each
        # cell, which represents all the cells attached to this one.
        # Currently, each cell is attached to only itself.
        cells = [[_CellSet() for _ in xrange(hwidth)] for _ in xrange(hheight)]

        # Generate the edges between the cells. Maps the x and y
        # coordinates and if the path is upwards or to the left, to
        # the two CellSets of the cells the path connects.
        paths = {
            (x, y, is_up): (cells[y][x], cells[y - is_up][x - (not is_up)])
            for x in xrange(hwidth)
            for y in xrange(hheight)
            for is_up in (False, True)
            if not (is_up and y == 0) and not (not is_up and x == 0)
        }

        # Chisel the marble: for each path, if either side is of a
        # different CellSet, create a path between them, and make them
        # share a CellSet.
        order = paths.keys()
        random.shuffle(order)
        for key in order:
            cset1, cset2 = paths[key]
            if cset1 != cset2:
                del paths[key]
                cset1.join(cset2)

        # Fill in the center
        for x in xrange(hwidth):
            xt = x * 2
            for y in xrange(hheight):
                yt = y * 2
                self.walls[(xt, yt)] = True
                self.walls[(xt + 1, yt)] = (x, y, True) in paths
                self.walls[(xt, yt + 1)] = (x, y, False) in paths
                self.walls[(xt + 1, yt + 1)] = False

        # Fill in the edges
        for x in xrange(width + 1):
            self.walls[(x, 0)] = True

        for y in xrange(height + 1):
            self.walls[(0, y)] = True


class CirclesLabyrinth(board.Maze):
    def __init__(self, radius):
        width = radius * 8
        height = radius * 8
        hwidth = (width - 1) // 2
        hheight = (height - 1) // 2
        super(CirclesLabyrinth, self).__init__(hwidth * 2 + 1, hheight * 2 + 1)

        closure = lambda x2, y2: lambda x1, y1: (x1 - x2) ** 2 + (y1 - y2) ** 2 < radius ** 2
        circles = [
            closure(x2, y2)
            for x2, y2 in [
                (radius * 2, radius),
                (radius, radius * 2),
                (radius * 2, radius * 3),
                (radius * 3, radius * 2),
                (radius * 2, radius * 2),
            ]
        ]

        cells = [[
            _CellSet() if any(f(x, y) for f in circles) else None
            for x in xrange(hwidth)]
            for y in xrange(hheight)
        ]

        paths = {
            (x, y, is_up): (cells[y][x], cells[y - is_up][x - (not is_up)])
            for x in xrange(hwidth)
            for y in xrange(hheight)
            for is_up in (False, True)
            if not (is_up and y == 0) and not (not is_up and x == 0)
        }

        order = paths.keys()
        random.shuffle(order)
        for key in order:
            cset1, cset2 = paths[key]
            if not (cset1 is cset2 is None):
                if cset1 is None or cset2 is None:
                    paths[key] = True
                elif cset1 != cset2:
                    cset1.join(cset2)
                    paths[key] = False
                else:
                    paths[key] = True

        # Fill in the center
        for x in xrange(hwidth):
            xt = x * 2
            for y in xrange(hheight):
                yt = y * 2
                if cells[y][x] is None:
                    continue
                self.walls[(xt, yt)] = True
                self.walls[(xt + 1, yt)] = paths[(x, y, True)]
                self.walls[(xt, yt + 1)] = paths[(x, y, False)]
                self.walls[(xt + 1, yt + 1)] = False


class _CellSet(object):
    _id = 0

    def __init__(self):
        self.id = _CellSet._id
        _CellSet._id += 1
        self.parent = None

    def join(self, other):
        other.root.parent = self.root

    @property
    def root(self):
        while True:
            if self.parent is None:
                return self
            self = self.parent

    def __eq__(self, other):
        return self.root is other.root

    def __ne__(self, other):
        return self.root is not other.root

    def __repr__(self):
        return str(self.root.id)


if __name__ == '__main__':
    import sys
    try:
        args = map(int, sys.argv[1:])
    except ValueError:
        args = 20, 10
    # maze = CirclesLabyrinth(*args)
    maze = RectangleLabyrinth(*args)
    print str(maze)
