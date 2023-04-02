from PyQt5 import uic
from matplotlib import pyplot as plt
from time import time
from tools import *

import math
import sys

runs_count = 30


class PaintWidget(QtWidgets.QWidget):
    def __init__(self, parent):

        super().__init__(parent)

        self.qp = QtGui.QPainter()

        self.setFixedSize(900, 720)

        self.lineColor = None
        self.backgroundColor = None

        self.setLineColor()
        self.setBackgroundColor()

        self.lines = []
        self.spectra = []

    def setLineColor(self, color=QtGui.QColor(0, 0, 0)):
        self.lineColor = color

    def setBackgroundColor(self, color=QtGui.QColor(255, 255, 255)):
        self.backgroundColor = color

    def paintEvent(self, event: QtGui.QPaintEvent):

        self.qp.begin(self)

        # Clear the field
        self.qp.fillRect(0, 0, self.width(), self.height(), self.backgroundColor)

        if self.lines:
            for line in self.lines:
                self.drawLine(line)

        if self.spectra:
            for spectrum in self.spectra:
                self.drawSpectrum(spectrum)

        self.qp.end()

    def drawLine(self, points):

        # Draw using library function
        if points[-1]:
            self.qp.setPen(QtGui.QPen(self.backgroundColor, 1))
            self.qp.drawLine(int(points[0][0]), int(points[0][1]),
                             int(points[1][0]), int(points[1][1]))
            self.qp.setPen(QtGui.QPen(self.lineColor, 1))
            self.qp.drawLine(int(points[0][0]), int(points[0][1]),
                             int(points[1][0]), int(points[1][1]))
        else:
            for point in points[:-1]:
                self.qp.setPen(QtGui.QPen(self.backgroundColor, 1))
                self.qp.drawPoint(int(point[0]), int(point[1]))
                color = GetQColor(point[2])
                self.qp.setPen(QtGui.QPen(color, 1))
                self.qp.drawPoint(int(point[0]), int(point[1]))

    def drawSpectrum(self, spectra: list):

        for line in spectra:
            self.drawLine(line)

    def clear(self):

        self.lines = []
        self.spectra = []

        self.update()


# Main window class
class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load the UI Interface
        uic.loadUi('Window/Window.ui', self)

        # Create a paint widget
        self.paintWidget = PaintWidget(self.GraphField)

        # Set the radio buttons in layouts
        self.BlueColor.setChecked(True)
        self.WhiteColor_2.setChecked(True)
        self.DDAAlg.setChecked(True)

        # Set actions on lines color radio buttons
        self.BlueColor.clicked.connect(self.SetLineColor)
        self.GreenColor.clicked.connect(self.SetLineColor)
        self.RedColor.clicked.connect(self.SetLineColor)
        self.YellowColor.clicked.connect(self.SetLineColor)
        self.WhiteColor.clicked.connect(self.SetLineColor)
        self.PurpleColor.clicked.connect(self.SetLineColor)

        # Set actions on background color radio buttons
        self.BlueColor_2.clicked.connect(self.SetGraphFieldBackground)
        self.GreenColor_2.clicked.connect(self.SetGraphFieldBackground)
        self.RedColor_2.clicked.connect(self.SetGraphFieldBackground)
        self.YellowColor_2.clicked.connect(self.SetGraphFieldBackground)
        self.WhiteColor_2.clicked.connect(self.SetGraphFieldBackground)
        self.PurpleColor_2.clicked.connect(self.SetGraphFieldBackground)

        # Set the main field
        self.SetGraphFieldBackground()

        # Set the buttons
        self.DrawLine.clicked.connect(self.DrawingLine)
        self.DrawSpectrum.clicked.connect(self.DrawingSpectrum)
        self.TimeCompare.clicked.connect(self.TimeComparing)
        self.SteppingCompare.clicked.connect(self.SteppingComparing)
        self.ClearGraph.clicked.connect(self.DeleteGraph)

        self.AuthorInfo.triggered.connect(PrintAuthorInfo)
        self.TaskInfo.triggered.connect(PrintTaskInfo)

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

    # Set the line color
    def SetLineColor(self):

        # Get the line color
        line_color = GetLineColor(self)

        # Save color
        self.paintWidget.lineColor = line_color

        # Set the line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

    # Set the graph field background color
    def SetGraphFieldBackground(self):

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Get Qt color
        background_color = GetQColor(background_color)

        # Save color
        self.paintWidget.backgroundColor = background_color

        # Set the background color
        self.GraphField.setStyleSheet("background-color: rgb({}, {}, {});".format(background_color.getRgb()[0],
                                                                                  background_color.getRgb()[1],
                                                                                  background_color.getRgb()[2]))

    # Draw the line
    def DrawingLine(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

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
        points, is_lib_alg = GetAlgorithmPoints(self,
                                                first_point[0], first_point[1],
                                                second_point[0], second_point[1],
                                                line_color)

        # Draw the points
        points.append(is_lib_alg)

        # Add the line to the list
        self.paintWidget.lines.append(points)
        self.paintWidget.update()

    # Draw the spectra
    def DrawingSpectrum(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

        # Get the center
        center = [self.CenterX.toPlainText(), self.CenterY.toPlainText()]

        # Get the length
        length = self.LenField.toPlainText()

        # Get the angle
        angle = self.AngleField.toPlainText()

        # Check the input data
        if center[0] == "" or center[1] == "" or length == "" or angle == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Не все поля заполнены!")
            return

        try:
            center[0] = int(center[0])
            center[1] = int(center[1])
            length = float(length)
            angle = float(angle)
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные данные!")
            return

        # Init current angle and spectrum
        current_angle = 0
        current_spectrum = []

        # Draw the spectra
        while current_angle < 360:
            # Get points
            points, is_lib_alg = GetAlgorithmPoints(self,
                                                    center[0], center[1],
                                                    center[0] + length * math.cos(math.radians(current_angle)),
                                                    center[1] + length * math.sin(math.radians(current_angle)),
                                                    line_color)

            # Draw the points
            points.append(is_lib_alg)

            current_spectrum.append(points)

            # Update the angle
            current_angle += angle

        self.paintWidget.spectra.append(current_spectrum)
        self.paintWidget.update()

    # Compare the time
    def TimeComparing(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

        # Get the center
        center = [self.CenterX.toPlainText(), self.CenterY.toPlainText()]

        # Get the length
        length = self.LenField.toPlainText()

        # Get the angle
        angle = self.AngleField.toPlainText()

        # Check the input data
        if center[0] == "" or center[1] == "" or length == "" or angle == "":
            ErrorDialog("Ошибка", "Ошибка замеров", "Не все поля заполнены!")
            return

        try:
            center[0] = int(center[0])
            center[1] = int(center[1])
            length = float(length)
            angle = float(angle)
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка замеров", "Введены некорректные данные!")
            return

        # Init times list
        times = []

        # Get the time
        for alg in [DDAAlgorithm, BresenhamFloatAlgorithm, BresenhamIntegerAlgorithm,
                    BresenhamEliminationOfAliasingAlgorithm, WuAlgorithm, LibAlgorithm]:
            all_time = 0

            for _ in range(runs_count):
                start_time = time()

                cur_angle = 0

                while cur_angle < 360:
                    alg(center[0], center[1],
                        center[0] + length * math.cos(math.radians(angle)),
                        center[1] + length * math.sin(math.radians(angle)),
                        line_color)

                    cur_angle += angle

                end_time = time()

                all_time += end_time - start_time

            times.append(all_time / runs_count)

        # Draw the 2d diagrams for the times of the algorithms
        plt.figure(figsize=(20, 20))
        plt.title("Сравнение времени работы алгоритмов")
        plt.xlabel("Алгоритм")
        plt.ylabel("Время, с")
        plt.bar(["ЦДА", "Брезенхем (float)", "Брезенхем (int)", "Брезенхем (сглаживание)", "Ву", "Библиотечный"],
                times, color='green')

        plt.show()

    # Compare the stepping
    def SteppingComparing(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

        # Get the center
        center = [self.CenterX.toPlainText(), self.CenterY.toPlainText()]

        # Get the length
        length = self.LenField.toPlainText()

        # Check the input data
        if center[0] == "" or center[1] == "" or length == "":
            ErrorDialog("Ошибка", "Ошибка замеров", "Не все поля заполнены!")
            return

        try:
            center[0] = int(center[0])
            center[1] = int(center[1])
            length = float(length)
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка замеров", "Введены некорректные данные!")
            return

        # Init times list
        steps = [[] for _ in range(5)]
        angle_step = 2
        cur_angle = 0

        # Get the time

        while cur_angle < 90:
            for i, alg in enumerate([DDAAlgorithm, BresenhamFloatAlgorithm, BresenhamIntegerAlgorithm,
                                     BresenhamEliminationOfAliasingAlgorithm, WuAlgorithm]):
                cur_steps = alg(center[0], center[1],
                                center[0] + length * math.cos(math.radians(cur_angle)),
                                center[1] + length * math.sin(math.radians(cur_angle)),
                                line_color, True)

                steps[i].append(cur_steps)

            cur_angle += angle_step

        # Draw the 2d diagrams for the stepping of the algorithms
        plt.figure(figsize=(20, 20))
        plt.title("Сравнение ступенчатости алгоритмов при разных углах при длине отрезков: " + str(length))
        plt.xlabel("Угол, градусы")
        plt.ylabel("Количество ступенек")

        plt.plot([i for i in range(0, 90, angle_step)], steps[0], label="ЦДА")
        plt.plot([i for i in range(0, 90, angle_step)], steps[1], "--", label="Брезенхем (float)")
        plt.plot([i for i in range(0, 90, angle_step)], steps[2], "-.", label="Брезенхем (int)")
        plt.plot([i for i in range(0, 90, angle_step)], steps[3], "*", label="Брезенхем (сглаживание)")
        plt.plot([i for i in range(0, 90, angle_step)], steps[4], ".", label="Ву")

        plt.xticks([i for i in range(0, 91, angle_step)])
        plt.legend()

        plt.show()

    # Clear the graph
    def DeleteGraph(self):

        # Clear the graph
        self.paintWidget.clear()

        # Update the field
        self.GraphField.update()


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    # Run the main Qt loop
    sys.exit(app.exec())
