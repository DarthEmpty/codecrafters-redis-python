from asyncore import read
import socket
import threading
from app.resp_handlers import BufferedReader, RESPDecoder


def client_loop(connection):
    print("thread spawned")
    reader = BufferedReader(connection)
    decode = RESPDecoder()

    while True:
        try:
            resp = reader.read() # wait for client to send data
            print(resp)
            command = decode(resp)

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
