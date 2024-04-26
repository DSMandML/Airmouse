

class Config:
    def __init__(self):
        """
        Configuration class.
        Define all the configurations and hyperparameters here.
        Pre-defines indicies for different fingers.
        """
        self.wrist = (0)
        self.thumb = (1, 2, 3, 4)
        self.index = (5, 6, 7, 8)
        self.middle = (9, 10, 11, 12)
        self.ring = (13, 14, 15, 16)
        self.small = (17, 18, 19, 20)
        self.finger_to_lock = self.index[-1]
