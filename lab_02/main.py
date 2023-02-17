import math

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys


# Default coordinates
default_coordinates = {
    "circle": {
        "center": [400, 310],
        "radius": 100
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
            "second_point": [450, 276]
        }
    },
    "right_quad": {
        "first_side": {
            "first_point": [550, 410],
            "second_point": [450, 276]
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
    return [int(center[0] + (point[0] - center[0]) * math.cos(math.radians(angle)) + (point[1] - center[1]) *
                math.sin(math.radians(angle))),
            int(center[1] - (point[0] - center[0]) * math.sin(math.radians(angle)) + (point[1] - center[1]) *
                math.cos(math.radians(angle)))]


class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load the UI Interface
        uic.loadUi('Window/Window.ui', self)

        # Set the main field
        self.SetGraphField()

        # Set the buttons
        self.ClearAllFields.setShortcut("Ctrl+W")
        self.ClearAllFields.clicked.connect(lambda clear_all: self.DeleteAllFieldsData())
        self.ExecTrans.clicked.connect(lambda draw_figure: self.ExecTransFigure())
        self.DrawInitFigure.clicked.connect(lambda draw_figure: self.InitDrawFigure())
        self.ClearGraph.clicked.connect(lambda delete_graph: self.DeleteGraph())
        self.ReturnToPrev.setShortcut("Ctrl+Z")
        self.ReturnToPrev.clicked.connect(lambda go_back: self.GoBack())

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(lambda close_app: QtWidgets.qApp.quit())

        # Coordinates of figures
        self.coordinates, self.last_coordinates = {}, []

    def SetGraphField(self):

        canvas = QtGui.QPixmap(900, 720)
        self.GraphField.setPixmap(canvas)

    def InitDrawFigure(self):

        # Save coordinates
        self.last_coordinates.append(self.coordinates)
        self.coordinates = default_coordinates

        # Draw figure
        self.DrawFigure()

    def DrawFigure(self):

        if not self.coordinates:
            self.coordinates = default_coordinates

        # Draw the figure
        self.DrawCircle(colors[0],
                        self.coordinates["circle"]["center"],
                        self.coordinates["circle"]["radius"])

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

    def GetXYParams(self, func_x, func_y):

        tmp_x = func_x()
        tmp_y = func_y()

        if tmp_y == tmp_x == "":
            return [], None

        x, y = float(), float()

        # Get coordinates
        try:
            x, y = float(tmp_x), float(tmp_y)
        except ValueError:
            ErrorDialog("Ошибка получения координат",
                        "Координаты центра масштабирования/поворота заданы некорректно",
                        "Ожидались целые величины\n(заданы символьные значения)")

            return [], ValueError

        if int(x) != x or int(y) != y:
            ErrorDialog("Ошибка получения координат",
                        "Координаты центра масштабирования/поворота заданы некорректно",
                        "Ожидались целые величины\n(заданы вещественные значения)")

            return [], ValueError

        return [int(x), int(y)], None

    def ExecTransFigure(self):

        # Get shift
        shift, err = self.GetXYParams(self.OffsetXField.toPlainText, self.OffsetYField.toPlainText)
        if err == ValueError:
            return
        elif len(shift) == 0:
            print("Skip")

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

    def DrawCircle(self, color, center, radius):

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

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
            self.coordinates = default_coordinates

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
        self.last_coordinates = self.coordinates

        # Clear coordinates
        self.coordinates = []


if __name__ == "__main__":

    # Create the Qt Application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    # Run the main Qt loop
    sys.exit(app.exec())
