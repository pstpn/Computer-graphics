import math
from decimal import Decimal

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

# Default coordinates
default_coordinates = {
    "circle": {
        "first_point": [450, 410],
        "second_point": [410, 330],
        "third_point": [490, 330],
    },
    "line": {
        "first_point": [350, 410],
        "second_point": [550, 410]
    },
    "ellipse": {
        "center": [350, 360],
        "radius_x": 200,
        "radius_y": 100
    },
    "left_quad": {
        "first_side": {
            "first_point": [350, 410],
            "second_point": [450, 277]
        }
    },
    "right_quad": {
        "first_side": {
            "first_point": [550, 410],
            "second_point": [450, 277]
        }
    }
}

# Colors code: green, red, blue, purple, yellow
colors = ["#00FF00", "#FF0000", "#0000FF", "#800080", "#FFFF00"]


def ErrorDialog(title, name, info):

    # Create a message box
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    # Set the message box text
    msg.setText(name)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    # Show the message box
    msg.exec_()


def RotatePoint(center, point, angle):

    return [int((Decimal(center[0] + (point[0] - center[0]) * Decimal(math.cos(math.radians(angle)))) + Decimal((point[1] - center[1])) *
                Decimal(math.sin(math.radians(angle))))),
            int((Decimal(center[1] - (point[0] - center[0]) * Decimal(math.sin(math.radians(angle)))) + Decimal((point[1] - center[1])) *
                Decimal(math.cos(math.radians(angle)))))]


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

    if int(x) != x or int(y) != y:
        ErrorDialog("Ошибка получения координат",
                    "Координаты заданы некорректно",
                    "Ожидались целые величины\n(заданы вещественные значения)")

        return [], ValueError

    return [int(x), int(y)], None


def GetCircleCenter(first_point, second_point, third_point):

    x1, y1 = first_point
    x2, y2 = second_point
    x3, y3 = third_point

    if x3 == x2 or x2 == x1:
        x2 += 1e-11

    m1 = (Decimal((y2 - y1))) / (Decimal((x2 - x1)))
    m2 = (Decimal((y3 - y2))) / (Decimal((x3 - x2)))

    if m1 == 0 or m1 == m2:
        m1 += Decimal(1e-11)

    xc = (Decimal((m1 * m2 * (y1 - y3) + m2 * (x1 + x2) - m1 * (x2 + x3)))) / (Decimal(2 * (m2 - m1)))
    yc = (Decimal(-1 / m1)) * (Decimal(xc - Decimal(Decimal((x1 + x2)) / 2))) + Decimal(Decimal((y1 + y2)) / 2)

    return [int(xc - 50), int(yc - 50)]


def GetCircleRadius(first_point, second_point, third_point, center):

    r1 = Decimal(math.sqrt(Decimal((first_point[0] - center[0]) ** 2) + Decimal((first_point[1] - center[1]) ** 2)))
    r2 = Decimal(math.sqrt(Decimal((second_point[0] - center[0]) ** 2) + Decimal((second_point[1] - center[1]) ** 2)))
    r3 = Decimal(math.sqrt(Decimal((third_point[0] - center[0]) ** 2) + Decimal((third_point[1] - center[1]) ** 2)))

    return int(max(r1, r2, r3))


class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load the UI Interface
        uic.loadUi('Window/Window.ui', self)

        # Set the main field
        self.SetGraphField()

        # Set the buttons
        self.ClearAllFields.setShortcut("Ctrl+W")
        self.ClearAllFields.clicked.connect(self.DeleteAllFieldsData)
        self.ExecTrans.clicked.connect(self.ExecTransFigure)
        self.DrawInitFigure.clicked.connect(self.InitDrawFigure)
        self.ClearGraph.clicked.connect(self.DeleteGraph)
        self.ReturnToPrev.setShortcut("Ctrl+Z")
        self.ReturnToPrev.clicked.connect(self.GoBack)

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

        # Coordinates of figures
        self.coordinates, self.last_coordinates = {}, []

    def SetGraphField(self):

        canvas = QtGui.QPixmap(900, 720)
        self.GraphField.setPixmap(canvas)

    def InitDrawFigure(self):

        # Save coordinates
        if len(self.last_coordinates) != 0:
            self.last_coordinates.append(self.coordinates)

        self.coordinates = default_coordinates

        # Draw figure
        self.DrawFigure()

    def DrawFigure(self):

        if len(self.coordinates) == 0:
            return

        # Draw the figure
        self.DrawCircle(colors[0])

        self.DrawLine(colors[1],
                      self.coordinates["line"]["first_point"],
                      self.coordinates["line"]["second_point"])

        self.DrawHalfEllipse(colors[2],
                             self.coordinates["ellipse"]["center"],
                             self.coordinates["ellipse"]["radius_x"],
                             self.coordinates["ellipse"]["radius_y"])

        self.DrawLine(colors[3],
                      self.coordinates["left_quad"]["first_side"]["first_point"],
                      self.coordinates["left_quad"]["first_side"]["second_point"])

        self.DrawLine(colors[3],
                      self.coordinates["left_quad"]["first_side"]["second_point"],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["second_point"],
                                  self.coordinates["left_quad"]["first_side"]["first_point"],
                                  -90))

        self.DrawLine(colors[3],
                      self.coordinates["left_quad"]["first_side"]["first_point"],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["first_point"],
                                  self.coordinates["left_quad"]["first_side"]["second_point"],
                                  90))

        self.DrawLine(colors[3],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["first_point"],
                                  self.coordinates["left_quad"]["first_side"]["second_point"],
                                  90),
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["second_point"],
                                  self.coordinates["left_quad"]["first_side"]["first_point"],
                                  -90))

        self.DrawLine(colors[3],
                      self.coordinates["right_quad"]["first_side"]["first_point"],
                      self.coordinates["right_quad"]["first_side"]["second_point"])

        self.DrawLine(colors[3],
                      self.coordinates["right_quad"]["first_side"]["second_point"],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["second_point"],
                                  self.coordinates["right_quad"]["first_side"]["first_point"],
                                  90))

        self.DrawLine(colors[3],
                      self.coordinates["right_quad"]["first_side"]["first_point"],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["first_point"],
                                  self.coordinates["right_quad"]["first_side"]["second_point"],
                                  -90))

        self.DrawLine(colors[3],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["first_point"],
                                  self.coordinates["right_quad"]["first_side"]["second_point"],
                                  -90),
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["second_point"],
                                  self.coordinates["right_quad"]["first_side"]["first_point"],
                                  90))

    def TransferFigure(self, shift):

        self.coordinates["circle"]["first_point"][0] += shift[0]
        self.coordinates["circle"]["first_point"][1] -= shift[1]
        self.coordinates["circle"]["second_point"][0] += shift[0]
        self.coordinates["circle"]["second_point"][1] -= shift[1]
        self.coordinates["circle"]["third_point"][0] += shift[0]
        self.coordinates["circle"]["third_point"][1] -= shift[1]

        self.coordinates["line"]["first_point"][0] += shift[0]
        self.coordinates["line"]["first_point"][1] -= shift[1]
        self.coordinates["line"]["second_point"][0] += shift[0]
        self.coordinates["line"]["second_point"][1] -= shift[1]

        self.coordinates["ellipse"]["center"][0] += shift[0]
        self.coordinates["ellipse"]["center"][1] -= shift[1]

        self.coordinates["left_quad"]["first_side"]["first_point"][0] += shift[0]
        self.coordinates["left_quad"]["first_side"]["first_point"][1] -= shift[1]
        self.coordinates["left_quad"]["first_side"]["second_point"][0] += shift[0]
        self.coordinates["left_quad"]["first_side"]["second_point"][1] -= shift[1]

        self.coordinates["right_quad"]["first_side"]["first_point"][0] += shift[0]
        self.coordinates["right_quad"]["first_side"]["first_point"][1] -= shift[1]
        self.coordinates["right_quad"]["first_side"]["second_point"][0] += shift[0]
        self.coordinates["right_quad"]["first_side"]["second_point"][1] -= shift[1]

    def RotateFigure(self, center, angle):

        self.coordinates["circle"]["first_point"] = \
            RotatePoint(center, self.coordinates["circle"]["first_point"], angle)
        self.coordinates["circle"]["second_point"] = \
            RotatePoint(center, self.coordinates["circle"]["second_point"], angle)
        self.coordinates["circle"]["third_point"] = \
            RotatePoint(center, self.coordinates["circle"]["third_point"], angle)

        self.coordinates["line"]["first_point"] = \
            RotatePoint(center, self.coordinates["line"]["first_point"], angle)
        self.coordinates["line"]["second_point"] = \
            RotatePoint(center, self.coordinates["line"]["second_point"], angle)

        self.coordinates["ellipse"]["center"] = \
            RotatePoint(center, self.coordinates["ellipse"]["center"], angle)

        self.coordinates["left_quad"]["first_side"]["first_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["first_side"]["first_point"], angle)
        self.coordinates["left_quad"]["first_side"]["second_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["first_side"]["second_point"], angle)

        self.coordinates["right_quad"]["first_side"]["first_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["first_side"]["first_point"], angle)
        self.coordinates["right_quad"]["first_side"]["second_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["first_side"]["second_point"], angle)

    def GetAngle(self):

        # Get angle (string)
        s_angle = self.RotateField.toPlainText()

        if s_angle == "":
            return 0, False

        # Get angle (float)
        try:
            f_angle = float(s_angle)
        except ValueError:
            ErrorDialog("Ошибка получения угла",
                        "Значение задано некорректно",
                        "Ожидалось вещественное число\n(задано символьное значение)")

            return -1, False

        return f_angle, True

    def ExecTransFigure(self):

        # Get shift
        shift, err = GetXYParams(self.OffsetXField.toPlainText, self.OffsetYField.toPlainText)
        if err == ValueError:
            return

        if len(shift) != 0:
            self.TransferFigure(shift)

        # Get input angle
        input_angle, is_correct = self.GetAngle()
        if is_correct is not True and input_angle == -1:
            return

        if is_correct is True:

            # Get center
            center, err = GetXYParams(self.CenterXField.toPlainText, self.CenterYField.toPlainText)
            if err == ValueError:
                return

            if len(center) != 0:
                self.RotateFigure(center, input_angle)
            else:
                ErrorDialog("Ошибка получения координат",
                            "Координаты центра поворота/масштабирования не были заданы",
                            "Ожидались целые величины\n")
                return

        # Очистить поле и нарисовать фигуру после всех преобразований

        tmp_coordinates = self.coordinates
        self.DeleteGraph()
        self.coordinates = tmp_coordinates

        # Draw figure
        self.DrawFigure()

        self.last_coordinates.append(self.coordinates)

    def DrawLine(self, color, first_point, second_point):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Draw the line
        painter.drawLine(first_point[0], first_point[1], second_point[0], second_point[1])

        # Update the field
        self.GraphField.update()
        painter.end()

    def DrawCircle(self, color):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Get center
        center = GetCircleCenter(self.coordinates["circle"]["first_point"],
                                 self.coordinates["circle"]["second_point"],
                                 self.coordinates["circle"]["third_point"])

        # Get radius
        radius = GetCircleRadius(self.coordinates["circle"]["first_point"],
                                 self.coordinates["circle"]["second_point"],
                                 self.coordinates["circle"]["third_point"],
                                 center) + 25

        # Draw the circle
        painter.drawEllipse(center[0], center[1], radius, radius)

        # Update the field
        self.GraphField.update()
        painter.end()

    def DrawHalfEllipse(self, color, center, radius_x, radius_y):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Draw the half ellipse
        painter.drawArc(center[0], center[1], radius_x, radius_y, 0, -180 * 16)

        # Update the field
        self.GraphField.update()
        painter.end()

    def GoBack(self):

        # Get prev coordinates
        try:
            self.coordinates = self.last_coordinates.pop()
        except IndexError:
            self.DeleteGraph()
            return

        # Clear graph
        tmp_coordinates = self.coordinates
        self.DeleteGraph()
        self.coordinates = tmp_coordinates

        # Draw figure
        self.DrawFigure()

    def DeleteAllFieldsData(self):

        # Clear center coordinates fields
        self.CenterXField.clear()
        self.CenterYField.clear()

        # Clear offset coordinates fields
        self.OffsetXField.clear()
        self.OffsetYField.clear()

        # Clear rotate angle field
        self.RotateField.clear()

        # Clear scaling field
        self.ScalingField.clear()

    def DeleteGraph(self):

        # Clear the graph
        self.GraphField.pixmap().fill(QtCore.Qt.black)
        self.GraphField.update()

        # Save coordinates
        self.last_coordinates.append(self.coordinates)

        # Clear coordinates
        self.coordinates = {}


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    # Run the main Qt loop
    sys.exit(app.exec())
