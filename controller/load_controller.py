class LoadController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.load_slice_button.clicked.connect(self.load_reference_slice)
        self.main_window.sidebar.load_phantom_button.clicked.connect(self.load_reference_slice)

    def load_reference_slice(self):
        print("load_reference_slice")
        