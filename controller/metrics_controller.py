class MetricsController:
    def __init__(self, main_window):
        self.main_window = main_window
        
        self.main_window.sidebar.reconstruct_button.clicked.connect(self.update_metrics)
        # There is also a signal in the viewer that can be used

    def update_metrics(self):
        print("update_metrics")
        
        