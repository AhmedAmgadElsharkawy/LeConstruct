from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidgetItem,
    QFileDialog, QLabel, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt

from view.widget.slice_item import SliceItem
from view.widget.scrollable_list import ScrollableList
from view.widget.custom_spin_box import CustomSpinBox

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

        self.controls_widget = QWidget()
        self.controls_widget_layout = QVBoxLayout(self.controls_widget)
        self.controls_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.addWidget(self.controls_widget,stretch=1)
        
        
        self.range_container = QWidget()
        self.range_container_layout = QVBoxLayout(self.range_container)
        self.range_container_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.range_container)

        self.range_header = QLabel("Angle Range")
        self.range_container_layout.addWidget(self.range_header)

        self.range_start_spin_box = CustomSpinBox("Start")
        self.range_container_layout.addWidget(self.range_start_spin_box)
        self.range_end_spin_box = CustomSpinBox("End")
        self.range_container_layout.addWidget(self.range_end_spin_box)

        


        


    def update_slice_list(self):
        self.slice_list.clear()
        for i, s in enumerate(self.slices):
            item_widget = SliceItem(slice_obj=s, delete_callback=self.delete_slice, index=i)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.slice_list.addItem(item)
            self.slice_list.setItemWidget(item, item_widget)

    def delete_slice(self, index):
        if 0 <= index < len(self.slices):
            del self.slices[index]
            for i, s in enumerate(self.slices):
                s.index = i
            self.update_slice_list()
            


    def toggle_roi_mode(self):
        if hasattr(self.main_window, "slice_viewer1") and hasattr(self.main_window, "slice_viewer2"):
            self.roi_enabled = not self.roi_enabled
            self.line_enabled = False
            self.main_window.slice_viewer1.enable_roi_mode(self.roi_enabled)
            self.main_window.slice_viewer2.enable_roi_mode(self.roi_enabled)
            self.update_buttons()
            
            

    def toggle_line_profile_mode(self):
        if hasattr(self.main_window, "slice_viewer1") and hasattr(self.main_window, "slice_viewer2"):
            self.line_enabled = not self.line_enabled
            self.roi_enabled = False
            self.main_window.slice_viewer1.enable_line_mode(self.line_enabled)
            self.main_window.slice_viewer2.enable_line_mode(self.line_enabled)
            self.update_buttons()


    def update_buttons(self):
        self.roi_button.setProperty("active", self.roi_enabled)
        self.roi_button.style().unpolish(self.roi_button)
        self.roi_button.style().polish(self.roi_button)

        if(self.roi_enabled):
            self.roi_button.setText("ROI (Active)")
        else:
            self.roi_button.setText("ROI")

        self.line_profile_button.setProperty("active", self.line_enabled)
        self.line_profile_button.style().unpolish(self.line_profile_button)
        self.line_profile_button.style().polish(self.line_profile_button)

        if(self.line_enabled):
            self.line_profile_button.setText("Line (Active)")
        else:
            self.line_profile_button.setText("Line")
