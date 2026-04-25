class ReconstructionController:
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.main_window.sidebar.reconstruct_button.clicked.connect(self.reconstruct)

    def reconstruct(self):
        reconstruction_method = self.main_window.sidebar.reconstruction_method_combo_box.current_text()
        # reconstruction_method = self.main_window.sidebar.reconstruction_method_combo_box.current_index()
        angle_range_start = self.main_window.sidebar.range_start_spin_box.value()
        angle_range_end = self.main_window.sidebar.range_end_spin_box.value()
        angle_step = self.main_window.sidebar.angle_step_spin_box.value()
        excluded_angles_list = self.main_window.sidebar.item_list.get_items()

        print(reconstruction_method, angle_range_start, angle_range_end, angle_step, excluded_angles_list)
        
        