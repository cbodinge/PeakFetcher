class Points:
    def __init__(self):
        self.x = []
        self.y = []

    @property
    def xmax(self):
        if self.x is not None:
            return max(self.x)

    @property
    def ymax(self):
        if self.y is not None:
            return max(self.y)

    @property
    def xmin(self):
        if self.x is not None:
            return min(self.x)

    @property
    def ymin(self):
        if self.y is not None:
            return min(self.y)

    @property
    def x_at_ymax(self):
        try:
            index = self.y.index(self.ymax)
            return self.x[index]
        except (ValueError, IndexError):
            return

    def normalized(self, xmin=None, xmax=None, ymin=None, ymax=None):
        if xmin is None:
            xmin = self.xmin

        if xmax is None:
            xmax = self.xmax

        if ymin is None:
            ymin = self.ymin

        if ymax is None:
            ymax = self.ymax

        x = [(x - xmin) / (xmax - xmin) for x in self.x]
        y = [(y - ymin) / (ymax - ymin) for y in self.y]

        return x, y
