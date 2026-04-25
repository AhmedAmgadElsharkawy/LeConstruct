from pyqtgraph.functions import gaussianFilter
from qtpy.QtWidgets import QFileDialog
from model.slice_model import Slice
import nibabel as nib
import numpy as np

from utils.toast_utils import show_toast

class LoadController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.load_slice_button.clicked.connect(self.load_reference_slice)
        self.main_window.sidebar.load_phantom_button.clicked.connect(self.load_phantom_slice)

    def load_reference_slice(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Select CT File",
            "",
            "NIfTI Files (*.nii *.nii.gz)"
        )

        if not file_path:
            return

        # 2. Load volume
        img = nib.load(file_path)
        volume = img.get_fdata().astype(np.float32)

        # 3. CT range clipping (optional but good)
        volume = np.clip(volume, -1000, 1000)

        # 4. Normalize for display
        volume = (volume - volume.min()) / (volume.max() - volume.min() + 1e-8)

        # 5. Pick ONE slice (middle slice is best default)
        z = volume.shape[2] // 2
        single_slice = volume[:, :, z]

        # 6. Create Slice object
        slice_obj = Slice(
            name=f"CT Slice {z}",
            data=single_slice,
            volume=volume,
            z_index=z
        )

        self.main_window.reference_slice_viewer.set(slice_obj.data)

        show_toast(
            self.main_window,
            "CT Loaded",
            f"Showing slice {z} from CT volume"
        )

    def load_phantom_slice(self):
        size = 256
        phantom = np.zeros((size, size), dtype=np.float32)

        rr, cc = np.ogrid[:size, :size]
        center = size // 2

        # 🔹 1. Background (air)
        phantom[:] = -1000

        # 🔹 2. Body (ellipse)
        body = ((rr - center)**2 / (100**2) + (cc - center)**2 / (80**2)) < 1
        phantom[body] = -100  # fat

        # 🔹 3. Chest soft tissue
        tissue = ((rr - center)**2 / (80**2) + (cc - center)**2 / (65**2)) < 1
        phantom[tissue] = 40

        # 🔹 4. Left lung
        left_lung = ((rr - center)**2 / (55**2) + (cc - (center - 35))**2 / (30**2)) < 1
        phantom[left_lung] = -800  # lung air

        # 🔹 5. Right lung
        right_lung = ((rr - center)**2 / (55**2) + (cc - (center + 35))**2 / (30**2)) < 1
        phantom[right_lung] = -800

        # 🔹 6. Add nodules (small circular artifacts) to RIGHT lung only
        for _ in range(6):
            r_offset = np.random.randint(-20, 20)
            c_offset = np.random.randint(10, 40)

            nodule = ((rr - (center + r_offset))**2 +
                    (cc - (center + c_offset))**2) < 5**2

            # ensure nodules stay inside right lung
            phantom[nodule & right_lung] = 100  # soft-tissue-like

        # 🔹 7. Spine (bone)
        spine = ((rr - center)**2 + (cc - center)**2) < 10**2
        phantom[spine] = 1000

        # 🔹 8. Texture (low-frequency variation)
        texture = gaussianFilter(np.random.randn(size, size), sigma=6)
        phantom += texture * 20

        # 🔹 9. Noise (scanner noise)
        noise = np.random.normal(0, 10, (size, size))
        phantom += noise

        # 🔹 10. Blur
        phantom = gaussianFilter(phantom, sigma=1)

        # 🔹 11. Clip HU range
        phantom = np.clip(phantom, -1000, 1000)

        # 🔹 12. Normalize for display
        display = (phantom - phantom.min()) / (phantom.max() - phantom.min() + 1e-8)

        slice_obj = Slice(
            name="Lung Phantom",
            data=display,
            volume=None,
            z_index=0
        )

        self.main_window.reference_slice_viewer.set(slice_obj.data)

        show_toast(
            self.main_window,
            "Phantom Loaded",
            "Synthetic CT slice generated"
        )