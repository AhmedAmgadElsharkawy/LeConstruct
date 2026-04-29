import numpy as np

class FTController:
    def __init__(self, main_window):
        # Store the main window reference so we can reach the FT viewers
        self.main_window = main_window
        # Update the reference FT whenever the reference image changes
        self.main_window.reference_slice_viewer.imageChanged.connect(self.update_refrence_slice_ft)
        # Update the reconstructed FT whenever the reconstruction changes
        self.main_window.reconstructed_slice_viewer.imageChanged.connect(self.update_reconstructed_slice_ft)

    def _compute_ft_image(self, image_data: np.ndarray) -> np.ndarray:
        # Ensure the input is a NumPy array so FFT functions work reliably
        data = np.asarray(image_data)
        # Convert to float32 to keep the FFT fast and memory usage reasonable
        data = data.astype(np.float32, copy=False)
        # Compute the 2D Fourier transform of the image
        fft2 = np.fft.fft2(data)
        # Shift the zero-frequency component to the center for display
        fft2_shifted = np.fft.fftshift(fft2)
        # Take the magnitude because the FFT result is complex-valued
        magnitude = np.abs(fft2_shifted)
        # Use log scaling to compress the dynamic range for visualization
        log_magnitude = np.log1p(magnitude)
        # Compute the minimum and maximum value so we can normalize the image between 0 & 1
        min_val = log_magnitude.min()
        max_val = log_magnitude.max()
        scale = max_val - min_val + 1e-8
        normalized = (log_magnitude - min_val) / scale
        return normalized

    def update_refrence_slice_ft(self, refrence_slice_ft_date):
        # If there is no image, clear the FT viewer to match the empty state
        if refrence_slice_ft_date is None:
            self.main_window.reference_slice_ft_viewer.reset()
            return
        # Compute the Fourier transform visualization for the reference slice
        ft_image = self._compute_ft_image(refrence_slice_ft_date)
        self.main_window.reference_slice_ft_viewer.set(ft_image)

    def update_reconstructed_slice_ft(self, reconstructed_slice_ft_data):
        if reconstructed_slice_ft_data is None:
            self.main_window.reconstructed_slice_ft_viewer.reset()
            return
        ft_image = self._compute_ft_image(reconstructed_slice_ft_data)
        self.main_window.reconstructed_slice_ft_viewer.set(ft_image)

        
        