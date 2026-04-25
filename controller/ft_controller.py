class FTController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.reference_slice_viewer.imageChanged.connect(self.update_refrence_slice_ft)
        self.main_window.reconstructed_slice_viewer.imageChanged.connect(self.update_reconstructed_slice_ft)

    def update_refrence_slice_ft(self,refrence_slice_ft_date):
        print("update_refrence_slice_ft", refrence_slice_ft_date)

    def update_reconstructed_slice_ft(self,reconstructed_slice_ft_data):
        print("update_reconstructed_slice_ft", reconstructed_slice_ft_data)

        
        