from tools import *


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
