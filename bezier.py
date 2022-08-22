def _tridiagonal(n: int):
    """
    creates the Bezier (X) matrix which has a strict definition as tridiaganol in all cases.
    ex. for n = 7

        2   1   0   0   0   0   0
        1   4   1   0   0   0   0
        0   1   4   1   0   0   0
        0   0   1   4   1   0   0
        0   0   0   1   4   1   0
        0   0   0   0   1   4   1
        0   0   0   0   0   2   7

    """
    n = n - 2
    matrix = [i * [0] + [1, 4, 1] + (n - i - 1) * [0] for i in range(n)]
    temp = [2, 1] + n * [0]
    matrix.insert(0, temp)
    matrix.append(n * [0] + [2, 7])

    return matrix


def _build_equals_vector(vector):
    """Solution Vector (Y) for the generalized linear solution X*b=Y"""
    n = len(vector) - 1
    p = [2 * (2 * vector[i] + vector[i + 1]) for i in range(n)]
    p[0] = vector[0] + 2 * vector[1]
    p[-1] = 8 * vector[-2] + vector[-1]

    return p


def _thomas(vector):
    """
    Use Thomas Algorithm to solve the tridiagonal system xb=y.
    """
    n = len(vector) - 1
    x = _tridiagonal(n)
    y = _build_equals_vector(vector)

    c = (n - 1) * [0.0]
    d = n * [0.0]

    for i in range(n):
        if i == 0:
            c[i] = x[i][i + 1] / x[i][i]
            d[i] = y[i] / x[i][i]
        else:
            ai = x[i][i - 1]
            bi = x[i][i]
            di = y[i]
            if i < n - 1:
                ci = x[i][i + 1]
                c[i] = ci / (bi - ai * c[i - 1])

            d[i] = (di - ai * d[i - 1]) / (bi - ai * c[i - 1])

    b = n * [0.0]
    b[-1] = d[-1]
    for i in range(2, n + 1):
        j = -i
        b[j] = (d[j] - c[j + 1] * b[j + 1])

    return b


def interpolate(x: list[float], y: list[float]):
    ax = _thomas(x)
    ay = _thomas(y)

    n = len(x) - 1

    def solve_for_b(a, vector):
        b = n * [0]
        for i in range(n - 1):
            b[i] = 2 * vector[i + 1] - a[i + 1]
        b[-1] = (a[-1] + vector[-1]) / 2

        return b

    bx = solve_for_b(ax, x)
    by = solve_for_b(ay, y)

    return ax, ay, bx, by


def normalized_interpolation(x: list[float], y: list[float]):
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)

    x = [(i - xmin)/(xmax - xmin) for i in x]
    y = [(i - ymin) / (ymax - ymin) for i in y]

    return interpolate(x, y)
