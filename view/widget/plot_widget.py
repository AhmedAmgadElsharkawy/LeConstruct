from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,QHBoxLayout,QLabel
)

import pyqtgraph as pg
from PyQt5.QtGui import QFont


class PlotWidget(QWidget):
    def __init__(self, title):
        super().__init__()

        self.title = title
        self.legend = None

        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("plot_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(16,16,16,16)
        self.main_widget_layout.setSpacing(24)
        self.central_layout.addWidget(self.main_widget)

        self.header_widget = QWidget()
        self.header_widget_layout = QHBoxLayout(self.header_widget)
        self.header_widget_layout.setContentsMargins(0,0,0,0)
        self.header_widget_layout.setSpacing(0)
        self.main_widget_layout.addWidget(self.header_widget)

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal) 

        self.title_label = QLabel(title)
        self.title_label.setFont(font)
        self.header_widget_layout.addWidget(self.title_label)

        self._plot_widget  = pg.PlotWidget()
        self._plot_widget .showGrid(x=True, y=True)
        self._plot_widget .setBackground("#FFFFFF")
        self._plot_widget .getAxis("left").setPen("black")
        self._plot_widget .getAxis("bottom").setPen("black")
        self._plot_widget .getPlotItem().titleLabel.item.setFont(QFont("Arial"))
        self.main_widget_layout.addWidget(self._plot_widget )


    def setLabel(self, *args, **kwargs):
        self._plot_widget .setLabel(*args, **kwargs)

    def clear(self):
        self._plot_widget .clear()

    def addLegend(self, *args, **kwargs):
        if self.legend is None:
            self.legend = self._plot_widget .addLegend(*args, **kwargs)
        return self.legend

    def plot(self, *args, **kwargs):
        return self._plot_widget .plot(*args, **kwargs)