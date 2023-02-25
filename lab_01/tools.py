from PyQt5 import QtWidgets


# Transfers coordinates to the coordinate system of the canvas
DX, DY = 360, 360


# Get zoom coordinates
def ZoomOut(triangle):

    # Get max and min coordinates
    max_x, min_x = max(*triangle, key=lambda x: x[0])[0],\
        min(*triangle, key=lambda x: x[0])[0]
    max_y, min_y = max(*triangle, key=lambda x: x[1])[1],\
        min(*triangle, key=lambda x: x[1])[1]

    # Scale coordinates
    scale_coordinates = [[x, y] for x, y in triangle]

    while max_x > 1.1 * DX or max_y > 1.1 * DY or \
            min_x < -200 or min_y < -200:
        max_x /= 2
        max_y /= 2

        min_x /= 2
        min_y /= 2

        for i in range(len(scale_coordinates)):
            scale_coordinates[i] = [scale_coordinates[i][0] / 2, scale_coordinates[i][1] / 2]

    if min(scale_coordinates, key=lambda x: x[0])[0] < 0 or \
            min(scale_coordinates, key=lambda x: x[1])[1] < 0:
        for i in range(len(scale_coordinates)):
            scale_coordinates[i] = [scale_coordinates[i][0] + 200, scale_coordinates[i][1] + 200]

    print(scale_coordinates)

    return scale_coordinates


# Print information
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


# Print author information
def PrintAuthorInfo():

    PrintInfo(
            "Информация об авторе",
            "Задание выполнил Постнов Степан Андреевич,\n"
            "студент группы ИУ7-41Б"
    )


# Print task information
def PrintTaskInfo():

    PrintInfo(
            "Условие задания",
            "На плоскости дано множество точек.\n"
            "Найти такой треугольник с вершинами в этих точках, \n"
            "у которого угол, образованный прямой, соединяющей\n "
            "точку пересечения высот и начало координат, и осью ординат максимален.\n"
            "Вывести изображение в графическом режиме."

    )


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