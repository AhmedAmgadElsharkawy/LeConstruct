from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidgetItem,
    QFileDialog, QLabel, QSizePolicy
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
        self.controls_widget_layout = QVBoxLayout(self.controls_widget)
        self.controls_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.controls_widget_layout.setSpacing(25)
        self.controls_widget_layout.setContentsMargins(16, 16, 16, 16)
        self.main_widget_layout.addWidget(self.controls_widget,stretch=1)
        
        
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

        self.range_start_spin_box = SpinBox("Start")
        self.range_start_spin_box.set_font(font)
        self.range_container_layout.addWidget(self.range_start_spin_box)
        self.range_end_spin_box = SpinBox("End")
        self.range_end_spin_box.set_font(font)
        self.range_container_layout.addWidget(self.range_end_spin_box)
        self.angle_step_spin_box = SpinBox("Step")
        self.angle_step_spin_box.set_font(font)
        self.range_container_layout.addWidget(self.angle_step_spin_box)       


        # self.slice_list_container = QWidget()
        # self.slice_list_container_layout = QVBoxLayout(self.slice_list_container)
        # self.slice_list_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.slice_list_container_layout.setContentsMargins(16,16,0,0)
        # self.slice_list_container_layout.setSpacing(0)
        # self.main_widget_layout.addWidget(self.slice_list_container)

        # font = QFont("Segoe UI", 12)
        # font.setWeight(QFont.Weight.Medium) 

        # self.slice_list_header = QLabel("Loaded Slices")
        # self.slice_list_header.setFont(font)
        # self.slice_list_container_layout.addWidget(self.slice_list_header)
        # self.slice_list_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # font = QFont("Segoe UI", 12)
        # font.setWeight(QFont.Weight.Light) 
        # self.no_slices_label = QLabel("No Slices Loaded")
        # self.no_slices_label.setFont(font)
        # self.slice_list_container_layout.addWidget(self.no_slices_label)
        # self.no_slices_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # self.slice_list = ScrollableList()
        # self.slice_list_container_layout.addWidget(self.slice_list, stretch=1)
        # self.slice_list.setVisible(False)
        self.add_excluded_angle_container = QWidget()
        self.add_excluded_angle_container.setObjectName("sidebar_buttons_container")
        self.add_excluded_angle_container_layout = QVBoxLayout(self.add_excluded_angle_container)
        self.add_excluded_angle_container_layout.setContentsMargins(0,0,0,0)
        self.add_excluded_angle_container_layout.setSpacing(8)
        self.controls_widget_layout.addWidget(self.add_excluded_angle_container)

        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Medium) 
        self.excluded_angle_header = QLabel("Exclude Angle")
        self.excluded_angle_header.setFont(font)
        self.add_excluded_angle_container_layout.addWidget(self.excluded_angle_header)

        self.excluded_angle_inputs_container = QWidget()
        self.excluded_angle_inputs_layout = QHBoxLayout(self.excluded_angle_inputs_container)
        self.excluded_angle_inputs_layout.setContentsMargins(0,0,0,0)
        self.excluded_angle_inputs_layout.setSpacing(8)
        self.add_excluded_angle_container_layout.addWidget(self.excluded_angle_inputs_container)

        font = QFont("Segoe UI", 9)
        font.setWeight(QFont.Weight.Normal) 

        self.excluded_angle_spin_box = SpinBox(label_text="Angle (Degree)", decimals=2, initial_value=0)
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

        self.item_list_header = QLabel("Cysts")
        self.item_list_header.setFont(font)
        self.item_list_container_layout.addWidget(self.item_list_header)
        self.item_list_header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.item_list = ScrollableList(self.main_window)
        self.item_list_container_layout.addWidget(self.item_list, stretch=1)

        


    def on_excluded_angle_added(self):
            # new_cyst = CystItem(
            #     depth= self.depth_spin_box.value(),
            #     lateral= self.lateral_spin_box.value(),
            #     radius = self.radius_spin_box.value()
            # )
            
            # is_cyst_exists = self.main_window.phantom_controller.is_cyst_exists(new_cyst)

            # if is_cyst_exists:
            #     show_toast(self.main_window, "Cyst Already Exists",f"Cyst (d={self.depth_spin_box.value()}, l={self.lateral_spin_box.value()}, r={self.radius_spin_box.value()}) already exists.")
            #     return
            
            # self.main_window.phantom_controller.add_cyst(new_cyst)
            # self.item_list.append_item(new_cyst)

            show_toast(self.main_window, "Cyst Added",f"Cyst (d={self.excluded_angle_spin_box.value()}, l={self.lateral_spin_box.value()}, r={self.radius_spin_box.value()}) added successfully.")


    # def is_cyst_exists(self, cyst: CystItem):
    #     for existing_cyst in self.cysts:
    #         if existing_cyst['x'] == cyst.get_lateral() and existing_cyst['z'] == cyst.get_depth() and existing_cyst['radius'] == cyst.get_radius():
    #             return True
    #     return False
    
    # def add_cyst(self, cyst: CystItem):
    #     self.cysts.append({"x": cyst.get_lateral(), "z": cyst.get_depth(), "radius": cyst.get_radius()})