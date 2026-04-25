from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt

from view.widget.scrollable_list import ScrollableList
from view.widget.spin_box import SpinBox

from utils.toast_utils import show_toast


class Sidebar(QWidget):
    currentIndexChanged = pyqtSignal(int)
    loadSlicesRequested = pyqtSignal()
    loadPhantomRequested = pyqtSignal()

    def __init__(self,main_window):
        super().__init__()
        self.setFixedWidth(330)

        self.roi_enabled = False
        self.line_enabled = False

        self.slices = [] 

        self.main_window = main_window

        self.centeral_layout = QVBoxLayout(self)
        self.centeral_layout.setContentsMargins(0, 0, 0, 0)
        self.centeral_layout.setSpacing(0)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("sidebar_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.setSpacing(0)
        self.centeral_layout.addWidget(self.main_widget)

        self.buttons_container = QWidget()
        self.buttons_container.setObjectName("sidebar_buttons_container")
        self.buttons_container_layout = QVBoxLayout(self.buttons_container)
        self.buttons_container_layout.setContentsMargins(16, 16, 16, 16)
        self.buttons_container_layout.setSpacing(8)
        self.main_widget_layout.addWidget(self.buttons_container)

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Medium) 

        self.load_buttons_container = QWidget()
        self.load_button_layout = QHBoxLayout(self.load_buttons_container)
        self.load_button_layout.setContentsMargins(0,0,0,0)
        self.load_button_layout.setSpacing(8)
        

        self.load_slice_button = QPushButton("Load Slice")
        self.load_slice_button.setObjectName("load_button")
        self.load_slice_button.setFont(font)
        self.load_slice_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.load_phantom_button = QPushButton("Load Phantom")
        self.load_phantom_button.setObjectName("load_button")
        self.load_phantom_button.setFont(font)
        self.load_phantom_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.load_button_layout.addWidget(self.load_slice_button)
        self.load_button_layout.addWidget(self.load_phantom_button)
        self.buttons_container_layout.addWidget(self.load_buttons_container)

        self.reconstruct_button = QPushButton("Reconstruct")
        self.reconstruct_button.setObjectName("reconstruct_button")
        self.reconstruct_button.setFont(font)
        self.reconstruct_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.buttons_container_layout.addWidget(self.reconstruct_button)



        self.controls_widget = QWidget()
        self.controls_widget.setObjectName("controls_widget")
        self.controls_widget_layout = QVBoxLayout(self.controls_widget)
        self.controls_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.controls_widget_layout.setSpacing(25)
        self.controls_widget_layout.setContentsMargins(16, 16, 16, 16)
        self.main_widget_layout.addWidget(self.controls_widget)
        
        
        self.range_container = QWidget()
        self.range_container_layout = QVBoxLayout(self.range_container)
        self.range_container_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.range_container)

        self.range_header = QLabel("Angle Range")
        self.range_header.setFont(font)
        self.range_container_layout.addWidget(self.range_header)
        self.range_container_layout.setSpacing(10)

        font = QFont("Segoe UI", 9)
        font.setWeight(QFont.Weight.Normal) 

        self.angle_range_inputs_container = QWidget()
        self.angle_range_inputs_container_layout = QVBoxLayout(self.angle_range_inputs_container)
        self.range_container_layout.addWidget(self.angle_range_inputs_container)
        self.angle_range_inputs_container_layout.setContentsMargins(16,0,0,0)

        self.range_start_spin_box = SpinBox("Start")
        self.range_start_spin_box.set_font(font)
        self.angle_range_inputs_container_layout.addWidget(self.range_start_spin_box)
        self.range_end_spin_box = SpinBox("End")
        self.range_end_spin_box.set_font(font)
        self.angle_range_inputs_container_layout.addWidget(self.range_end_spin_box)
        self.angle_step_spin_box = SpinBox("Step")
        self.angle_step_spin_box.set_font(font)
        self.angle_range_inputs_container_layout.addWidget(self.angle_step_spin_box)       

        self.add_excluded_angle_container = QWidget()
        self.add_excluded_angle_container.setObjectName("sidebar_buttons_container")
        self.add_excluded_angle_container_layout = QVBoxLayout(self.add_excluded_angle_container)
        self.add_excluded_angle_container_layout.setContentsMargins(0,0,0,0)
        self.add_excluded_angle_container_layout.setSpacing(8)
        self.controls_widget_layout.addWidget(self.add_excluded_angle_container)

        # font = QFont("Segoe UI", 10)
        # font.setWeight(QFont.Weight.Medium) 
        # self.excluded_angle_header = QLabel("Exclude Angle")
        # self.excluded_angle_header.setFont(font)
        # self.add_excluded_angle_container_layout.addWidget(self.excluded_angle_header)

        self.excluded_angle_inputs_container = QWidget()
        self.excluded_angle_inputs_layout = QHBoxLayout(self.excluded_angle_inputs_container)
        self.excluded_angle_inputs_layout.setContentsMargins(0,0,0,0)
        self.excluded_angle_inputs_layout.setSpacing(8)
        self.add_excluded_angle_container_layout.addWidget(self.excluded_angle_inputs_container)

        font = QFont("Segoe UI", 9)
        font.setWeight(QFont.Weight.Normal) 

        self.excluded_angle_spin_box = SpinBox(label_text="Angle", decimals=2, initial_value=0)
        self.excluded_angle_spin_box.set_font(font)
        self.excluded_angle_inputs_layout.addWidget(self.excluded_angle_spin_box)

        self.add_excluded_angle_button = QPushButton("Add Excluded Angle")
        self.add_excluded_angle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Medium) 
        self.add_excluded_angle_button.setFont(font)
        self.add_excluded_angle_button.setObjectName("add_excluded_angle_button")
        self.add_excluded_angle_container_layout.addWidget(self.add_excluded_angle_button)
        self.add_excluded_angle_button.clicked.connect(self.on_excluded_angle_added)


        self.item_list_container = QWidget()
        self.item_list_container.setObjectName("item_list_container")
        self.item_list_container_layout = QVBoxLayout(self.item_list_container)
        self.item_list_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.item_list_container_layout.setContentsMargins(16,16,0,0)
        self.item_list_container_layout.setSpacing(0)
        self.main_widget_layout.addWidget(self.item_list_container)

        font = QFont("Segoe UI", 12)
        font.setWeight(QFont.Weight.Medium) 

        self.item_list_header = QLabel("Excluded Angels")
        self.item_list_header.setFont(font)
        self.item_list_container_layout.addWidget(self.item_list_header)
        self.item_list_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.item_list = ScrollableList(self.main_window)
        self.item_list_container_layout.addWidget(self.item_list, stretch=1)

        


    def on_excluded_angle_added(self):
        angle_value = self.excluded_angle_spin_box.value()
        
        if self.item_list.is_item_exist(angle_value):
            show_toast(
                self.main_window, 
                title="Angle Already Exists", 
                text=f"Angle {angle_value}° is already excluded.",
                type="ERROR"
            )
            return
        
        self.item_list.append_item(angle_value)

        show_toast(
            self.main_window, 
            title="Angle Excluded", 
            text=f"Angle {angle_value}° added successfully.",
            type="SUCCESS"
        )