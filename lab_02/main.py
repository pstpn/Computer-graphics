import sys
import copy
import math

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from calculate import RotatePoint, ScalePoint, GetXYParams, GetDXLen, GetDYLen, GetCircleCenter, GetAngle
from tools import ClearCoordinates, DeepCopy, ErrorDialog, PrintTaskInfo, PrintAuthorInfo


# Default coordinates
default_coordinates = {
    "circle": {
        "first_point": [450, 410],
        "second_point": [410, 330],
        "third_point": [490, 330],
        "radius_x": 50,
        "radius_y": 50,
        "points": []
    },
    "line": {
        "first_point": [350, 410],
        "second_point": [550, 410]
    },
    "ellipse": {
        "radius_x": 100,
        "radius_y": 50,
        "points": []
    },
    "left_quad": {
        "first_point": [350, 410],
        "second_point": [450, 277],
        "third_point": [317, 177],
        "fourth_point": [217, 310]
    },
    "right_quad": {
        "first_point": [550, 410],
        "second_point": [450, 277],
        "third_point": [583, 177],
        "fourth_point": [683, 310]
    }
}

# Transfers coordinates to the coordinate system of the canvas
DX, DY = 450, 360

# Colors code: red, purple, yellow
colors = ["#FF0000", "#800080", "#FFFF00"]


# Main window class
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
        self.ClearGraph.clicked.connect(self.DeleteGraphAndCoordinates)
        self.ReturnToPrev.setShortcut("Ctrl+Z")
        self.ReturnToPrev.clicked.connect(self.GoBack)

        self.AuthorInfo.triggered.connect(PrintAuthorInfo)
        self.TaskInfo.triggered.connect(PrintTaskInfo)

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

        # Coordinates of figures
        self.coordinates = {
            "circle": {
                "first_point": [],
                "second_point": [],
                "third_point": [],
                "radius_x": 0,
                "radius_y": 0,
                "points": []
            },
            "line": {
                "first_point": [],
                "second_point": []
            },
            "ellipse": {
                "radius_x": 0,
                "radius_y": 0,
                "points": []
            },
            "left_quad": {
                "first_point": [],
                "second_point": [],
                "third_point": [],
                "fourth_point": []
            },
            "right_quad": {
                "first_point": [],
                "second_point": [],
                "third_point": [],
                "fourth_point": []
            }
        }

        # Last coordinates of figure
        self.last_coordinates = []

    # Set the graph field
    def SetGraphField(self):

        canvas = QtGui.QPixmap(900, 720)
        self.GraphField.setPixmap(canvas)

    # Draw initial figure
    def InitDrawFigure(self):

        # Save coordinates
        self.last_coordinates.append(copy.deepcopy(self.coordinates))

        # Deep copy
        DeepCopy(self.coordinates, default_coordinates)

        # Clear the field
        self.DeleteGraph()

        # Draw figure
        self.DrawFigure()

    # Draw figure
    def DrawFigure(self):

        # Check if the coordinates are empty
        if len(self.coordinates["circle"]["first_point"]) == 0:
            return

        # Draw circle
        self.DrawCircle(colors[0])

        # Draw line
        self.DrawLine(colors[1],
                      self.coordinates["line"]["first_point"],
                      self.coordinates["line"]["second_point"])

        # Draw half ellipse
        self.DrawHalfEllipse(colors[2],
                             self.coordinates["ellipse"]["radius_x"],
                             self.coordinates["ellipse"]["radius_y"])

        # Draw left quadrilateral
        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["first_point"],
                      self.coordinates["left_quad"]["second_point"])

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["second_point"],
                      self.coordinates["left_quad"]["third_point"])

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["third_point"],
                      self.coordinates["left_quad"]["fourth_point"])

        self.DrawLine(colors[1],
                      self.coordinates["left_quad"]["fourth_point"],
                      self.coordinates["left_quad"]["first_point"]
                      )

        # Draw right quadrilateral
        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["first_point"],
                      self.coordinates["right_quad"]["second_point"])

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["second_point"],
                      self.coordinates["right_quad"]["third_point"])

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["third_point"],
                      self.coordinates["right_quad"]["fourth_point"])

        self.DrawLine(colors[1],
                      self.coordinates["right_quad"]["fourth_point"],
                      self.coordinates["right_quad"]["first_point"]
                      )

    # Transfer figure
    def TransferFigure(self, shift):

        # Check if the figure was drawn
        if len(self.coordinates) == 0:
            ErrorDialog("Ошибка переноса",
                        "Невозможно переместить фигуру, так как она не была нарисована",
                        "")
            return

        # Transfer the circle
        self.TransferCircle(shift)

        # Transfer the half ellipse
        self.TransferHalfEllipse(shift)

        # Transfer the line
        self.TransferLine(shift)

        # Transfer the quad
        self.TransferQuad(shift)

    # Transfer the circle
    def TransferCircle(self, shift):

        self.coordinates["circle"]["first_point"][0] += shift[0]
        self.coordinates["circle"]["first_point"][1] -= shift[1]
        self.coordinates["circle"]["second_point"][0] += shift[0]
        self.coordinates["circle"]["second_point"][1] -= shift[1]
        self.coordinates["circle"]["third_point"][0] += shift[0]
        self.coordinates["circle"]["third_point"][1] -= shift[1]

        for i in range(len(self.coordinates["circle"]["points"])):
            self.coordinates["circle"]["points"][i][0] += shift[0]
            self.coordinates["circle"]["points"][i][1] -= shift[1]

    # Transfer the half ellipse
    def TransferHalfEllipse(self, shift):

        for i in range(len(self.coordinates["ellipse"]["points"])):
            self.coordinates["ellipse"]["points"][i][0] += shift[0]
            self.coordinates["ellipse"]["points"][i][1] -= shift[1]

    # Transfer the line
    def TransferLine(self, shift):

        self.coordinates["line"]["first_point"][0] += shift[0]
        self.coordinates["line"]["first_point"][1] -= shift[1]
        self.coordinates["line"]["second_point"][0] += shift[0]
        self.coordinates["line"]["second_point"][1] -= shift[1]

    # Transfer the quad
    def TransferQuad(self, shift):

        self.coordinates["left_quad"]["first_point"][0] += shift[0]
        self.coordinates["left_quad"]["first_point"][1] -= shift[1]
        self.coordinates["left_quad"]["second_point"][0] += shift[0]
        self.coordinates["left_quad"]["second_point"][1] -= shift[1]
        self.coordinates["left_quad"]["third_point"][0] += shift[0]
        self.coordinates["left_quad"]["third_point"][1] -= shift[1]
        self.coordinates["left_quad"]["fourth_point"][0] += shift[0]
        self.coordinates["left_quad"]["fourth_point"][1] -= shift[1]

        self.coordinates["right_quad"]["first_point"][0] += shift[0]
        self.coordinates["right_quad"]["first_point"][1] -= shift[1]
        self.coordinates["right_quad"]["second_point"][0] += shift[0]
        self.coordinates["right_quad"]["second_point"][1] -= shift[1]
        self.coordinates["right_quad"]["third_point"][0] += shift[0]
        self.coordinates["right_quad"]["third_point"][1] -= shift[1]
        self.coordinates["right_quad"]["fourth_point"][0] += shift[0]
        self.coordinates["right_quad"]["fourth_point"][1] -= shift[1]

    # Rotate figure
    def RotateFigure(self, center, angle):

        # Check if the figure was drawn
        if len(self.coordinates) == 0:
            ErrorDialog("Ошибка поворота",
                        "Невозможно повернуть фигуру, так как она не была нарисована",
                        "")
            return

        # Rotate the circle
        self.RotateCircle(center, angle)

        # Rotate the half ellipse
        self.RotateHalfEllipse(center, angle)

        # Rotate the line
        self.RotateLine(center, angle)

        # Rotate the quad
        self.RotateQuad(center, angle)

    # Rotate the circle
    def RotateCircle(self, center, angle):

        self.coordinates["circle"]["first_point"] = \
            RotatePoint(center, self.coordinates["circle"]["first_point"], angle)
        self.coordinates["circle"]["second_point"] = \
            RotatePoint(center, self.coordinates["circle"]["second_point"], angle)
        self.coordinates["circle"]["third_point"] = \
            RotatePoint(center, self.coordinates["circle"]["third_point"], angle)

        for i in range(len(self.coordinates["circle"]["points"])):

            self.coordinates["circle"]["points"][i] = \
                RotatePoint(center, self.coordinates["circle"]["points"][i], angle)

    # Rotate the half ellipse
    def RotateHalfEllipse(self, center, angle):

        for i in range(len(self.coordinates["ellipse"]["points"])):

            self.coordinates["ellipse"]["points"][i] = \
                RotatePoint(center, self.coordinates["ellipse"]["points"][i], angle)

    # Rotate the line
    def RotateLine(self, center, angle):

        self.coordinates["line"]["first_point"] = \
            RotatePoint(center, self.coordinates["line"]["first_point"], angle)
        self.coordinates["line"]["second_point"] = \
            RotatePoint(center, self.coordinates["line"]["second_point"], angle)

    # Rotate the quad
    def RotateQuad(self, center, angle):

        self.coordinates["left_quad"]["first_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["first_point"], angle)
        self.coordinates["left_quad"]["second_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["second_point"], angle)
        self.coordinates["left_quad"]["third_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["third_point"], angle)
        self.coordinates["left_quad"]["fourth_point"] = \
            RotatePoint(center, self.coordinates["left_quad"]["fourth_point"], angle)

        self.coordinates["right_quad"]["first_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["first_point"], angle)
        self.coordinates["right_quad"]["second_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["second_point"], angle)
        self.coordinates["right_quad"]["third_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["third_point"], angle)
        self.coordinates["right_quad"]["fourth_point"] = \
            RotatePoint(center, self.coordinates["right_quad"]["fourth_point"], angle)

    # Scale figure
    def ScaleFigure(self, center, scale):

        # Check if the figure was drawn
        if len(self.coordinates) == 0:
            ErrorDialog("Ошибка масштабирования",
                        "Невозможно масштабировать фигуру, так как она не была нарисована",
                        "")
            return

        # Scale the circle
        self.ScaleCircle(center, scale)

        # Scale the half ellipse
        self.ScaleHalfEllipse(center, scale)

        # Scale the line
        self.ScaleLine(center, scale)

        # Scale the quad
        self.ScaleQuad(center, scale)

    # Scale the circle
    def ScaleCircle(self, center, scale):

        self.coordinates["circle"]["first_point"] = \
            ScalePoint(center, self.coordinates["circle"]["first_point"], scale)
        self.coordinates["circle"]["second_point"] = \
            ScalePoint(center, self.coordinates["circle"]["second_point"], scale)
        self.coordinates["circle"]["third_point"] = \
            ScalePoint(center, self.coordinates["circle"]["third_point"], scale)

        self.coordinates["circle"]["radius_x"] *= scale[0]
        self.coordinates["circle"]["radius_y"] *= scale[1]

        for i in range(len(self.coordinates["circle"]["points"])):

            self.coordinates["circle"]["points"][i] = \
                ScalePoint(center, self.coordinates["circle"]["points"][i], scale)

    # Scale the half ellipse
    def ScaleHalfEllipse(self, center, scale):

        self.coordinates["ellipse"]["radius_x"] *= scale[0]
        self.coordinates["ellipse"]["radius_y"] *= scale[1]

        for i in range(len(self.coordinates["ellipse"]["points"])):

            self.coordinates["ellipse"]["points"][i] = \
                ScalePoint(center, self.coordinates["ellipse"]["points"][i], scale)

    # Scale the line
    def ScaleLine(self, center, scale):

        self.coordinates["line"]["first_point"] = \
            ScalePoint(center, self.coordinates["line"]["first_point"], scale)
        self.coordinates["line"]["second_point"] = \
            ScalePoint(center, self.coordinates["line"]["second_point"], scale)

    # Scale the quad
    def ScaleQuad(self, center, scale):

        if math.fabs(scale[0]) < 1e-8 or math.fabs(scale[1]) < 1e-8:
            scale = [0, 0]

        self.coordinates["left_quad"]["first_point"] = \
            ScalePoint(center, self.coordinates["left_quad"]["first_point"], scale)
        self.coordinates["left_quad"]["second_point"] = \
            ScalePoint(center, self.coordinates["left_quad"]["second_point"], scale)
        self.coordinates["left_quad"]["third_point"] = \
            ScalePoint(center, self.coordinates["left_quad"]["third_point"], scale)
        self.coordinates["left_quad"]["fourth_point"] = \
            ScalePoint(center, self.coordinates["left_quad"]["fourth_point"], scale)

        self.coordinates["right_quad"]["first_point"] = \
            ScalePoint(center, self.coordinates["right_quad"]["first_point"], scale)
        self.coordinates["right_quad"]["second_point"] = \
            ScalePoint(center, self.coordinates["right_quad"]["second_point"], scale)
        self.coordinates["right_quad"]["third_point"] = \
            ScalePoint(center, self.coordinates["right_quad"]["third_point"], scale)
        self.coordinates["right_quad"]["fourth_point"] = \
            ScalePoint(center, self.coordinates["right_quad"]["fourth_point"], scale)

    # Get input angle
    def GetAngle(self):

        # Get angle (string)
        s_angle = self.RotateField.toPlainText()

        # Check skip rotation
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

    # Get input scale
    def GetScale(self):

        # Get scale (string)
        s_scale_x, s_scale_y = self.ScaleXField.toPlainText(), self.ScaleYField.toPlainText()

        # Check skip scaling
        if s_scale_x == s_scale_y == "":
            return [1, 1], False

        # Get scale (float)
        try:
            f_scale_x, f_scale_y = float(s_scale_x), float(s_scale_y)
        except ValueError:
            ErrorDialog("Ошибка получения масштаба",
                        "Значения заданы некорректно",
                        "Ожидались вещественные числа\n(заданы символьные значения)")

            return [], False

        return [f_scale_x, f_scale_y], True

    # Execute transformation of the figure
    def ExecTransFigure(self):

        # Check if the figure was drawn
        if len(self.coordinates["circle"]["first_point"]) == 0:
            ErrorDialog("Ошибка трансформации фигуры",
                        "Невозможно трансформировать фигуру, так как она не была нарисована",
                        "")
            return

        # Save the coordinates
        self.last_coordinates.append(copy.deepcopy(self.coordinates))

        # Get shift
        shift, err = GetXYParams(self.OffsetXField.toPlainText, self.OffsetYField.toPlainText)
        if err == ValueError:
            return

        # Shift the figure
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
            elif len(center) == 0:
                ErrorDialog("Ошибка получения координат",
                            "Координаты центра поворота/масштабирования не были заданы",
                            "Ожидались вещественные значения\n")
                return

            center[0] += DX
            center[1] += DY

            # Rotate the figure
            if len(center) != 0:
                self.RotateFigure(center, input_angle)
            else:
                ErrorDialog("Ошибка получения координат",
                            "Координаты центра поворота/масштабирования не были заданы",
                            "Ожидались целые величины\n")
                return

        # Get input scale
        input_scale, is_correct = self.GetScale()
        if is_correct is not True and len(input_scale) == 0:
            return

        if is_correct is True:

            # Get center
            center, err = GetXYParams(self.CenterXField.toPlainText, self.CenterYField.toPlainText)
            if err == ValueError:
                return
            elif len(center) == 0:
                ErrorDialog("Ошибка получения координат",
                            "Координаты центра поворота/масштабирования не были заданы",
                            "Ожидались вещественные значения\n")
                return

            center[0] += DX
            center[1] += DY

            # Scale the figure
            if len(center) != 0:
                self.ScaleFigure(center, input_scale)
            else:
                ErrorDialog("Ошибка получения координат",
                            "Координаты центра поворота/масштабирования не были заданы",
                            "Ожидались целые величины\n")
                return

        # Clear the field
        self.DeleteGraph()

        # Draw figure
        self.DrawFigure()

    # Draw the line
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

    # Draw the circle
    def DrawCircle(self, color):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Get circle points
        if len(self.coordinates["circle"]["points"]) == 0:

            # Get center
            center = GetCircleCenter(self.coordinates["circle"]["first_point"],
                                     self.coordinates["circle"]["second_point"],
                                     self.coordinates["circle"]["third_point"])

            # Calculate the points
            for i in range(3600):

                self.coordinates["circle"]["points"].append(
                    [center[0] + GetDXLen(self.coordinates["circle"]["radius_x"], i * 0.1),
                     center[1] - GetDYLen(self.coordinates["circle"]["radius_y"], i * 0.1)])

        # Draw the circle
        for i in range(len(self.coordinates["circle"]["points"]) - 1):

            # Draw the line
            painter.drawLine(int(self.coordinates["circle"]["points"][i][0]),
                             int(self.coordinates["circle"]["points"][i][1]),
                             int(self.coordinates["circle"]["points"][i + 1][0]),
                             int(self.coordinates["circle"]["points"][i + 1][1]))

        # Update the field
        self.GraphField.update()
        painter.end()

    # Draw the half ellipse
    def DrawHalfEllipse(self, color, radius_x, radius_y):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        if len(self.coordinates["ellipse"]["points"]) == 0:

            # Get initial point
            last_coord = [self.coordinates["line"]["first_point"][0], self.coordinates["line"]["first_point"][1]]

            # Get center
            center = [last_coord[0] + radius_x, last_coord[1]]

            # Get angle between the center line and the x-axis
            angle = GetAngle(self.coordinates["line"]["second_point"],
                             self.coordinates["line"]["first_point"],
                             center)

            # Check the angle
            if angle < 0 and \
                self.coordinates["line"]["second_point"][1] < self.coordinates["line"]["first_point"][1] or \
                    angle > 0 and \
                    self.coordinates["line"]["second_point"][1] > self.coordinates["line"]["first_point"][1]:
                angle += 180

            # Calculate the points
            for i in range(1800):

                self.coordinates["ellipse"]["points"].append(
                    [center[0] + GetDXLen(radius_x, i * 0.1),
                        center[1] + GetDYLen(radius_y, i * 0.1)])

        # Draw the ellipse
        for i in range(len(self.coordinates["ellipse"]["points"]) - 1):

            # Draw the line
            painter.drawLine(int(self.coordinates["ellipse"]["points"][i][0]),
                             int(self.coordinates["ellipse"]["points"][i][1]),
                             int(self.coordinates["ellipse"]["points"][i + 1][0]),
                             int(self.coordinates["ellipse"]["points"][i + 1][1]))

        # Update the field
        self.GraphField.update()
        painter.end()

    # Back to the previous drawing
    def GoBack(self):

        # Get prev coordinates
        if len(self.last_coordinates) == 0:
            self.DeleteGraph()
            return
        else:
            # Copy the coordinates
            DeepCopy(self.coordinates, self.last_coordinates[-1])
            self.last_coordinates.pop()

        # Clear graph
        self.DeleteGraph()

        # Draw figure
        self.DrawFigure()

    # Clear the fields
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
        self.ScaleXField.clear()
        self.ScaleYField.clear()

    # Clear the graph
    def DeleteGraph(self):

        self.GraphField.pixmap().fill(QtCore.Qt.black)
        self.GraphField.update()

    # Clear the graph and coordinates
    def DeleteGraphAndCoordinates(self):

        # Clear the field
        self.DeleteGraph()

        # Initialize the coordinates
        ClearCoordinates(self.coordinates)


if __name__ == "__main__":

    # Create the Qt Application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    # Run the main Qt loop
    sys.exit(app.exec())
