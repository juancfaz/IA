import math

sqrt2 = math.sqrt(2)


class Problem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[0 for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (width - 1, height - 1)

    def startState(self):
        return self.start

    def endState(self):
        return self.end

    def isEnd(self, state):
        return state == self.end

    def blockState(self, state):
        (x, y) = state
        self.world[y][x] = 1

    def unblockState(self, state):
        (x, y) = state
        self.world[y][x] = 0

    def isBlocked(self, state):
        (x, y) = state
        return self.world[y][x]

    def validState(self, state):
        (w, h) = (self.width, self.height)
        (x, y) = state
        if not (0 <= x < w):
            return False
        if not (0 <= y < h):
            return False
        if self.world[y][x] != 0:
            return False
        return True

    def successorsAndCosts(self, state):
        (x, y) = state
        results = []
        if self.validState((x + 1, y)):
            results.append(("e", (x + 1, y), 1))
        if self.validState((x - 1, y)):
            results.append(("w", (x - 1, y), 1))
        if self.validState((x, y - 1)):
            results.append(("n", (x, y - 1), 1))
        if self.validState((x, y + 1)):
            results.append(("s", (x, y + 1), 1))
        if self.validState((x + 1, y + 1)):
            results.append(("se", (x + 1, y + 1), sqrt2))
        if self.validState((x + 1, y - 1)):
            results.append(("ne", (x + 1, y - 1), sqrt2))
        if self.validState((x - 1, y + 1)):
            results.append(("sw", (x - 1, y + 1), sqrt2))
        if self.validState((x - 1, y - 1)):
            results.append(("nw", (x - 1, y - 1), sqrt2))
        return results
