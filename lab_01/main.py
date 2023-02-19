from secrets import choice
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import Qt
import sys

import calculate


# Colors
colors = [
    '#FFFF00', '#FF00FF', '#00BFFF', '#E0FFFF', '#FF0000', '#00FF7F',
    '#ADFF2F', '#C71585', '#FFD700', '#F5DEB3', '#00FF00', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

# Transfers coordinates to the coordinate system of the canvas
DX, DY = 360, 400


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
        self.ClearGraph.clicked.connect(self.DeleteGraph)
        self.ClearGraph.setShortcut("Ctrl+F")

        self.Quit.setShortcut("Ctrl+D")
        self.Quit.triggered.connect(QtWidgets.qApp.quit)

        self.coordinates = {}

        self.last_x = None
        self.last_y = None

    def DrawAxes(self):

        # Draw axes
        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("white"))
        painter.setPen(pen)

        painter.drawLine(0, 400, 720, 400)
        painter.drawLine(360, 0, 360, 800)

        painter.end()

    def SetCoordinates(self):

        # Set canvas
        canvas = QtGui.QPixmap(720, 800)
        self.Label.setPixmap(canvas)

        # Draw axes
        self.DrawAxes()

    def SetTable(self):

        # Set table columns and rows
        self.Table.setColumnCount(3)

        # Set table column width
        self.Table.setColumnWidth(0, 175)
        self.Table.setColumnWidth(1, 175)
        self.Table.setColumnWidth(2, 175)

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
        self.coordinates[row + 1] = (new_x, new_y)

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
        self.coordinates[number] = (new_x, new_y)

    def DrawAnswer(self):

        self.DataCompletion()

        if not self.coordinates:
            ErrorDialog("Ошибка получения координат",
                        "Координаты не были заданы. Попробуйте снова",
                        "")
            return

        max_angle, triangle_points = calculate.GetMaxAngle(self.coordinates)

        if not triangle_points:
            ErrorDialog("Ошибка поиска решений",
                        "Треугольник, удовлетворяющий условию, не был найден. Попробуйте снова",
                        "")
            return

        painter = QtGui.QPainter(self.Label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("white"))
        painter.setPen(pen)

        # Draw triangle
        painter.drawLine(triangle_points[0][0], triangle_points[0][1],
                         triangle_points[1][0], triangle_points[1][1])

        painter.drawLine(triangle_points[1][0], triangle_points[1][1],
                         triangle_points[2][0], triangle_points[2][1])

        painter.drawLine(triangle_points[2][0], triangle_points[2][1],
                         triangle_points[0][0], triangle_points[0][1])

        # Draw text
        font = QtGui.QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(10, 10, f"Максимальный угол: {max_angle}")

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
        self.coordinates[row + 1] = (e.pos().x() - 10, e.pos().y() - 36)

        # Add point to table
        self.AddPointToTable(
            row,
            self.coordinates[row + 1][0] - DX,
            -(self.coordinates[row + 1][1] - DY))

        # Draw point
        painter.drawPoint(self.coordinates[row + 1][0], self.coordinates[row + 1][1])

        self.update()
        painter.end()

        return super().mousePressEvent(e)

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

        # Update label
        self.Label.update()


if __name__ == '__main__':
    # Run application
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    sys.exit(app.exec())
