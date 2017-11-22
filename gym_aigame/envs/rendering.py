import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPolygon
from PyQt5.QtCore import QPoint, QSize

class Renderer:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.img = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
        self.painter = QPainter()

    def beginFrame(self):
        self.painter.begin(self.img)

        # Clear the background
        self.painter.setBrush(QColor(0, 0, 0))
        self.painter.drawRect(0, 0, self.width - 1, self.height - 1)

    def endFrame(self):
        self.painter.end()

    def getPixmap(self):
        return QPixmap.fromImage(self.img)

    def getArray(self, shape=None):
        """
        Get a numpy array of RGB pixel values.
        The size argument should be (3,w,h)
        """

        width = shape[0]
        height = shape[1]
        assert shape[2] == 3
        assert width > 0 and width <= self.width
        assert height > 0 and height <= self.height

        # Get a downsampled version of the image
        scaled = self.img.scaled(
            QSize(width, height),
            transformMode = Qt.SmoothTransformation
        )

        # Copy the pixel data to a numpy array
        output = np.ndarray(shape=shape, dtype='uint8')
        for y in range(0, height):
            for x in range(0, width):
                pix = scaled.pixel(x, y)
                r = (pix >> 16) & 0xFF
                g = (pix >>  8) & 0xFF
                b = (pix >>  0) & 0xFF
                output[x, y, 0] = r
                output[x, y, 1] = g
                output[x, y, 2] = b

        return output

    def push(self):
        self.painter.save()

    def pop(self):
        self.painter.restore()

    def rotate(self, degrees):
        self.painter.rotate(degrees)

    def translate(self, x, y):
        self.painter.translate(x, y)

    def scale(self, x, y):
        self.painter.scale(x, y)

    def setLineColor(self, r, g, b):
        self.painter.setPen(QColor(r, g, b))

    def setColor(self, r, g, b):
        self.painter.setBrush(QColor(r, g, b))

    def drawLine(self, x0, y0, x1, y1):
        self.painter.drawLine(x0, y0, x1, y1)

    def drawCircle(self, x, y, r):
        center = QPoint(x, y)
        self.painter.drawEllipse(center, r, r)

    def drawPolygon(self, points):
        """Takes a list of points (tuples) as input"""
        points = map(lambda p: QPoint(p[0], p[1]), points)
        self.painter.drawPolygon(QPolygon(points))
