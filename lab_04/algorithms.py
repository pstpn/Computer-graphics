from math import sqrt, cos, sin, pi


# Add symmetric points
def AddSymPoints(x_c, y_c, x, y, figure: str):

    # Create points list
    points = []

    # Get delta
    delta_x = x - x_c
    delta_y = y - y_c

    # If figure is circle add 4 points
    if figure == "Circle":
        points.append([x_c - delta_y, y_c + delta_x])
        points.append([x_c + delta_y, y_c + delta_x])
        points.append([x_c + delta_y, y_c - delta_x])
        points.append([x_c - delta_y, y_c - delta_x])

    # Add 4 symmetric points
    points.append([x_c - delta_x, y_c + delta_y])
    points.append([x_c + delta_x, y_c + delta_y])
    points.append([x_c + delta_x, y_c - delta_y])
    points.append([x_c - delta_x, y_c - delta_y])

    return points


# Get circle points using canonical equation (x^2 + y^2 = r^2)
def CanonicalCircle(params: list, draw=True):

    # Get params
    x_c, y_c, r = params

    # Create points list
    points = []

    # Get edge
    x = 0
    r_sqr = r * r
    edge = round(r / sqrt(2))

    # Get points
    while x <= edge:

        # Get y
        y = sqrt(r_sqr - x ** 2)

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Circle")

        x += 1

    if draw:
        return points


# Get circle points using parametric equation (x = r * cos(alpha), y = r * sin(alpha))
def ParametricCircle(params: list, draw=True):

    # Get params
    x_c, y_c, r = params

    # Create points list
    points = []

    # Get step
    step = 1 / r

    # Get angle
    alpha = 0
    n = 0

    # Get points
    while alpha <= pi / 4:

        x = round(r * cos(alpha))
        y = round(r * sin(alpha))

        alpha = step * n
        n += 1

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Circle")

    if draw:
        return points


# Get circle points using Bresenham algorithm
def BresenhamCircle(params: list, draw=True):

    # Get params
    x_c, y_c, r = params

    # Create points list
    points = []
    x = 0
    y = r

    # Get delta
    delta = 2 * (1 - r)

    # Get points
    while x <= y:
        if draw:
            points += AddSymPoints(x_c, y_c, x_c + x, y_c + y, "Circle")

        x += 1
        if delta < 0 and 2 * delta + 2 * y - 1 < 0:
            delta += 2 * x + 1
        else:
            y -= 1
            delta += 2 * (x - y + 1)

    if draw:
        return points


# Get circle points using midpoint algorithm
def MidpointCircle(params: list, draw=True):

    # Get params
    x_c, y_c, r = params

    # Create points list
    points = []
    x = 0
    y = r

    # Get delta
    delta = 5/4 - r

    # Get points
    while x <= y:
        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Circle")

        x += 1

        if delta < 0:
            delta += 2 * x + 1
        else:
            y -= 1
            delta += 2 * x + 1 - 2 * y

    if draw:
        return points


# Get circle points using library algorithm
def LibCircle(params: list, draw=False):
    return [[params[0], params[1], int(params[2]), int(params[2])]]


# Get ellipse points using canonical equation (x^2 / rx^2 + y^2 / ry^2 = 1)
def CanonicalEllipse(params: list, draw=True):

    # Get params
    x_c, y_c, rx, ry = params

    # Create points list
    points = []

    # Get square of rx and ry
    sqr_rx = rx * rx
    sqr_ry = ry * ry
    sqr = sqr_rx * sqr_ry

    # Get edges of ellipse
    edge_x = round(rx / sqrt(1 + sqr_ry / sqr_rx))

    # Get points
    x = 0
    while x <= edge_x:
        y = round(sqrt(sqr - x * x * sqr_ry) / rx)

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

        x += 1

    while y >= 0:
        x = round(sqrt(sqr - y * y * sqr_rx) / ry)

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

        y -= 1

    if draw:
        return points


# Get ellipse points using parametric equation (x = rx * cos(alpha), y = ry * sin(alpha))
def ParametricEllipse(params: list, draw=True):

    # Get params
    x_c, y_c, rx, ry = params

    # Create points list
    points = []

    # Get step
    step = 1 / max(rx, ry)

    # Get angle
    alpha = 0

    # Get points
    while alpha <= pi / 2:

        x = round(rx * cos(alpha))
        y = round(ry * sin(alpha))

        alpha += step

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

    if draw:
        return points


# Get ellipse points using Bresenham algorithm
def BresenhamEllipse(params: list, draw=True):

    # Get params
    x_c, y_c, rx, ry = params

    # Create points list
    points = []
    y = ry
    x = 0

    # Get square of rx and ry
    sqr_rx = rx * rx
    sqr_ry = ry * ry

    # Get delta
    delta = sqr_ry - sqr_rx * (2 * ry + 1)

    # Get points
    while y >= 0:

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

        if delta <= 0:
            d1 = 2 * delta + sqr_rx * (2 * y + 2)

            x += 1

            if d1 < 0:
                delta += sqr_ry * (2 * x + 1)
            else:
                y -= 1
                delta += sqr_ry * (2 * x + 1) + sqr_rx * (1 - 2 * y)
        else:
            d2 = 2 * delta + sqr_ry * (2 - 2 * x)

            y -= 1

            if d2 < 0:
                x += 1
                delta += sqr_ry * (2 * x + 1) + sqr_rx * (1 - 2 * y)
            else:
                delta += sqr_rx * (1 - 2 * y)

    if draw:
        return points


# Get ellipse points using midpoint algorithm
def MidpointEllipse(params: list, draw=True):

    # Get params
    x_c, y_c, rx, ry = params

    # Create points list
    points = []
    y = ry
    x = 0

    # Get square of rx and ry
    sqr_rx = rx * rx
    sqr_ry = ry * ry

    # Get edge and delta
    edge = round(rx / sqrt(1 + sqr_ry / sqr_rx))
    delta = sqr_ry - round(sqr_rx * (ry - 1 / 4))

    # Get points
    while x <= edge:

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

        x += 1
        if delta < 0:
            delta += sqr_ry * (2 * x + 1)
        else:
            y -= 1
            delta += sqr_ry * (2 * x + 1) - sqr_rx * 2 * y

    x = rx
    y = 0

    # Get edge and delta
    edge = round(ry / sqrt(1 + sqr_rx / sqr_ry))
    delta = sqr_rx - round(sqr_ry * (rx - 1 / 4))

    # Get points
    while y <= edge:

        if draw:
            points += AddSymPoints(x_c, y_c, x + x_c, y + y_c, "Ellipse")

        y += 1
        if delta < 0:
            delta += sqr_rx * (2 * y + 1)
        else:
            x -= 1
            delta += sqr_rx * (2 * y + 1) - sqr_ry * 2 * x

    if draw:
        return points


# Get ellipse points using library algorithm
def LibEllipse(params: list, draw=False):
    return [[params[0], params[1], int(params[3]), int(params[2])]]