from PyQt5 import QtWidgets, QtGui, QtCore, uic
from tools import ErrorDialog, PrintAuthorInfo, PrintTaskInfo, GetColor, GetAlgorithmPoints

import sys


# Main window class
class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load the UI Interface
        uic.loadUi('Window/Window.ui', self)

        # Set the main field
        self.SetGraphField()

        # Set the radio buttons in layouts
        self.BlueColor.setChecked(True)
        self.DDAAlg.setChecked(True)

        # Set the buttons
        self.DrawLine.clicked.connect(self.DrawingLine)
        self.ClearGraph.clicked.connect(self.DeleteGraph)

        self.AuthorInfo.triggered.connect(PrintAuthorInfo)
        self.TaskInfo.triggered.connect(PrintTaskInfo)

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

    # Set the graph field
    def SetGraphField(self):

        canvas = QtGui.QPixmap(900, 720)
        self.GraphField.setPixmap(canvas)
        self.GraphField.pixmap().fill(QtCore.Qt.white)

    # Draw the line
    def DrawingLine(self):

        # Get the color
        color = GetColor(self)

        # Get the input points
        first_point = [self.X1Field.toPlainText(), self.Y1Field.toPlainText()]
        second_point = [self.X2Field.toPlainText(), self.Y2Field.toPlainText()]

        # Check the input points
        if first_point[0] == "" or first_point[1] == "" or second_point[0] == "" or second_point[1] == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Не все поля заполнены!")
            return
        try:
            first_point[0] = int(first_point[0])
            first_point[1] = int(first_point[1])
            second_point[0] = int(second_point[0])
            second_point[1] = int(second_point[1])
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные координаты!")
            return

        # Get points
        points = GetAlgorithmPoints(self,
                                    first_point[0], first_point[1],
                                    second_point[0], second_point[1],
                                    color)

        # Set the painter
        painter = QtGui.QPainter(self.GraphField.pixmap())
        pen = QtGui.QPen()

        # Draw using library function
        if len(points) == 0:
            pen.setColor(QtGui.QColor(*color))
            painter.setPen(pen)
            painter.drawLine(int(first_point[0]), int(first_point[1]), int(second_point[0]), int(second_point[1]))
        else:
            for point in points:
                pen.setColor(QtGui.QColor(*point[2]))
                painter.setPen(pen)
                painter.drawPoint(int(point[0]), int(point[1]))

        # Update the field
        self.GraphField.update()
        painter.end()

    # Clear the graph
    def DeleteGraph(self):

        self.GraphField.pixmap().fill(QtCore.Qt.white)
        self.GraphField.update()


if __name__ == "__main__":

    # Create the Qt Application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    # Run the main Qt loop
    sys.exit(app.exec())
