# LeConstruct
LeConstruct is a desktop application designed to simulate and visualize the CT image reconstruction process. The app allows users to explore how projection angles and reconstruction methods affect the final image, specifically focusing on the generation and mitigation of reconstruction artifacts.


## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Features](#features)
- [Contributors](#contributors)


## Prerequisites

- Python 3.6 or higher

## Installation

1. **Clone the repository:**

   ``````
   git clone https://github.com/AhmedAmgadElsharkawy/LeConstruct.git
   ``````

2. **Install The Dependincies:**
    ``````
    pip install -r requirements.txt
    ``````

3. **Run The App:**

    ``````
    python main.py
    ``````


## Features  

- **Flexible Data Input:**
  Load standard CT slices from external datasets or generate a built-in Phantom image. The loaded image serves as the ground truth and is displayed in the Reference Slice Viewer.

- **Comprehensive 4-Panel Visualization:**
  Simultaneously analyze the spatial and frequency domains using four dedicated viewers:
  - **Reference Slice Viewer:** Displays the original ground-truth image.
  - **Reference Slice Fourier Transform Viewer:** Displays the frequency domain (k-space) of the reference image.
  - **Reconstructed Slice Viewer:** Displays the resulting image after the reconstruction process.
  - **Reconstructed Slice Fourier Transform Viewer:** Displays the frequency domain of the reconstructed image.

- **Sinogram Visualization:**
  Generate and view the projection data (sinogram) used to create the reconstructed image.

- **Reconstruction Methods:**
  Choose between two distinct algorithmic approaches to reconstruct the image from the sinogram:
  - **Filtered Reconstruction** 
  - **Iterative Reconstruction (SIRT - SART)** 

- **Advanced Angle Controls:**
  Simulate different acquisition scenarios and explore how projection angles create reconstruction artifacts by adjusting:
  - **Range of Angles:** Define the total sweep of the projections.
  - **Angle Step:** Control the density or sparsity of the acquired projections.
  - **Exclude Angles List:** Specify certain angles to drop, allowing you to simulate missing data or limited-angle tomography artifacts.

- **Quantitative Metrics:**
  - **PSNR (Peak Signal-to-Noise Ratio):** Measures the pixel-wise numerical error between the images. 
  - **SSIM (Structural Similarity Index):** Measures the visual and structural similarity between the images.

## Contributors
- **AhmedAmgadElsharkawy**: [GitHub Profile](https://github.com/AhmedAmgadElsharkawy)
- **AbdullahMahmoudHanafy**: [GitHub Profile](https://github.com/AbdullahMahmoudHanafy)
- **zeyad-amr-22**: [GitHub Profile](https://github.com/zeyad-amr-22)
- **PavlyAwad**: [GitHub Profile](https://github.com/PavlyAwad)
- **mostafa-aboelmagd**: [GitHub Profile](https://github.com/mostafa-aboelmagd)


