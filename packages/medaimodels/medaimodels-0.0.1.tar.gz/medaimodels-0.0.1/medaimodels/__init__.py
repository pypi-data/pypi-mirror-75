class ModelOutput():
    
    def __init__(self, image=None, class_probabilities=None, mask=None, display=''):
        self.image = image
        self.class_probabilities = class_probabilities
        self.mask = mask
        self.display = display


    def __repr__(self):
        return self.display