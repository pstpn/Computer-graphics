from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys


# Default coordinates
default_coordinates = [(0, 0), (100, 0), (100, 100), (0, 100)]

# Colors code: green, red, blue, purple, yellow
colors = ["#00FF00", "#FF0000", "#0000FF", "#800080", "#FFFF00"]


def ErrorDialog(info):

    # Create a message box
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    # Set the message box text
    msg.setText("Ошибка")
    msg.setInformativeText(info)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    # Show the message box
    msg.exec_()


class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load the UI Interface
        uic.loadUi('Window/Window.ui', self)

        # Set the main field
        self.SetMainField()

        # Set the buttons
        self.ClearAllFields.setShortcut("Ctrl+W")
        self.ClearAllFields.clicked.connect(lambda clear_all: self.DeleteAllFieldsData())
        self.ExecTrans.clicked.connect(lambda draw_figure: self.DrawFigure())
        self.ClearGraph.clicked.connect(lambda delete_graph: self.DeleteGraph())

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(lambda close_app: QtWidgets.qApp.quit())

        # Coordinates of figures
        self.coordinates, self.last_coordinates = [], []

    def SetMainField(self):

        canvas = QtGui.QPixmap(900, 720)
        self.MainField.setPixmap(canvas)

    def DrawFigure(self):

        # Check if the coordinates
        if not self.coordinates:
            self.coordinates = default_coordinates

        # Draw the figure
        for i in range(len(self.coordinates) - 1):
            self.DrawLine(colors[i], self.coordinates[i], self.coordinates[i + 1])

        # Draw the last line
        self.DrawLine(colors[4], self.coordinates[-1], self.coordinates[0])

    def DrawLine(self, color, first_point, second_point):

        # Set the painter
        painter = QtGui.QPainter(self.MainField.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)

        # Draw the first point
        painter.drawLine(first_point[0], first_point[1], second_point[0], second_point[1])

        # Update the field
        self.MainField.update()
        painter.end()

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
        self.MainField.pixmap().fill(QtCore.Qt.black)
        self.MainField.update()

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
