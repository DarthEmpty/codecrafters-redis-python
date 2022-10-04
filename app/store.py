from time import time_ns

class Store:
    def __init__(self):
        self.contents = {}
    
    def get(self, key):
        if key not in self.contents:
            return None

        value, expiry_time = self.contents[key]
        now = time_ns()

        if expiry_time and expiry_time <= now:
            return None

        print(expiry_time)
        print(now)

        return value
    
    def set(self, key, value, expiry=None):
        if expiry:
            # expiry in millisecs, time_ns in nanosecs
            expired = time_ns() + expiry * 1e6 
            self.contents[key] = (value, expired)
        
        else:
            self.contents[key] = (value, None)