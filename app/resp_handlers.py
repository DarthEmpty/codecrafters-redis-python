class RESPStreamDecoder:
    def __init__(self, connection):
        super()
        self.reader = RESPStreamReader(connection)

    def decode(self):
        resp_type = self.reader.read(1)

        if resp_type == b"+":
            return self._simple_string()

        elif resp_type == b"$":
            return self._bulk_string()

        elif resp_type == b"*":
            return self._array()
        
        else:
            raise Exception(f"Unknown data type byte: {resp_type}")
    
    def _simple_string(self):
        return self.reader.read_until_delimiter()

    def _bulk_string(self):
        # TODO: figure out why this method hangs
        size = int(self.reader.read_until_delimiter())

        if size == -1:
            return None
        
        else:
            data = self.reader.read(size)

            # Ensure that delimiter is immediately after the string
            # assert self.reader.read_until_delimiter() == b"" 
            return data

    def _array(self):
        size = int(self.reader.read_until_delimiter())        
        data = []

        for _ in range(size):
            data.append(self.decode())
        
        return data


class RESPStreamReader:
    DEFAULT_MAX_BYTES = 1024

    def __init__(self, connection):
        self.connection = connection
        self.buffer = b""

    def _load_to_buffer(self):
        data = self.connection.recv(RESPStreamReader.DEFAULT_MAX_BYTES)            
        self.buffer += data

    def read(self, bytes_no=DEFAULT_MAX_BYTES):
        if len(self.buffer) < bytes_no:
            self._load_to_buffer()

        data, self.buffer = self.buffer[:bytes_no], self.buffer[bytes_no:]
        
        return data

    def read_until_delimiter(self, delimiter=b"\r\n"):
        while delimiter not in self.buffer:
            self._load_to_buffer()
        
        data, self.buffer = self.buffer.split(delimiter, maxsplit=1)

        return data
