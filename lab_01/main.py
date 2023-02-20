# На плоскости дано множество точек.
# Найти такой треугольник с вершинами в этих точках, у которого угол, образованный прямой, соединяющей точку пересечения
# высот и начало координат, и осью ординат максимален.

from secrets import choice
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

import calculate

# Colors
colors = [
    '#FFFF00', '#FF00FF', '#00BFFF', '#E0FFFF', '#FF0000', '#00FF7F',
    '#ADFF2F', '#C71585', '#FFD700', '#F5DEB3', '#00FF00', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

# Transfers coordinates to the coordinate system of the canvas
DX, DY = 360, 360


def PrintInfo(title, text):

    # Create a message box
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    # Set the message box text
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    # Show the message box
    msg.exec_()


def PrintAuthorInfo():

    PrintInfo(
            "Информация об авторе",
            "Задание выполнил Постнов Степан Андреевич,\n"
            "студент группы ИУ7-41Б"
    )


def PrintTaskInfo():

    PrintInfo(
            "Условие задания",
            "На плоскости дано множество точек.\n"
            "Найти такой треугольник с вершинами в этих точках, \n"
            "у которого угол, образованный прямой, соединяющей\n "
            "точку пересечения высот и начало координат, и осью ординат максимален.\n"
            "Вывести изображение в графическом режиме."

    )


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


def ZoomOut(triangle):

    # Get max and min coordinates
    max_x, min_x = max(*triangle, key=lambda x: x[0])[0],\
        min(*triangle, key=lambda x: x[0])[0]
    max_y, min_y = max(*triangle, key=lambda x: x[1])[1],\
        min(*triangle, key=lambda x: x[1])[1]

    # Scale coordinates
    scale_coordinates = [[x, y] for x, y in triangle]

    while max_x > 1.1 * DX or max_y > 1.1 * DY or \
            min_x < -1 or min_y < -1:
        max_x /= 2
        max_y /= 2

        min_x /= 2
        min_y /= 2

        for i in range(len(scale_coordinates)):
            scale_coordinates[i] = [scale_coordinates[i][0] / 2, scale_coordinates[i][1] / 2]

    print(scale_coordinates)

    return scale_coordinates


class Window(QtWidgets.QMainWindow):
    def __init__(self):

        super(Window, self).__init__()

        # Load UI
        uic.loadUi('Window/Window.ui', self)

        # Set table
        self.SetTable()

        # Set canvas
        self.SetCoordinates()

        # Connect buttons
        self.AddPoint.clicked.connect(self.AddingPoint)
        self.DeletePoint.clicked.connect(self.DeletePointWithNum)
        self.ChangePoint.clicked.connect(self.UpdatePointWithNum)
        self.ClearTable.clicked.connect(lambda clear_table: self.ClearTableData())
        self.ClearTable.setShortcut("Ctrl+W")
        self.ClearGraph.clicked.connect(self.DeleteGraphAndInit)
        self.ClearGraph.setShortcut("Ctrl+F")
        self.FindTriangle.clicked.connect(self.FindAnswerTriangle)

        self.AuthorInfo.triggered.connect(PrintAuthorInfo)
        self.TaskInfo.triggered.connect(PrintTaskInfo)

        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

        self.coordinates = {}

        self.last_x = None
        self.last_y = None

    def DrawCenterCoordinates(self, x, y):

        # Draw center
        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor(choice(colors)))
        painter.setPen(pen)
        painter.drawPoint(DX, DY)

        painter.setFont(QtGui.QFont("Times", 10))
        painter.drawText(DX + 10, DY + 20, f"O ({x - DX}, {y - DY})")

        painter.end()

    def DrawAxes(self):

        # Draw axes
        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("gray"))
        painter.setPen(pen)

        painter.drawLine(0, DY, DX * 2, DY)
        painter.drawLine(DX, 0, DX, DY * 2)

        painter.end()

    def DrawGrid(self):

        # Draw grid
        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor("gray"))
        painter.setPen(pen)

        for i in range(1, 10):
            painter.drawLine(0, DY + i * 40, DX * 2, DY + i * 40)
            painter.drawLine(0, DY - i * 40, DX * 2, DY - i * 40)
            painter.drawLine(DX + i * 40, 0, DX + i * 40, DY * 2)
            painter.drawLine(DX - i * 40, 0, DX - i * 40, DY * 2)

        painter.end()

    def SetCoordinates(self):

        # Set canvas
        canvas = QtGui.QPixmap(DX * 2, DY * 2)
        self.Label.setPixmap(canvas)

        # Draw axes
        self.DrawAxes()

        # Draw grid
        self.DrawGrid()

        # Draw center
        self.DrawCenterCoordinates(DX, DY)

    def SetTable(self):

        # Set table columns and rows
        self.Table.setColumnCount(3)

        # Set table column width
        self.Table.setColumnWidth(0, 193)
        self.Table.setColumnWidth(1, 193)
        self.Table.setColumnWidth(2, 193)

        # Set table headers
        self.Table.setHorizontalHeaderLabels(["Number", "X", "Y"])
        self.Table.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: black;}")

        # Set read-only table
        self.Table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Hide vertical header
        self.Table.verticalHeader().hide()

    def AddPointToTable(self, row, new_x, new_y):

        # Set number
        self.Table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))

        # Set X
        self.Table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(new_x)))

        # Set Y
        self.Table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(new_y)))

    def AddingPoint(self):

        # Get data from fields
        new_x, new_y = self.AddXField.toPlainText(), self.AddYField.toPlainText()

        # Check data
        if not new_x or not new_y:
            ErrorDialog("Ошибка добавления точки",
                        "Поля не могут быть пустыми",
                        "")
            return

        try:
            new_x, new_y = float(new_x), float(new_y)
        except ValueError:
            ErrorDialog("Ошибка добавления точки",
                        "Ожидались целые или дробные числа",
                        "")
            return

        # Get count rows
        row = self.Table.rowCount()
        self.Table.setRowCount(row + 1)

        # Add point to table
        self.AddPointToTable(row, new_x, new_y)

        # Add point to coordinates
        self.coordinates[row + 1] = (new_x + DX, DY - new_y)

    def DeletePointWithNum(self):

        # Get point number
        number = self.DelNumPointField.toPlainText()

        # Check data
        if not number:
            ErrorDialog("Ошибка удаления точки",
                        "Поле не может быть пустым",
                        "")
            return

        try:
            number = int(number)
        except ValueError:
            ErrorDialog("Ошибка удаления точки",
                        "Ожидался целый номер точки",
                        "")
            return

        # Check point number
        if number not in self.coordinates.keys():
            ErrorDialog("Ошибка удаления точки",
                        "Точка с таким номером не найдена",
                        "")
            return

        # Delete point from table
        self.Table.removeRow(number - 1)

        # Delete point from coordinates
        del self.coordinates[number]

        # Update coordinates numbers
        for i in range(number, self.Table.rowCount() + 1):
            self.coordinates[i] = self.coordinates[i + 1]
            del self.coordinates[i + 1]

        # Update table
        for i in range(self.Table.rowCount()):
            self.Table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))

    def UpdatePointWithNum(self):

        # Get point number
        number = self.ChangeNumPointField.toPlainText()

        # Get data from fields
        new_x, new_y = self.UpdateXField.toPlainText(), self.UpdateYField.toPlainText()

        # Check data
        if not number or not new_x or not new_y:
            ErrorDialog("Ошибка обновления точки",
                        "Поле не может быть пустым",
                        "")
            return

        try:
            number = int(number)
        except ValueError:
            ErrorDialog("Ошибка обновления точки",
                        "Ожидался целый номер точки",
                        "")
            return

        try:
            new_x, new_y = float(new_x), float(new_y)
        except ValueError:
            ErrorDialog("Ошибка обновления точки",
                        "Ожидались целые или дробные числа",
                        "")
            return

        # Check point number
        if number not in self.coordinates.keys():
            ErrorDialog("Ошибка обновления точки",
                        "Точка с таким номером не найдена",
                        "")
            return

        # Update point in table
        self.Table.setItem(number - 1, 1, QtWidgets.QTableWidgetItem(str(new_x)))
        self.Table.setItem(number - 1, 2, QtWidgets.QTableWidgetItem(str(new_y)))

        # Update point in coordinates
        self.coordinates[number] = (new_x + DX, DY - new_y)

    def FindAnswerTriangle(self):

        # Check coordinates
        if not self.coordinates:
            ErrorDialog("Ошибка получения координат",
                        "Координаты не были заданы. Попробуйте снова",
                        "")
            return

        if len(self.coordinates) < 3:
            ErrorDialog("Ошибка построения",
                        "Недостаточно точек для построения треугольника. Попробуйте снова",
                        "")
            return

        # Get max angle and triangle points
        max_angle, triangle_points, inter_heights = calculate.GetMaxAngle(self.coordinates, DX, DY)

        # Check triangle points
        if len(triangle_points) != 3:
            ErrorDialog("Ошибка поиска решений",
                        "Треугольник, удовлетворяющий условию, не был найден. Попробуйте снова",
                        "")
            return

        # Check intersection heights
        if inter_heights[0] is None or inter_heights[1] is None:
            ErrorDialog("Ошибка поиска решений",
                        "Вырожденный случай. Попробуйте снова",
                        "")
            return

        # Get scale figure
        scaled_triangle_points = triangle_points

        # Check scale figure
        if max(*triangle_points, key=lambda x: x[0])[0] > 2 * DX or \
                max(*triangle_points, key=lambda x: x[1])[1] > 2 * DY:
            scaled_triangle_points = ZoomOut(triangle_points)

            # Clear label
            self.DeleteGraph()
        else:

            # Clear label
            self.DeleteGraphAndInit()

        # Draw triangle
        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(choice(colors)))
        painter.setPen(pen)

        painter.drawLine(int(scaled_triangle_points[0][0]), int(scaled_triangle_points[0][1]),
                         int(scaled_triangle_points[1][0]), int(scaled_triangle_points[1][1]))

        painter.drawLine(int(scaled_triangle_points[1][0]), int(scaled_triangle_points[1][1]),
                         int(scaled_triangle_points[2][0]), int(scaled_triangle_points[2][1]))

        painter.drawLine(int(scaled_triangle_points[2][0]), int(scaled_triangle_points[2][1]),
                         int(scaled_triangle_points[0][0]), int(scaled_triangle_points[0][1]))

        pen.setWidth(10)
        painter.setPen(pen)

        painter.drawPoint(int(scaled_triangle_points[0][0]), int(scaled_triangle_points[0][1]))
        painter.drawPoint(int(scaled_triangle_points[1][0]), int(scaled_triangle_points[1][1]))
        painter.drawPoint(int(scaled_triangle_points[2][0]), int(scaled_triangle_points[2][1]))

        # Draw points number and coordinates on canvas near point
        for i in range(3):
            painter.drawText(int(scaled_triangle_points[i][0] + 10), int(scaled_triangle_points[i][1] + 10),
                             f"{i + 1} ({int(triangle_points[i][0] - DX)}, {int(DY - triangle_points[i][1])})")

        # Draw result
        self.AnswerLabel.setText(f"Полученный максимальный угол: {round(max_angle, 2)} градусов\n"
                                 f"Точки треугольника: "
                                 f"({int(triangle_points[0][0] - DX)}, {int(DY - triangle_points[0][1])}), "
                                 f"({int(triangle_points[1][0] - DX)}, {int(DY - triangle_points[1][1])}), "
                                 f"({int(triangle_points[2][0] - DX)}, {int(DY - triangle_points[2][1])})")

        self.Label.update()
        painter.end()

    def mousePressEvent(self, e):

        # Draw point
        painter = QtGui.QPainter(self.Label.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(QtGui.QColor(choice(colors)))
        painter.setPen(p)

        # Get count rows
        row = self.Table.rowCount()
        self.Table.setRowCount(row + 1)

        # Adding to coordinates
        self.coordinates[row + 1] = (e.pos().x() - 10, e.pos().y() - 42)

        # Add point to table
        self.AddPointToTable(
            row,
            self.coordinates[row + 1][0] - DX,
            DY - self.coordinates[row + 1][1])

        # Draw point
        painter.drawPoint(self.coordinates[row + 1][0], self.coordinates[row + 1][1])

        # Draw points number and coordinates on canvas near point
        font = QtGui.QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(self.coordinates[row + 1][0] + 10,
                         self.coordinates[row + 1][1] + 10,
                         f"{row + 1} ({self.coordinates[row + 1][0] - DX}; {DY - self.coordinates[row + 1][1]})")

        self.update()
        painter.end()

        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):

        # Get coordinates
        x, y = e.pos().x() - 10, e.pos().y() - 42

        # Set coordinates to label
        self.MouseCoordinatesLabel.setText(f"Текущие координаты: ({x - DX}; {DY - y})")

    def mouseReleaseEvent(self, e):

        self.last_x = None
        self.last_y = None

    def ClearTableData(self):

        # Clear table
        self.Table.setRowCount(0)

        # Clear coordinates
        self.coordinates = {}

    def DeleteGraph(self):

        # Clear canvas
        self.Label.pixmap().fill(QtCore.Qt.black)

        # Draw axes
        self.DrawAxes()

        # Draw grid
        self.DrawGrid()

        # Update label
        self.Label.update()

    def DeleteGraphAndInit(self):

        # Clear canvas
        self.DeleteGraph()

        # Draw center
        self.DrawCenterCoordinates(DX, DY)

        # Update label
        self.Label.update()


if __name__ == '__main__':

    # Run application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    sys.exit(app.exec())
