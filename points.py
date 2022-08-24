import bezier


class Points:
    def __init__(self):
        self._bezier = None
        self._x = None
        self._y = None

    def transform(self, xmin=0, xmax=1, ymin=0, ymax=1):
        ax, ay, bx, by = self._bezier
        x, y = self._x[:], self._y[:]

        window = xmax - xmin
        drt = 0.17

        def trans_x(xlist):
            xlist = [(i - self.rt) for i in xlist]
            xlist = [(i + drt) / (2 * drt) for i in xlist]
            xlist = [i * window for i in xlist]
            return xlist

        def trans_y(ylist):
            ylist = [(i - self.ymin) / (self.ymax - self.ymin) for i in ylist]
            ylist = [ymax - (i * (ymax - ymin) - ymin) for i in ylist]

            return ylist

        x = trans_x(x)
        ax = trans_x(ax)
        bx = trans_x(bx)

        y = trans_y(y)
        ay = trans_y(ay)
        by = trans_y(by)

        n = len(ax)

        points = [[[ax[i], ay[i]], [bx[i], by[i]], [x[i + 1], y[i + 1]]] for i in range(n)]
        points = [i for pt in points for i in pt]

        point1 = [x[0], y[0]]
        points.insert(0, point1)

        return points

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
            self._bezier = bezier.interpolate(self._x, self._y)
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

    @property
    def rt(self):
        rt = self._y.index(max(self._y))
        x, y = self.get_points(start=rt-5, end=rt+5)

        i = y.index(max(y))

        return x[i]

    def get_cubic(self, a, b, c, d):
        n = 50
        t = [i / (n - 1) for i in range(n)]
        return [sum([a * (1 - i) ** 3, 3 * i * b * (1 - i) ** 2, 3 * c * (1 - i) * i ** 2, d * i ** 3]) for i in t]

    def get_points(self, start=0, end=0):
        x = self._x[:]
        y = self._y[:]

        if end == 0:
            end = len(x) - 1

        cubex = []
        cubey = []

        for j in range(start, end):
            cubex = cubex + self.get_cubic(x[j], self.bezier[0][j], self.bezier[2][j], x[j + 1])
            cubey = cubey + self.get_cubic(y[j], self.bezier[1][j], self.bezier[3][j], y[j + 1])

        return cubex, cubey
