# На плоскости дано множество точек.
# Найти такой треугольник с вершинами в этих точках, у которого угол, образованный прямой, соединяющей точку пересечения
# высот и начало координат, и осью ординат максимален.
# Входные данные: в первой строке задано количество точек n (3 ≤ n ≤ 1000). В следующих n строках заданы координаты точек.
# Выходные данные: в первой строке выведите значение максимального угла в градусах. Во второй строке выведите координаты
# вершин треугольника в порядке обхода против часовой стрелки, начиная с вершины, соответствующей максимальному углу.
# Пример входных данных:
# 4
# 0 0
# 1 0
# 0 1
# 1 1
# Пример выходных данных:
# 45.00000000000001
# 0 0
# 1 0
# 0 1

import math


def GetAngle(x1, y1, x2, y2):

    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def GetDistance(x1, y1, x2, y2):

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def GetMaxAngle(points):

    max_angle = 0
    max_angle_points = []
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                a = GetDistance(points[i][0], points[i][1], points[j][0], points[j][1])
                b = GetDistance(points[i][0], points[i][1], points[k][0], points[k][1])
                c = GetDistance(points[j][0], points[j][1], points[k][0], points[k][1])

                p = (a + b + c) / 2
                s = math.sqrt(p * (p - a) * (p - b) * (p - c))
                h = 2 * s / a

                x = points[i][0] + (points[j][0] - points[i][0]) * h / a
                y = points[i][1] + (points[j][1] - points[i][1]) * h / a

                angle = GetAngle(x, y, points[i][0], points[i][1])

                if angle > max_angle:
                    max_angle = angle
                    max_angle_points = [points[i], points[j], points[k]]

    return max_angle, max_angle_points
