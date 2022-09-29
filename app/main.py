import socket
import threading

def client_loop(connection):
    while True:
        connection.recv(1024) # wait for client to send data
        connection.send(b"+PONG\r\n")



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_connection, _ = server_socket.accept() # wait for client
        threading.Thread(target=client_loop, args=(client_connection,))



if __name__ == "__main__":
    main()
