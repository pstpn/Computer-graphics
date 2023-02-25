import math

from tools import ErrorDialog


# Rotate the point around the center
def RotatePoint(center, point, angle):

    return [(center[0] + (point[0] - center[0]) * math.cos(math.radians(angle)) +
             (point[1] - center[1]) *
             math.sin(math.radians(angle))),
            (center[1] - (point[0] - center[0]) * math.sin(math.radians(angle)) +
             (point[1] - center[1]) *
             math.cos(math.radians(angle)))]


# Scale the point around the center
def ScalePoint(center, point, scale):

    return [(point[0] - center[0]) * scale[0] + center[0],
            (point[1] - center[1]) * scale[1] + center[1]]


# Get the coordinates of the point
def GetXYParams(func_x, func_y):

    tmp_x = func_x()
    tmp_y = func_y()

    if tmp_y == tmp_x == "":
        return [], None

    # Get coordinates
    try:
        x, y = float(tmp_x), float(tmp_y)
    except ValueError:
        ErrorDialog("Ошибка получения координат",
                    "Координаты заданы некорректно",
                    "Ожидались целые величины\n(заданы символьные значения)")

        return [], ValueError

    return [int(x), int(y)], None


# Get the center of the circle
def GetCircleCenter(first_point, second_point, third_point):

    x1, y1 = first_point
    x2, y2 = second_point
    x3, y3 = third_point

    # Check for the possibility of a circle
    if x3 == x2 or x2 == x1:
        x2 += 1e-11

    # Calculate the slopes of the lines
    m1 = (y2 - y1) / (x2 - x1)
    m2 = (y3 - y2) / (x3 - x2)

    # Check for the possibility of a circle
    if m1 == 0 or m1 == m2:
        m1 += 1e-11

    # Calculate the center of the circle
    xc = (m1 * m2 * (y1 - y3) + m2 * (x1 + x2) - m1 * (x2 + x3)) / (2 * (m2 - m1))
    yc = (-1 / m1) * (xc - (x1 + x2) / 2) + (y1 + y2) / 2

    return [int(xc), int(yc)]


# Get the length of the vector in the X direction
def GetDXLen(input_len, angle):

    return input_len * math.cos(angle * math.pi / 180.0)


# Get the length of the vector in the Y direction
def GetDYLen(input_len, angle):

    return input_len * math.sin(angle * math.pi / 180.0)


# Get angle between two lines
def GetAngle(first_point, second_point, third_point):

    x1, y1 = first_point
    x2, y2 = second_point
    x3, y3 = third_point

    # Check for the possibility of the angle
    if x1 == x2 or x2 == x3:
        x2 += 1e-11

    # Calculate the slopes of the lines
    m1 = (y2 - y1) / (x2 - x1)
    m2 = (y3 - y2) / (x3 - x2)

    # Check for the possibility of the angle
    if m1 == 0 or m1 == m2:
        m1 += 1e-11

    return math.degrees(math.atan((m2 - m1) / (1 + m1 * m2)))
