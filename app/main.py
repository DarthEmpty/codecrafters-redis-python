from asyncore import read
import socket
import threading
from app.resp_handlers import RESPStreamReader, RESPStreamDecoder


def client_loop(connection):
    print("thread spawned")
    while True:
        try:
            command, *args = RESPStreamDecoder(connection).decode()

            if command == b"ping":
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
