import socket
import threading
from app.resp_handlers import RESPStreamDecoder, RESPEncoder
from app.store import Store


def client_loop(connection: socket.socket, store: Store):
    decoder = RESPStreamDecoder(connection)
    encoder = RESPEncoder()

    while True:
        try:
            command, *args = decoder.decode()

            print(command, *args)

            if command == b"ping":
                connection.send(encoder.to_simple_string(b"PONG"))

            elif command == b"echo":
                connection.send(encoder.to_bulk_string(args[0]))

            elif command == b"set":
                if b"px" in args:
                    store.set(args[0], args[1], int(args[3]))
                else:
                    store.set(args[0], args[1])

                connection.send(encoder.to_simple_string(b"OK"))

            elif command == b"get":
                payload = store.get(args[0])
                connection.send(encoder.to_bulk_string(payload))

            else:
                connection.send(encoder.to_error(b"ERR unknown command"))

        except ConnectionError:
            break


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    store = Store()

    while True:
        client_connection, _ = server_socket.accept() # wait for client
        threading.Thread(target=client_loop, args=(client_connection, store)).start()



if __name__ == "__main__":
    main()
