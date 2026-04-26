import numpy as np
from skimage.transform import radon, iradon
from utils.toast_utils import show_toast
from skimage.transform import resize
try:
     import astra
except ImportError:
     print("ASTRA toolbox not found. ASTRA-based reconstruction methods will not be available.")

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
        angles = np.arange(angle_range_start, angle_range_end+angle_step, angle_step)
        
        # Remove excluded angles (using a small tolerance for floating point matching)
        if excluded_angles_list:
            angles = [a for a in angles if not any(np.isclose(a, ex, atol=0.1) for ex in excluded_angles_list)]
            
        if len(angles) == 0:
            show_toast(self.main_window, "Error", "No angles available for reconstruction.", type="ERROR")
            return

        if reconstruction_method == "FBP":
            self.FBP_Reconstruction(original_image, angles)
        else:
            # Algorithm selection
            try:
                if astra.use_cuda():
                    if reconstruction_method == "SART":
                        alg_type = "SART_CUDA"
                    elif reconstruction_method == "SIRT":
                        alg_type = "SIRT_CUDA"
                else:
                    
                    if reconstruction_method == "SART":
                        alg_type = "SART"
                    elif reconstruction_method == "SIRT":
                        alg_type = "SIRT"
                self.ASTRA_Reconstruction(original_image, angles, alg_type)
            except NameError:
                show_toast(self.main_window, "Error", "ASTRA toolbox not available. Cannot perform ASTRA-based reconstruction.", type="ERROR")

    def FBP_Reconstruction(self, original_image, angles):
        try:
                # 1. Forward projection (radon transform)
                sinogram = radon(original_image, theta=angles)
                
                # Update Sinogram Plot
                self.main_window.sinogram_window.set_data(sinogram, angles)

                # 2. Filtered back projection (iradon transform)
                reconstructed_image = iradon(sinogram, theta=angles, filter_name='ramp')
                
                # Show image
                self.main_window.reconstructed_slice_viewer.set(reconstructed_image)
                self.main_window.ft_controller.update_refrence_slice_ft(original_image)
                self.main_window.ft_controller.update_reconstructed_slice_ft(reconstructed_image)
                show_toast(self.main_window, "Success", "FBP Reconstruction completed.", type="SUCCESS")
        except Exception as e:
                show_toast(self.main_window, "Error", f"Reconstruction failed: {str(e)}", type="ERROR")

    def ASTRA_Reconstruction(self, original_image, original_angles, alg_type):
         try:
              # Convert to radians
                angles = np.deg2rad(original_angles)

                # Volume geometry
                vol_geom = astra.create_vol_geom(256, 256)

                # Projection geometry
                proj_geom = astra.create_proj_geom('parallel', 1.0, 256, angles)

                # Projector
                if astra.use_cuda():
                    proj_id = astra.create_projector('cuda', proj_geom, vol_geom)
                else:
                    proj_id = astra.create_projector('linear', proj_geom, vol_geom)
                # Forward projection
                sinogram_id, sinogram = astra.create_sino(original_image, proj_id)
                self.sinogram = resize(sinogram,(256,256),anti_aliasing=True)

                # Reconstruction volume
                rec_id = astra.data2d.create('-vol', vol_geom)

                # Configure algorithm
                alg_cfg = astra.astra_dict(alg_type)
                alg_cfg['ReconstructionDataId'] = rec_id
                alg_cfg['ProjectionDataId'] = sinogram_id
                alg_cfg['ProjectorId'] = proj_id

                # Run reconstruction
                alg_id = astra.algorithm.create(alg_cfg)
                astra.algorithm.run(alg_id, 50)

                reconstruction = astra.data2d.get(rec_id)

                # Cleanup
                astra.algorithm.delete(alg_id)
                astra.data2d.delete(sinogram_id)
                astra.projector.delete(proj_id)

                # Display
                self.main_window.sinogram_window.set_data(sinogram, original_angles)
                self.main_window.reconstructed_slice_viewer.set(reconstruction)
                self.main_window.ft_controller.update_refrence_slice_ft(original_image)
                self.main_window.ft_controller.update_reconstructed_slice_ft(reconstruction)
                show_toast(self.main_window, "Success", "ASTRA Reconstruction completed.", type="SUCCESS")
                
         except Exception as e:
                show_toast(self.main_window, "Error", f"Reconstruction failed: {str(e)}", type="ERROR")
