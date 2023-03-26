from math import floor, fabs


# Get sign of number
def sign(x):

    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# Digital Differential Analyzer Algorithm
def DDAAlgorithm(x1, y1, x2, y2, color):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[round(x1), round(y1), color]]

    # Calculate the number of steps
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    # Calculate the increment in x and y for each step
    x_inc = dx / steps
    y_inc = dy / steps

    # Set the initial point
    x = x1
    y = y1

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(steps):
        points.append([round(x), round(y), color])
        x += x_inc
        y += y_inc

    return points


# Bresenham float algorithm
def BresenhamFloatAlgorithm(x1, y1, x2, y2, color):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, color]]

    # Get sign of dx and dy
    sx = sign(dx)
    sy = sign(dy)

    # Absolute values of dx and dy
    dx = abs(dx)
    dy = abs(dy)

    # Calculate the number of steps
    if dy > dx:
        dx, dy = dy, dx
        exchange = True
    else:
        exchange = False

    # Initialize the error
    try:
        error = dy / dx - 0.5
    except ZeroDivisionError:
        error = dy / 1e-10 - 0.5

    # Set the initial point
    x = x1
    y = y1

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(dx + 1):
        points.append([x, y, color])

        if error >= 0:
            if exchange:
                x += sx
            else:
                y += sy

            error -= 1

        if exchange:
            y += sy
        else:
            x += sx

        try:
            error += dy / dx
        except ZeroDivisionError:
            error += dy / 1e-10

    return points


# Bresenham integer algorithm
def BresenhamIntegerAlgorithm(x1, y1, x2, y2, color):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, color]]

    # Get sign of dx and dy
    sx = sign(dx)
    sy = sign(dy)

    # Absolute values of dx and dy
    dx = abs(dx)
    dy = abs(dy)

    # Calculate the number of steps
    if dy > dx:
        dx, dy = dy, dx
        exchange = True
    else:
        exchange = False

    # Initialize the error
    error = 2 * dy - dx

    # Set the initial point
    x = x1
    y = y1

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(dx + 1):
        points.append([x, y, color])

        if error >= 0:
            if exchange:
                x += sx
            else:
                y += sy

            error -= 2 * dx

        if exchange:
            y += sy
        else:
            x += sx

        error += 2 * dy

    return points


# Bresenham elimination of aliasing algorithm
def BresenhamEliminationOfAliasingAlgorithm(x1, y1, x2, y2, color):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, color]]

    # Get sign of dx and dy
    sx = sign(dx)
    sy = sign(dy)

    # Absolute values of dx and dy
    dx = abs(dx)
    dy = abs(dy)

    # Calculate the number of steps
    if dy > dx:
        dx, dy = dy, dx
        exchange = True
    else:
        exchange = False

    # Initialize the error
    error = 0.5

    # Initialize the error increment
    try:
        error_inc = dy / dx
    except ZeroDivisionError:
        error_inc = dy / 1e-10

    # Set the initial point
    x = x1
    y = y1

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(dx + 1):
        points.append([x, y, (color[0] + round(255 * error) if color[0] + round(255 * error) < 255 else 255,
                              color[1] + round(255 * error) if color[1] + round(255 * error) < 255 else 255,
                              color[2] + round(255 * error) if color[2] + round(255 * error) < 255 else 255)])

        if error < (1 - error_inc):
            if not exchange:
                x += sx
            else:
                y += sy

            error += error_inc
        else:
            x += sx
            y += sy
            error -= (1 - error_inc)

    return points


# Wu algorithm
def WuAlgorithm(x1, y1, x2, y2, color):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, color]]

    # Initialize the intensity coefficient
    intensity_coefficient = 1

    # Initialize step
    step = 1

    # Create a list of points
    points = []

    if abs(dy) >= abs(dx):
        if dy != 0:
            intensity_coefficient = dx / dy

        temp_intensity_coefficient = intensity_coefficient

        if y1 > y2:
            temp_intensity_coefficient *= -1
            step *= -1

        end = round(y2) - 1 if dy < dx else round(y2) + 1

        for y in range(round(y1), end, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            points.append([int(x1) + 1, y, (color[0] + round(fabs(d2) * 255) if color[0] + round(fabs(d2) * 255) < 255
                                            else 255,
                                            color[1] + round(fabs(d2) * 255) if color[1] + round(fabs(d2) * 255) < 255
                                            else 255,
                                            color[2] + round(fabs(d2) * 255) if color[2] + round(fabs(d2) * 255) < 255
                                            else 255)])
            points.append([int(x1), y, (color[0] + round(fabs(d1) * 255) if color[0] + round(fabs(d1) * 255) < 255
                                        else 255,
                                        color[1] + round(fabs(d1) * 255) if color[1] + round(fabs(d1) * 255) < 255
                                        else 255,
                                        color[2] + round(fabs(d1) * 255) if color[2] + round(fabs(d1) * 255) < 255
                                        else 255)])

            x1 += temp_intensity_coefficient
    else:
        if dx != 0:
            intensity_coefficient = dy / dx

        temp_intensity_coefficient = intensity_coefficient

        if x1 > x2:
            temp_intensity_coefficient *= -1
            step *= -1

        end = round(x2) - 1 if dx < dy else round(x2) + 1

        for x in range(round(x1), end, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            points.append([x, int(y1) + 1, (color[0] + round(fabs(d2) * 255) if color[0] + round(fabs(d2) * 255) < 255
                                            else 255,
                                            color[1] + round(fabs(d2) * 255) if color[1] + round(fabs(d2) * 255) < 255
                                            else 255,
                                            color[2] + round(fabs(d2) * 255) if color[2] + round(fabs(d2) * 255) < 255
                                            else 255)])
            points.append([x, int(y1), (color[0] + round(fabs(d1) * 255) if color[0] + round(fabs(d1) * 255) < 255
                                        else 255,
                                        color[1] + round(fabs(d1) * 255) if color[1] + round(fabs(d1) * 255) < 255
                                        else 255,
                                        color[2] + round(fabs(d1) * 255) if color[2] + round(fabs(d1) * 255) < 255
                                        else 255)])

            y1 += temp_intensity_coefficient

    return points
