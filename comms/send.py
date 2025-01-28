# Deploy on the "child" device i.e. PiB to allow it to communicate with the "parent" device i.e. PiA

import os
import socket
from os import listdir

def list_images(folder_path, client_socket):
    # get the path/directory
        images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            print("No images found")
            client_socket.close()
            return

        print(len(images))
        client_socket.sendall(f"{len(images)}".encode())

        for image in images:
            filesize = os.path.getsize(image)
            
            filename = os.path.basename(image)

            client_socket.sendall(f"{filename}|{filesize}".encode())

            # Wait for acknowledgment
            ack = client_socket.recv(1024).decode()
            if ack != "READY":
                print("Server is not ready to receive the file.")
                return
    
            # Send the image file
            with open(folder_path, "rb") as file:
                while (chunk := file.read(1024)):
                    client_socket.sendall(chunk)
            
            print(f"Image {filename} sent successfully!")
        
        print("All images sent!")
        return

def send_images(path, ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((ip, port))
        print(f"Connected to {ip}:{port}")

        list_images("./", client_socket)
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    ip = "10.12.23.188"
    test_ip = "10.12.71.113"
    port = 5002
    path = ""

    send_images(path, ip, port)
