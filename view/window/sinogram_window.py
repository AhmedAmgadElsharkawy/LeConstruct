import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SinogramWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sinogram")
        self.setMinimumSize(1100, 800)
        self.resize(1200, 900)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        
        self.plot_widget.setBackground(QColor("#edf2f8"))
        self.plot_widget.setLabel('bottom', "Angle (Degrees)")
        self.plot_widget.setLabel('left', "Sensor Position")
        
        self.image_item = pg.ImageItem()
        self.plot_widget.addItem(self.image_item)
        
        # Configure view
        self.plot_widget.getViewBox().invertY(False)
        self.plot_widget.getViewBox().setAspectLocked(False)

        self.data = None

    def set_data(self, sinogram_data: np.ndarray, angles: np.ndarray):
        self.data = sinogram_data
        if len(angles) > 1:
            angle_step = angles[1] - angles[0]
            start_angle = angles[0]
        else:
            angle_step = 1
            start_angle = angles[0] if len(angles) == 1 else 0
            
        rect = pg.QtCore.QRectF(start_angle, 0, angle_step * sinogram_data.shape[1], sinogram_data.shape[0])
        self.image_item.setImage(sinogram_data.T, autoLevels=True)
        self.image_item.setRect(rect)
