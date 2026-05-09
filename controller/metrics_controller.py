import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from utils.toast_utils import show_toast

class MetricsController:
    def __init__(self, main_window):
        self.main_window = main_window
        # It has a problem that it calls the function before the reconstructed image is updated.
        # We need to find a better way to trigger this after reconstruction is done.
        # For now, we can just call this function manually after reconstruction to see the metrics update.
        # self.main_window.sidebar.reconstruct_button.clicked.connect(self.update_metrics)

    def _prepare_metric_inputs(self, reference_slice, reconstructed_slice):
        reference_slice = np.asarray(reference_slice, dtype=np.float32)
        reconstructed_slice = np.asarray(reconstructed_slice, dtype=np.float32)

        if reference_slice.shape != reconstructed_slice.shape:
            raise ValueError("Reference and reconstructed slices must have the same shape to compute metrics.")

        combined_min = min(float(reference_slice.min()), float(reconstructed_slice.min()))
        combined_max = max(float(reference_slice.max()), float(reconstructed_slice.max()))
        scale = combined_max - combined_min

        if scale > 0:
            reference_slice = (reference_slice - combined_min) / scale
            reconstructed_slice = (reconstructed_slice - combined_min) / scale
        else:
            reference_slice = np.zeros_like(reference_slice, dtype=np.float32)
            reconstructed_slice = np.zeros_like(reconstructed_slice, dtype=np.float32)

        return reference_slice.astype(np.float32, copy=False), reconstructed_slice.astype(np.float32, copy=False)

    def update_metrics(self):
        ref_viewer_data = self.main_window.reference_slice_viewer.data
        recon_viewer_data = self.main_window.reconstructed_slice_viewer.data

        if ref_viewer_data is None or recon_viewer_data is None:
            show_toast(self.main_window, "Error", "Both reference and reconstruction slices must be loaded to compute metrics.", type="ERROR")
            return
        
        psnr_value, ssim_value = self.compute_metrics(ref_viewer_data, recon_viewer_data)

        self.show_metrics_on_GUI(psnr_value, ssim_value)

    def compute_metrics(self, reference_slice, reconstructed_slice):
        reference_slice, reconstructed_slice = self._prepare_metric_inputs(reference_slice, reconstructed_slice)

        psnr_value = self.caluculate_psnr(reference_slice, reconstructed_slice)
        ssim_value, _ = ssim(reference_slice, reconstructed_slice, full=True, data_range=1.0)

        psnr_value = round(psnr_value, 2)
        ssim_value = round(ssim_value, 4)

        return psnr_value, ssim_value
    
    def caluculate_psnr(self, reference_slice, reconstructed_slice):
        mask = self.calculate_mask(reference_slice, reconstructed_slice)

        ref_roi = reference_slice[mask]
        recon_roi = reconstructed_slice[mask]

        psnr_value = cv2.PSNR(ref_roi, recon_roi, 1.0)

        return psnr_value
    
    def calculate_ssim(self, reference_slice, reconstructed_slice):
        ssim_value, _ = ssim(reference_slice, reconstructed_slice, full=True, data_range=1.0)

        return ssim_value
    
    def calculate_mask(self, reference_slice, reconstructed_slice):
        mask = reference_slice > 0.05

        return mask

    def show_metrics_on_GUI(self, psnr_value, ssim_value):
        self.main_window.PSNR_metric.set_value(str(psnr_value) + " dB")
        self.main_window.SSIM_metric.set_value(str(ssim_value))