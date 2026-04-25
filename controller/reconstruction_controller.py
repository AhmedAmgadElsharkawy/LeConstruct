import numpy as np
from skimage.transform import radon, iradon
from utils.toast_utils import show_toast

class ReconstructionController:
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.main_window.sidebar.reconstruct_button.clicked.connect(self.reconstruct)

    def reconstruct(self):
        reconstruction_method = self.main_window.sidebar.reconstruction_method_combo_box.current_text()
        angle_range_start = self.main_window.sidebar.range_start_spin_box.value()
        angle_range_end = self.main_window.sidebar.range_end_spin_box.value()
        angle_step = self.main_window.sidebar.angle_step_spin_box.value()
        excluded_angles_list = self.main_window.sidebar.item_list.get_items()

        print(reconstruction_method, angle_range_start, angle_range_end, angle_step, excluded_angles_list)

        ref_viewer = self.main_window.reference_slice_viewer
        if ref_viewer.data is None:
            show_toast(self.main_window, "Error", "No reference slice loaded.", type="ERROR")
            return

        original_image = ref_viewer.data

        # Build list of angles based on step & excluded angles
        if angle_step <= 0:
            show_toast(self.main_window, "Error", "Angle step must be strictly positive.", type="ERROR")
            return
        
        # start angle, end angle and the step.
        # smaller steps -> more projections to be smeared and added together -> better reconstruction but more computationally expensive
        angles = np.arange(angle_range_start, angle_range_end, angle_step)
        
        # Remove excluded angles (using a small tolerance for floating point matching)
        if excluded_angles_list:
            angles = [a for a in angles if not any(np.isclose(a, ex, atol=0.1) for ex in excluded_angles_list)]
            
        if len(angles) == 0:
            show_toast(self.main_window, "Error", "No angles available for reconstruction.", type="ERROR")
            return

        if reconstruction_method == "FBP":
            try:
                # 1. Forward projection (radon transform)
                sinogram = radon(original_image, theta=angles)
                
                # Update Sinogram Plot
                self.main_window.sinogram_window.set_data(sinogram, angles)

                # 2. Filtered back projection (iradon transform)
                reconstructed_image = iradon(sinogram, theta=angles, filter_name='ramp')
                
                # Show image
                self.main_window.reconstructed_slice_viewer.set(reconstructed_image)
                show_toast(self.main_window, "Success", "FBP Reconstruction completed.", type="SUCCESS")
            except Exception as e:
                show_toast(self.main_window, "Error", f"Reconstruction failed: {str(e)}", type="ERROR")
        else:
            show_toast(self.main_window, "Info", f"Method '{reconstruction_method}' not fully implemented yet.", type="INFO")
        
        