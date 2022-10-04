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
    DEFAULT_MAX_BYTES = 8

    def __init__(self, connection):
        self.connection = connection
        self.buffer = b""
    
    def read(self, max_bytes=DEFAULT_MAX_BYTES):
        # Prioritise reading from the buffer in case
        # there's data left over from read_until
        data = b""

        if self.buffer:
            data = self.buffer[:max_bytes]
            self.buffer = self.buffer[max_bytes:]

        # Read the remainder from the stream
        if (remainder := max_bytes - len(data)) > 0:
            data += self.connection.recv(remainder)

        return data
    
    def read_until_delimiter(self, delimiter=b"\r\n"):
        data = b""
        while delimiter not in data:
            data += self.read()
        
        data, self.buffer = data.split(delimiter, maxsplit=1)

        return data  # Excludes delim from return value
