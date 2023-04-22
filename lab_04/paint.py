from PyQt5 import QtCore
from tools import *


# Class for drawing figures
class PaintWidget(QtWidgets.QWidget):
    def __init__(self, parent):

        super().__init__(parent)

        self.qp = QtGui.QPainter()

        self.setFixedSize(900, 781)

        self.lineColor = None
        self.backgroundColor = None

        self.setLineColor()
        self.setBackgroundColor()

        self.figures = []
        self.spectra = []

    # Set line color
    def setLineColor(self, color=QtGui.QColor(0, 0, 0)):
        self.lineColor = color

    # Set background color
    def setBackgroundColor(self, color=QtGui.QColor(255, 255, 255)):
        self.backgroundColor = color

    # Paint event
    def paintEvent(self, event: QtGui.QPaintEvent):

        self.qp.begin(self)

        # Clear the field
        self.qp.fillRect(0, 0, self.width(), self.height(), self.backgroundColor)

        if self.figures:
            for figure in self.figures:
                self.drawFigure(figure)

        if self.spectra:
            for spectrum in self.spectra:
                self.drawFigure(spectrum)

        self.qp.end()

    # Draw figure
    def drawFigure(self, points):

        for point in points:

            current_color = point[-1]

            if len(point) == 3:
                self.qp.setPen(QtGui.QPen(current_color, 1))
                self.qp.drawPoint(QtCore.QPointF(point[0], point[1]))
            else:
                self.qp.setPen(QtGui.QPen(current_color, 1))
                self.qp.drawEllipse(QtCore.QPointF(point[0], point[1]), point[2], point[3])

    # Clear the field
    def clear(self):

        self.figures = []
        self.spectra = []

        self.update()
