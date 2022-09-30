import socket
import threading

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


def client_loop(connection):
    print("thread spawned")
    BUFFER_SIZE = 1024

    while True:
        try:
            resp = connection.recv(BUFFER_SIZE) # wait for client to send data
            command, *args = RESPDecoder(resp)

            if command == b"PING":
                connection.send(b"+PONG\r\n")
            else:
                connection.send(b"-ERR unknown command\r\n")

        except ConnectionError:
            break


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_connection, _ = server_socket.accept() # wait for client
        print("client found")

        threading.Thread(target=client_loop, args=(client_connection,)).start()



if __name__ == "__main__":
    main()
