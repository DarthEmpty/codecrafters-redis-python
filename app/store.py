class Store:
    def __init__(self):
        self.contents = {}
    
    def get(self, key):
        return self.contents[key]
    
    def set(self, key, value):
        self.contents[key] = value