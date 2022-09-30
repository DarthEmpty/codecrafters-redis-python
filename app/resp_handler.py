class RESPDecoder:
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
