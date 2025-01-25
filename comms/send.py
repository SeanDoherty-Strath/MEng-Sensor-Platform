# Deploy on the "child" device i.e. PiB to allow it to communicate with the "parent" device i.e. PiA

import os
import socket

def send_images(path, ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((ip, port))
        print(f"Connected to {ip}:{port}")

    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5001
    path = ""

    send_images(path, ip, port)