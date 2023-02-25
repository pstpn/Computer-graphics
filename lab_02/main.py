import math
import sys

from decimal import Decimal
from PyQt5 import QtWidgets, QtCore, QtGui, uic


# Default coordinates
default_coordinates = {
    "circle": {
        "first_point": [450, 410],
        "second_point": [410, 330],
        "third_point": [490, 330],
        "radius": 50,
    },
    "line": {
        "first_point": [350, 410],
        "second_point": [550, 410]
    },
    "ellipse": {
        "radius_x": 100,
        "radius_y": 50
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

# Transfers coordinates to the coordinate system of the canvas
DX, DY = 450, 360

# Colors code: red, purple, yellow
colors = ["#FF0000", "#800080", "#FFFF00"]


# Print error message
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


# Rotate the point around the center
def RotatePoint(center, point, angle):

    return [(Decimal(center[0] + (point[0] - center[0]) * Decimal(math.cos(math.radians(angle)))) +
             Decimal((point[1] - center[1])) *
             Decimal(math.sin(math.radians(angle)))),
            (Decimal(center[1] - (point[0] - center[0]) * Decimal(math.sin(math.radians(angle)))) +
             Decimal((point[1] - center[1])) *
             Decimal(math.cos(math.radians(angle))))]


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

    if int(x) != x or int(y) != y:
        ErrorDialog("Ошибка получения координат",
                    "Координаты заданы некорректно",
                    "Ожидались целые величины\n(заданы вещественные значения)")

        return [], ValueError

    return [int(x) + DX, int(y) + DY], None


# Get the center of the circle
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

    if x1 == x2 or x2 == x3:
        x2 += 1e-11

    m1 = (Decimal((y2 - y1))) / (Decimal((x2 - x1)))
    m2 = (Decimal((y3 - y2))) / (Decimal((x3 - x2)))

    if m1 == 0 or m1 == m2:
        m1 += Decimal(1e-11)

    angle = math.degrees(math.atan((m2 - m1) / (1 + m1 * m2)))

    print("Angle: ", angle)

    return angle


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
                             self.coordinates["ellipse"]["radius_x"],
                             self.coordinates["ellipse"]["radius_y"])

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["first_side"]["first_point"],
                      self.coordinates["left_quad"]["first_side"]["second_point"])

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["first_side"]["second_point"],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["second_point"],
                                  self.coordinates["left_quad"]["first_side"]["first_point"],
                                  -90))

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["first_side"]["first_point"],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["first_point"],
                                  self.coordinates["left_quad"]["first_side"]["second_point"],
                                  90))

        self.DrawLine(colors[1],
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["first_point"],
                                  self.coordinates["left_quad"]["first_side"]["second_point"],
                                  90),
                      RotatePoint(self.coordinates["left_quad"]["first_side"]["second_point"],
                                  self.coordinates["left_quad"]["first_side"]["first_point"],
                                  -90))

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["first_side"]["first_point"],
                      self.coordinates["right_quad"]["first_side"]["second_point"])

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["first_side"]["second_point"],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["second_point"],
                                  self.coordinates["right_quad"]["first_side"]["first_point"],
                                  90))

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["first_side"]["first_point"],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["first_point"],
                                  self.coordinates["right_quad"]["first_side"]["second_point"],
                                  -90))

        self.DrawLine(colors[1],
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["first_point"],
                                  self.coordinates["right_quad"]["first_side"]["second_point"],
                                  -90),
                      RotatePoint(self.coordinates["right_quad"]["first_side"]["second_point"],
                                  self.coordinates["right_quad"]["first_side"]["first_point"],
                                  90))

    def TransferFigure(self, shift):

        # Check if the figure was drawn
        if len(self.coordinates) == 0:
            ErrorDialog("Ошибка переноса",
                        "Невозможно переместить фигуру, так как она не была нарисована",
                        "")
            return

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

        # Check if the figure was drawn
        if len(self.coordinates) == 0:
            ErrorDialog("Ошибка поворота",
                        "Невозможно повернуть фигуру, так как она не была нарисована",
                        "")
            return

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
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Draw the line
        painter.drawLine(int(first_point[0]), int(first_point[1]), int(second_point[0]), int(second_point[1]))

        # Update the field
        self.GraphField.update()
        painter.end()

    def DrawCircle(self, color):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Get center
        center = GetCircleCenter(self.coordinates["circle"]["first_point"],
                                 self.coordinates["circle"]["second_point"],
                                 self.coordinates["circle"]["third_point"])

        # Draw the circle
        last_coord = [center[0] + self.coordinates["circle"]["radius"], center[1]]

        for i in range(3600):
            new_coord = [center[0] + GetDXLen(self.coordinates["circle"]["radius"], i * 0.1),
                         center[1] - GetDYLen(self.coordinates["circle"]["radius"], i * 0.1)]

            # Draw the line
            painter.drawLine(int(last_coord[0]), int(last_coord[1]), int(new_coord[0]), int(new_coord[1]))

            last_coord = new_coord

        # Update the field
        self.GraphField.update()
        painter.end()

    def DrawHalfEllipse(self, color, radius_x, radius_y):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Get initial point
        last_coord = [self.coordinates["line"]["first_point"][0], self.coordinates["line"]["first_point"][1]]

        # Get center
        center = [Decimal(last_coord[0] + radius_x), Decimal(last_coord[1])]

        # Get angle between the center line and the x-axis
        angle = GetAngle(self.coordinates["line"]["second_point"],
                         self.coordinates["line"]["first_point"],
                         center)

        if angle < 0 and self.coordinates["line"]["second_point"][1] < self.coordinates["line"]["first_point"][1] or \
                angle > 0 and self.coordinates["line"]["second_point"][1] > self.coordinates["line"]["first_point"][1]:
            angle += 180

        # Draw the half ellipse
        for i in range(1800):

            new_coord = RotatePoint(
                self.coordinates["line"]["first_point"],
                [center[0] + Decimal(GetDXLen(radius_x, i * 0.1)),
                 center[1] + Decimal(GetDYLen(radius_y, i * 0.1))],
                angle)

            # Draw the line
            painter.drawLine(int(last_coord[0]), int(last_coord[1]), int(new_coord[0]), int(new_coord[1]))

            last_coord = new_coord

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
