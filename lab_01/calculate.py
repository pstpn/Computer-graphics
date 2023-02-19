import math


# Get the angle between the line and the y-axis
def GetAngle(x1, y1, x2, y2):

    angle = math.degrees(math.atan2(abs(y2 - y1), abs(x2 - x1)))

    return 180 - angle if angle > 90 else 90 - angle


# Get the distance between two points
def GetDistance(x1, y1, x2, y2):

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Get the solution of the system of linear equations
def GetSystemSolution(a, b, c, d, e, f):

    # Get the determinant of the matrix
    det = a * d - b * c

    if det == 0:
        return None, None

    # Get the solution of the system of linear equations
    x = (e * d - b * f) / det
    y = (a * f - e * c) / det

    return x, y


# Get the maximum angle between the line and the y-axis
def GetMaxAngle(points, x_c, y_c):

    max_angle = 0
    max_angle_points = []

    # Coordinates of the point of intersection of the heights
    x_i, y_i = None, None

    for i in points.keys():
        for j in range(i + 1, len(points) + 1):
            for k in range(j + 1, len(points) + 1):

                # Get coordinates of the triangle vertices
                xa, ya, xb, yb, xc, yc = \
                    points[i][0], points[i][1], \
                    points[j][0], points[j][1], \
                    points[k][0], points[k][1]

                # Get the equation of the first height
                a1 = xc - xb
                b1 = yc - yb
                c1 = xa * (xc - xb) + ya * (yc - yb)

                # Get the equation of the second height
                a2 = xc - xa
                b2 = yc - ya
                c2 = xb * (xc - xa) + yb * (yc - ya)

                # Get the coordinates of the point of intersection of the heights
                x_i, y_i = GetSystemSolution(a1, b1, a2, b2, c1, c2)

                if x_i is None or y_i is None:
                    continue

                # Get the angle between the line and the y-axis
                angle = GetAngle(x_c, y_c, x_i, y_i)

                if angle > max_angle:
                    max_angle = angle
                    max_angle_points = [points[i], points[j], points[k]]

    return max_angle, max_angle_points, (x_i, y_i)
