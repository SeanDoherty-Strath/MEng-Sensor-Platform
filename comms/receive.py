# Deploy on the "parent" device i.e. PiA to allow it to receive information from the "child" device i.e. PiB

import socket
import os

def receive_image(save_location, host, port):
    try:
        os.makedirs(save_dir, exist_ok=True)
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host,port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        # Accept a connection
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        
        # Send acknowledgment
        num_images = int(conn.recv(1024).decode())
        conn.sendall(b"READY")
        print(f"Expecting {num_images} images.")

        for i in range(num_images):
            # Receive image metadata
            metadata = conn.recv(1024).decode()
            filename, file_size = metadata.split("|")
            file_size = int(file_size)

            # Prepare to receive the file
            save_path = os.path.join(save_location, filename)
            print(save_path)
            with open(save_path, "wb") as file:
                received_size = 0
                while received_size < file_size:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    received_size += len(chunk)
            
            print(f"Image received and saved at {save_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    port = 5002
    host = "0.0.0.0" # i.e. listening
    save_location = "./received_images"

    receive_image(save_location, host, port)