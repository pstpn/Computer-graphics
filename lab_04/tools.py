from PyQt5 import QtWidgets
from PyQt5 import QtGui

from algorithms import *


# Convert color to Qt color
def GetQColor(color):
    return QtGui.QColor(color[0], color[1], color[2], color[3]) \
        if len(color) == 4 \
        else QtGui.QColor(color[0], color[1], color[2])


# Get color from radio buttons
def GetLineColor(window):

    if window.BlueColor.isChecked():
        return 0, 0, 255
    elif window.GreenColor.isChecked():
        return 0, 255, 0
    elif window.RedColor.isChecked():
        return 255, 0, 0
    elif window.YellowColor.isChecked():
        return 255, 255, 0
    elif window.WhiteColor.isChecked():
        return 255, 255, 255
    elif window.PurpleColor.isChecked():
        return 255, 0, 255


# Get background color from radio buttons
def GetBackgroundColor(window):

    if window.BlueColor_2.isChecked():
        return 0, 0, 255
    elif window.GreenColor_2.isChecked():
        return 0, 255, 0
    elif window.RedColor_2.isChecked():
        return 255, 0, 0
    elif window.YellowColor_2.isChecked():
        return 255, 255, 0
    elif window.WhiteColor_2.isChecked():
        return 255, 255, 255
    elif window.PurpleColor_2.isChecked():
        return 255, 0, 255


# Get algorithm points from radio buttons
def GetAlgorithmPoints(window, params, draw_figure=True):

    if window.CanonAlg.isChecked():
        return CanonicalCircle(params, draw_figure) if window.CircleBtn.isChecked() \
            else CanonicalEllipse(params, draw_figure)
    elif window.ParamAlg.isChecked():
        return ParametricCircle(params, draw_figure) if window.CircleBtn.isChecked() \
            else ParametricEllipse(params, draw_figure)
    elif window.BrezAlg.isChecked():
        return BresenhamCircle(params, draw_figure) if window.CircleBtn.isChecked() \
            else BresenhamEllipse(params, draw_figure)
    elif window.MidpointAlg.isChecked():
        return MidpointCircle(params, draw_figure) if window.CircleBtn.isChecked() \
            else MidpointEllipse(params, draw_figure)
    elif window.LibAlg.isChecked():
        return [[params[0], params[1], int(params[2]), int(params[2])]] if window.CircleBtn.isChecked() \
            else [[params[0], params[1], int(params[3]), int(params[2])]]



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
            "Реализовать возможность построения \n"
            "окружности и эллипса методами Брезенхема, \n"
            "средней точки, параметрическими уравнениями \n"
            "и каноническими уравнениями. Реализовать сравнение \n"
            "временных характеристик разных алгоритмов.\n"
    )
