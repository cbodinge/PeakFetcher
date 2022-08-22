import bezier


class Points:
    def __init__(self):
        self._bezier = None
        self._x = None
        self._y = None

    @property
    def bezier(self):
        return self._bezier

    @property
    def points(self):
        return list(zip(self._x, self._y))

    @points.setter
    def points(self, points: list[list[float, float]]):
        if points:
            self._x, self._y = zip(*points)
            self._bezier = bezier.normalized_interpolation(self._x, self._y)
        else:
            self._x, self._y, self._bezier = None, None, None

    @property
    def xmax(self):
        if self._x is not None:
            return max(self._x)

    @property
    def ymax(self):
        if self._y is not None:
            return max(self._y)

    @property
    def xmin(self):
        if self._x is not None:
            return min(self._x)

    @property
    def ymin(self):
        if self._y is not None:
            return min(self._y)
