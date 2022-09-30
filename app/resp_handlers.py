from typing import Callable


class RESPDecoder(Callable):
    def __call__(self, resp: bytes):
        if resp.startswith(b"+"):
            return self._simple_string(resp)
        
        elif resp.startswith(b"*"):
            pass
        
        else:
            raise Exception(f"Unknown data type byte: {resp[0]}")
    
    def _simple_string(resp: bytes):
        return resp[1:].strip()


class RESPEncoder:
    pass


class BufferedReader:
    DEFAULT_BUFFER_SIZE = 1024

    def __init__(self, connection):
        self.connection = connection
    
    def read(self, buf_size=DEFAULT_BUFFER_SIZE):
        data = self.connection.recv(buf_size)

        return None if not data else bytes(data)