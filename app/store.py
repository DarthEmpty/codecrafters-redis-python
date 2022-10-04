from time import time_ns

class Store:
    def __init__(self):
        self.contents = {}
    
    def get(self, key):
        if key in self.contents:
            value, expired = self.contents[key]
            
            if time_ns() > expired:
                return value

        return None
    
    def set(self, key, value, expiry=None):
        if expiry:
            # expiry in millisecs, time_ns in nanosecs
            expired = time_ns() + expiry * 1e6 
            self.contents[key] = (value, expired)
        
        else:
            self.contents[key] = (value, None)