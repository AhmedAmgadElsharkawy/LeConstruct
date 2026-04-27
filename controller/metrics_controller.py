import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from utils.toast_utils import show_toast

class MetricsController:
    def __init__(self, main_window):
        self.main_window = main_window
        # self.main_window.sidebar.reconstruct_button.clicked.connect(self.update_metrics)

    def update_metrics(self):
        ref_viewer_data = self.main_window.reference_slice_viewer.data
        recon_viewer_data = self.main_window.reconstructed_slice_viewer.data

        if ref_viewer_data is None or recon_viewer_data is None:
            show_toast(self.main_window, "Error", "Both reference and reconstruction slices must be loaded to compute metrics.", type="ERROR")
            return
        
        psnr_value = cv2.PSNR(ref_viewer_data, recon_viewer_data)

        ssim_value, _ = ssim(ref_viewer_data, recon_viewer_data, full=True, data_range=1.0)
        show_toast(self.main_window, "Success", f"SSIM: {ssim_value}", type="SUCCESS")
        