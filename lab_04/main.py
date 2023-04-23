from PyQt5 import uic
from matplotlib import pyplot as plt
from time import time
from tools import *
from paint import PaintWidget

import sys


# Constants for measures
runs_count = 300
max_radius = 1200
step = 100


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
        self.CircleBtn.setChecked(True)
        self.CanonAlg.setChecked(True)

        # Set the figure and spectrum parameters
        self.CircleBtn.clicked.connect(self.SetParams)
        self.EllipseBtn.clicked.connect(self.SetParams)

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
        self.DrawCircleBtn.clicked.connect(self.DrawCircle)
        self.DrawEllipseBtn.clicked.connect(self.DrawEllipse)
        self.DrawCircleSpectrumBtn.clicked.connect(self.DrawCircleSpectrum)
        self.DrawEllipseSpectrumBtn.clicked.connect(self.DrawEllipseSpectrum)
        self.TimeCompare.clicked.connect(self.TimeComparing)
        self.ClearGraph.clicked.connect(self.DeleteGraph)

        self.AuthorInfo.triggered.connect(PrintAuthorInfo)
        self.TaskInfo.triggered.connect(PrintTaskInfo)

        # Set the quit trigger
        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

    # Set the figure and spectrum parameters
    def SetParams(self):

        # Set the figure parameters
        self.FigureParams.setCurrentIndex(0 if self.CircleBtn.isChecked() else 1)

        # Set the spectrum parameters
        self.SpectrumParams.setCurrentIndex(0 if self.CircleBtn.isChecked() else 1)

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

    # Draw the circle
    def DrawCircle(self):

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

        # Get the radius
        radius = self.RadiusField.toPlainText()

        # Check the input data
        if center[0] == "" or center[1] == "" or radius == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Не все поля заполнены!")
            return

        try:
            center[0] = float(center[0])
            center[1] = float(center[1])
            radius = float(radius)
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные данные!")
            return

        # Check the radius
        if radius <= 0:
            ErrorDialog("Ошибка", "Ошибка ввода", "Радиус должен быть положительным!")
            return

        center[0] = int(center[0])
        center[1] = int(center[1])

        # Get points
        points = GetAlgorithmPoints(self, [center[0], center[1], radius])

        # Save the color
        for point in points:
            point.append(self.paintWidget.lineColor)

        # Draw the circle
        self.paintWidget.figures.append(points)
        self.paintWidget.update()

    # Draw the ellipse
    def DrawEllipse(self):

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

        # Get the radius
        radius = [self.RxField.toPlainText(), self.RyField.toPlainText()]

        # Check the input data
        if center[0] == "" or center[1] == "" or radius[0] == "" or radius[1] == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Не все поля заполнены!")
            return

        try:
            center[0] = float(center[0])
            center[1] = float(center[1])
            radius[0] = float(radius[0])
            radius[1] = float(radius[1])
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные данные!")
            return

        # Check the radius
        if radius[0] <= 0 or radius[1] <= 0:
            ErrorDialog("Ошибка", "Ошибка ввода", "Радиус должен быть положительным!")
            return

        center[0] = int(center[0])
        center[1] = int(center[1])

        # Get points
        points = GetAlgorithmPoints(self, [center[0], center[1], radius[0], radius[1]])

        # Save the color
        for point in points:
            point.append(self.paintWidget.lineColor)

        # Draw the ellipse
        self.paintWidget.figures.append(points)
        self.paintWidget.update()

    # Draw circle spectrum
    def DrawCircleSpectrum(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

        # Get parameters count
        parameters_count = 0

        # Get spectrum parameters
        start_r = self.StartRField.toPlainText()
        if start_r != "":
            parameters_count += 1

        end_r = self.EndRField.toPlainText()
        if end_r != "":
            parameters_count += 1

        step_r = self.StepRField.toPlainText()
        if step_r != "":
            parameters_count += 1

        count = self.CountCurclesField.toPlainText()
        if count != "":
            parameters_count += 1

        # Check the input data
        if parameters_count != 3:
            ErrorDialog("Ошибка", "Ошибка ввода", "Должны быть заданы ровно 3 параметра")
            return

        # Get missing parameter
        if start_r == "":
            try:
                end_r = float(end_r)
                step_r = int(step_r)
                count = int(count)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            if end_r <= 0 or step_r <= 0 or count <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            start_r = end_r - step_r * count
        elif end_r == "":
            try:
                start_r = float(start_r)
                step_r = int(step_r)
                count = int(count)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            if start_r <= 0 or step_r <= 0 or count <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            end_r = start_r + step_r * count
        elif step_r == "":
            try:
                start_r = float(start_r)
                end_r = float(end_r)
                count = int(count)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            if start_r <= 0 or end_r <= 0 or count <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            step_r = (end_r - start_r) // count
        elif count == "":
            try:
                start_r = float(start_r)
                end_r = float(end_r)
                step_r = int(step_r)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            if start_r <= 0 or end_r <= 0 or step_r <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
                return

            count = (end_r - start_r) // step_r

        if start_r > end_r:
            ErrorDialog("Ошибка", "Ошибка ввода", "Начальный радиус должен быть меньше конечного!")
            return

        # Get the center
        center = [self.CenterX.toPlainText(), self.CenterY.toPlainText()]

        # Check the input data
        if center[0] == "" or center[1] == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Координаты центра не могут быть пустыми!")
            return

        try:
            center[0] = int(center[0])
            center[1] = int(center[1])
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные координаты центра!")
            return

        # Get points list
        points = []

        # Draw the circle spectrum
        for i in range(int(count)):
            points += GetAlgorithmPoints(self, [center[0], center[1], start_r + step_r * i])

        # Save the color
        for point in points:
            point.append(self.paintWidget.lineColor)

        # Draw the ellipse
        self.paintWidget.spectra.append(points)
        self.paintWidget.update()

    # Draw ellipse spectrum
    def DrawEllipseSpectrum(self):

        # Get the lines color
        line_color = GetLineColor(self)

        # Get the background color
        background_color = GetBackgroundColor(self)

        # Set line color
        self.paintWidget.setLineColor(QtGui.QColor(line_color[0], line_color[1], line_color[2]))

        # Set background color
        self.paintWidget.setBackgroundColor(QtGui.QColor(background_color[0], background_color[1], background_color[2]))

        # Get spectrum parameters
        start_rx, start_ry, count = \
            self.StartRxField.toPlainText(), \
            self.StartRyField.toPlainText(), \
            self.CountEllipsesField.toPlainText()

        # Check the input data
        if start_rx == "" or start_ry == "" or count == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Должны быть заданы обязательно начальная ширина, длина и количество!")
            return

        try:
            start_rx = float(start_rx)
            start_ry = float(start_ry)
            count = int(count)
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
            return

        if count <= 0 or start_rx <= 0 or start_ry <= 0:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные параметры спектра!")
            return

        # Get the step
        step_rx, step_ry = \
            self.StepRxField.toPlainText(), \
            self.StepRyField.toPlainText()

        # Check the input data
        if step_rx == "" and step_ry == "" or step_rx != "" and step_ry != "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Должен быть задан ровно один параметр шага!")
            return
        elif step_rx != "":
            try:
                step_rx = float(step_rx)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введен некорректный шаг!")
                return

            if step_rx <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Шаг должен быть положительным!")
                return
        else:
            try:
                step_ry = float(step_ry)
            except ValueError:
                ErrorDialog("Ошибка", "Ошибка ввода", "Введен некорректный шаг!")
                return

            if step_ry <= 0:
                ErrorDialog("Ошибка", "Ошибка ввода", "Шаг должен быть положительным!")
                return

        # Get the center
        center = [self.CenterX.toPlainText(), self.CenterY.toPlainText()]

        # Check the input data
        if center[0] == "" or center[1] == "":
            ErrorDialog("Ошибка", "Ошибка ввода", "Координаты центра не могут быть пустыми!")
            return

        try:
            center[0] = int(center[0])
            center[1] = int(center[1])
        except ValueError:
            ErrorDialog("Ошибка", "Ошибка ввода", "Введены некорректные координаты центра!")
            return

        # Get points list
        points = []

        # Get the temp radius
        rx, ry = start_rx, start_ry
        coefficient = rx / ry

        for _ in range(int(count)):

            if step_rx != "":
                rx += step_rx
                ry = round(rx / coefficient)
            else:
                ry += step_ry
                rx = round(ry * coefficient)

            points += GetAlgorithmPoints(self, [center[0], center[1], rx, ry])

        # Save the color
        for point in points:
            point.append(self.paintWidget.lineColor)

        # Draw the ellipse
        self.paintWidget.spectra.append(points)
        self.paintWidget.update()

    # Time measurement
    def TimeComparing(self):

        times = [[] for _ in range(5)]
        algorithms = [CanonicalCircle, ParametricCircle, BresenhamCircle, MidpointCircle, LibCircle] \
            if self.CircleBtn.isChecked() \
            else [CanonicalEllipse, ParametricEllipse, BresenhamEllipse, MidpointEllipse, LibEllipse]

        for k, alg in enumerate(algorithms):
            for i in range(1, max_radius // step):
                all_time = 0
                params = [0, 0, step*i] if self.CircleBtn.isChecked() else [0, 0, step*i, step*i]
                for _ in range(runs_count):
                    start_t = time()
                    alg(params, False)
                    end_t = time()
                    all_time += end_t - start_t

                times[k].append(all_time / runs_count)

        radius = [i for i in range(step, max_radius, step)]

        plt.figure(figsize=(13, 7))
        plt.rcParams['font.size'] = '15'

        plt.title(f"Замеры времени построения {'окружностей' if self.CircleBtn.isChecked() else 'эллипсов'}"
                  f" для различных алгоритмов")

        plt.plot(radius, times[0], label='Каноническое уравнение')
        plt.plot(radius, times[1], label='Параметрическое уравнение')
        plt.plot(radius, times[2], label='Алгоритм Брезенхема')
        plt.plot(radius, times[3], label='Алгоритм средней точки')
        plt.plot(radius, times[4], label='Библиотечная функция')

        plt.xticks([i for i in range(step, max_radius + 1, step)])
        plt.legend()
        plt.xlabel("Радиус")
        plt.ylabel("Время")

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
