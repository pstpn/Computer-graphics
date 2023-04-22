from math import floor, fabs


# Adding intensity
def addingIntensity(color, intensity):
    return color + (intensity, )


# Get sign of number
def sign(x):

    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# Digital Differential Analyzer Algorithm
def DDAAlgorithm(x1, y1, x2, y2, color, calculate_steps=False):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[round(x1), round(y1), addingIntensity(color, 100)]]

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
    tmp_x = x
    tmp_y = y
    count_steps = 0

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(int(steps)):
        if calculate_steps:
            tmp_x = x
            tmp_y = y

        x += x_inc
        y += y_inc

        if not calculate_steps:
            points.append([round(x), round(y), addingIntensity(color, 100)])
        elif round(tmp_x) != round(x) and round(tmp_y) != round(y):
            count_steps += 1

    return points if not calculate_steps else count_steps


# Bresenham float algorithm
def BresenhamFloatAlgorithm(x1, y1, x2, y2, color, calculate_steps=False):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, addingIntensity(color, 100)]]

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
    error = dy / dx - 0.5

    # Set the initial point
    x = x1
    y = y1
    tmp_x = x
    tmp_y = y
    count_steps = 0

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(int(dx + 1)):
        if not calculate_steps:
            points.append([x, y, addingIntensity(color, 100)])

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

        error += dy / dx

        if calculate_steps:
            if tmp_x != x and tmp_y != y:
                count_steps += 1

            tmp_x = x
            tmp_y = y

    return points if not calculate_steps else count_steps


# Bresenham integer algorithm
def BresenhamIntegerAlgorithm(x1, y1, x2, y2, color, calculate_steps=False):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, addingIntensity(color, 100)]]

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
    tmp_x = x
    tmp_y = y
    count_steps = 0

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(int(dx + 1)):
        if not calculate_steps:
            points.append([x, y, addingIntensity(color, 100)])

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

        if calculate_steps:
            if tmp_x != x and tmp_y != y:
                count_steps += 1

            tmp_x = x
            tmp_y = y

    return points if not calculate_steps else count_steps


# Bresenham's elimination of aliasing algorithm
def BresenhamEliminationOfAliasingAlgorithm(x1, y1, x2, y2, color, calculate_steps=False):

    # Calculate dx and dy
    dx = x2 - x1
    dy = y2 - y1

    # If dx and dy are equal to zero, then the line is a point
    if dx == 0 and dy == 0:
        return [[x1, y1, addingIntensity(color, 100)]]

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
    error_inc = dy / dx

    # Set the initial point
    x = x1
    y = y1
    tmp_x = x
    tmp_y = y
    count_steps = 0

    # Create a list of points
    points = []

    # Calculate the points
    for i in range(int(dx + 1)):
        if not calculate_steps:
            points.append([x, y, addingIntensity(color, round(200 * error))])

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

        if calculate_steps:
            if tmp_x != x and tmp_y != y:
                count_steps += 1

            tmp_x = x
            tmp_y = y

    return points if not calculate_steps else count_steps


# Wu algorithm
def WuAlgorithm(x1, y1, x2, y2, color, calculate_steps=False):

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
    count_steps = 0

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

            if not calculate_steps:
                points.append([int(x1) + 1, y, addingIntensity(color, round(fabs(d1) * 100))])
                points.append([int(x1), y, addingIntensity(color, round(fabs(d2) * 100))])
            elif y < round(y2) and int(x1) != int(x1 + intensity_coefficient):
                count_steps += 1

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

            if not calculate_steps:
                points.append([x, int(y1) + 1, addingIntensity(color, round(fabs(d1) * 100))])
                points.append([x, int(y1), addingIntensity(color, round(fabs(d2) * 100))])
            elif x < round(x2) and int(y1) != int(y1 + intensity_coefficient):
                count_steps += 1

            y1 += temp_intensity_coefficient

    return points if not calculate_steps else count_steps


# Library algorithm
def LibAlgorithm(x1, y1, x2, y2, color):
    return [[round(x1), round(y1), addingIntensity(color, 100)],
            [round(x2), round(y2), addingIntensity(color, 100)]]
