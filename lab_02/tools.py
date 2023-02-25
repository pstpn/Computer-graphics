from PyQt5 import QtWidgets


# Function for deep copying
def DeepCopy(dst, src):

    # Copy circle coordinates
    dst["circle"]["first_point"] = src["circle"]["first_point"].copy()
    dst["circle"]["second_point"] = src["circle"]["second_point"].copy()
    dst["circle"]["third_point"] = src["circle"]["third_point"].copy()
    dst["circle"]["radius_x"] = src["circle"]["radius_x"]
    dst["circle"]["radius_y"] = src["circle"]["radius_y"]
    dst["circle"]["points"] = src["circle"]["points"].copy()

    # Copy line coordinates
    dst["line"]["first_point"] = src["line"]["first_point"].copy()
    dst["line"]["second_point"] = src["line"]["second_point"].copy()

    # Copy ellipse coordinates
    dst["ellipse"]["radius_x"] = src["ellipse"]["radius_x"]
    dst["ellipse"]["radius_y"] = src["ellipse"]["radius_y"]
    dst["ellipse"]["points"] = src["ellipse"]["points"].copy()

    # Copy left quadrilateral coordinates
    dst["left_quad"]["first_side"]["first_point"] = \
        src["left_quad"]["first_side"]["first_point"].copy()
    dst["left_quad"]["first_side"]["second_point"] = \
        src["left_quad"]["first_side"]["second_point"].copy()

    # Copy right quadrilateral coordinates
    dst["right_quad"]["first_side"]["first_point"] = \
        src["right_quad"]["first_side"]["first_point"].copy()
    dst["right_quad"]["first_side"]["second_point"] = \
        src["right_quad"]["first_side"]["second_point"].copy()


# Function for clearing coordinates
def ClearCoordinates(coordinates):

    # Clear circle coordinates
    coordinates["circle"]["first_point"].clear()
    coordinates["circle"]["second_point"].clear()
    coordinates["circle"]["third_point"].clear()
    coordinates["circle"]["radius_x"] = 0
    coordinates["circle"]["radius_y"] = 0
    coordinates["circle"]["points"].clear()

    # Clear line coordinates
    coordinates["line"]["first_point"].clear()
    coordinates["line"]["second_point"].clear()

    # Clear ellipse coordinates
    coordinates["ellipse"]["radius_x"] = 0
    coordinates["ellipse"]["radius_y"] = 0
    coordinates["ellipse"]["points"].clear()

    # Clear left quadrilateral coordinates
    coordinates["left_quad"]["first_side"]["first_point"].clear()
    coordinates["left_quad"]["first_side"]["second_point"].clear()

    # Clear right quadrilateral coordinates
    coordinates["right_quad"]["first_side"]["first_point"].clear()
    coordinates["right_quad"]["first_side"]["second_point"].clear()


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
            "Изобразить на экране данную фигуру\n"
            "(2 квадрата, 1 окружность, 1 эллипс).\n"
            "Реализовать возможность перемещения фигуры, \n"
            "поворота и масштабирования.\n"

    )