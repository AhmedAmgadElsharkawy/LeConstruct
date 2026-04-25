import numpy as np

class Slice:
    def __init__(self, name: str, data: np.ndarray , volume=None, z_index=None):
        self.name = name
        self.data = data
        self.volume = volume   
        self.z_index = z_index 