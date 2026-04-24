from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem
)

from PyQt5.QtCore import Qt, pyqtSignal

from view.widget.slice_item import SliceItem

class ScrollableList(QWidget):
    itemSelectionChanged = pyqtSignal()
    
    def __init__(self, selectable=False, multi_select=False, delete = True):
        super().__init__()

        self.slices = []
        self.delete = delete
        self.selectable = selectable
        self.multi_select = multi_select

        self.central_layout = QVBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)

        self.main_widget = QWidget()
        self.central_layout.addWidget(self.main_widget)
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.setSpacing(0)

        self.slice_list = QListWidget()
        self.slice_list.setFocusPolicy(Qt.NoFocus)
        self.slice_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.slice_list.setObjectName("slice_list")
        self.main_widget_layout.addWidget(self.slice_list, stretch=1)

        if self.selectable:
            self.slice_list.setSelectionMode(
                QAbstractItemView.MultiSelection if self.multi_select else QAbstractItemView.SingleSelection
            )
        else:
            self.slice_list.setSelectionMode(QAbstractItemView.NoSelection)

        self.slice_list.itemSelectionChanged.connect(self.itemSelectionChanged.emit)



    def update_slice_list(self):
        self.slice_list.clear()
        for i, s in enumerate(self.slices):
            delete_callback = self.delete_slice if self.delete else None
            item_widget = SliceItem(slice_obj=s, delete_callback=delete_callback, index=i)
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

    def append_slices(self,new_slices):
        self.slices.extend(new_slices)
        self.update_slice_list()

    def set_slices(self,new_slices):
        self.slices = new_slices
        self.update_slice_list()


    def selectedItems(self):
        return self.slice_list.selectedItems()

    def itemWidget(self, item):
        return self.slice_list.itemWidget(item)

    def clearSelection(self):
        self.slice_list.clearSelection()

    def setSelectionMode(self, mode):
        self.slice_list.setSelectionMode(mode)

    def get_selected_slices(self):
        return [
            self.itemWidget(item).slice_obj
            for item in self.selectedItems()
            if self.itemWidget(item) is not None
        ]


