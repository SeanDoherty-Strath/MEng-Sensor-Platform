# Deploy on the "parent" device i.e. PiA to allow it to receive information from the "child" device i.e. PiB

import socket
import os

def receive_image(save_location, host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host,port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        # Accept a connection
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    port = 5001
    host = "0.0.0.0" # i.e. listening
    save_location = ""

    receive_image(save_location, host, port)