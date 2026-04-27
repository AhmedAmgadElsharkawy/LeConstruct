from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from view.widget.sidebar import Sidebar 
from view.widget.viewer import Viewer

from view.widget.metric_widget import MetricWidget
from view.style_manager import apply_stylesheet

from controller.reconstruction_controller import ReconstructionController
from controller.load_controller import LoadController
from controller.metrics_controller import MetricsController
from controller.ft_controller import FTController

import numpy as np

class MainWindow(QMainWindow):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            return super(MainWindow, cls).__new__(cls)
        return cls.__instance     

    def __init__(self):
        if MainWindow.__instance is not None:
            return
        
        super().__init__() 
        MainWindow.__instance = self

        self.setWindowTitle("LeConstruct")


        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setObjectName("main_widget")
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.main_widget_layout.addWidget(self.sidebar)

        self.body_container = QWidget()
        self.body_container_layout = QVBoxLayout(self.body_container)
        self.body_container_layout.setContentsMargins(24, 24, 24, 24)
        self.main_widget_layout.addWidget(self.body_container)

        self.top_bar_container = QWidget()
        self.top_bar_layout = QHBoxLayout(self.top_bar_container)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setSpacing(0)
        
        self.top_bar_layout.addStretch(1)
        
        from PyQt5.QtWidgets import QPushButton
        from PyQt5.QtGui import QFont
        from PyQt5.QtCore import Qt
        
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Medium)
        self.sinogram_button = QPushButton("Sinogram")
        self.sinogram_button.setObjectName("load_button")
        self.sinogram_button.setFont(font)
        self.sinogram_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.top_bar_layout.addWidget(self.sinogram_button)
        
        self.body_container_layout.addWidget(self.top_bar_container)

        self.slice_viewers_container = QWidget()
        self.slice_viewers_container_layout = QHBoxLayout(self.slice_viewers_container)
        self.slice_viewers_container_layout.setContentsMargins(0,0,0,0)
        self.slice_viewers_container_layout.setSpacing(24)
        self.body_container_layout.addWidget(self.slice_viewers_container, stretch=1)

        self.reference_slice_viewer = Viewer(self, title="Reference Slice")
        self.reconstructed_slice_viewer = Viewer(self, title="Reconstructed Slice")

        self.slice_viewers_container_layout.addWidget(self.reference_slice_viewer)
        self.slice_viewers_container_layout.addWidget(self.reconstructed_slice_viewer)

        
        self.ft_viewers_container = QWidget()
        self.ft_viewers_container_layout = QHBoxLayout(self.ft_viewers_container)
        self.ft_viewers_container_layout.setContentsMargins(0,0,0,0)
        self.ft_viewers_container_layout.setSpacing(24)
        self.body_container_layout.addWidget(self.ft_viewers_container, stretch=1)

        self.reference_slice_ft_viewer = Viewer(self, title= "Refrence Slice FT")
        self.reconstructed_slice_ft_viewer = Viewer(self, title= "Reconstructed Slice FT")

        self.ft_viewers_container_layout.addWidget(self.reference_slice_ft_viewer)
        self.ft_viewers_container_layout.addWidget(self.reconstructed_slice_ft_viewer)


        
        self.quantitative_metrics_container = QWidget()
        self.quantitative_metrics_container_layout = QHBoxLayout(self.quantitative_metrics_container)
        self.quantitative_metrics_container.setObjectName("quantitative_metrics_container")
        self.quantitative_metrics_container_layout.setContentsMargins(16,16,16,16)
        self.quantitative_metrics_container_layout.setSpacing(0)

        self.PSNR_metric = MetricWidget("PSNR")
        self.SSIM_metric = MetricWidget("SSIM")
        
        self.quantitative_metrics_container_layout.addWidget(self.PSNR_metric)
        self.quantitative_metrics_container_layout.addWidget(self.SSIM_metric)

        self.body_container_layout.addWidget(self.quantitative_metrics_container, stretch=0)
        
        from view.window.sinogram_window import SinogramWindow
        self.sinogram_window = SinogramWindow()
        self.sinogram_button.clicked.connect(self.sinogram_window.show)

        self.ft_controller = FTController(self)
        self.metrics_controller = MetricsController(self)
        self.load_controller = LoadController(self)
        self.reconstruction_controller = ReconstructionController(self)
        

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.showMaximized()

        apply_stylesheet(self, "light")
