import pickle
import socket
import struct

import cv2

# Create a socket
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.connect(("192.168.1.59", 9999))

received_data = b""
payload_size = struct.calcsize("L")

while True:
    # Receive and assemble the data until the payload size is reached
    while len(received_data) < payload_size:
        received_data += receive_socket.recv(4096)

    # Extract the packed message size
    packed_msg_size = received_data[:payload_size]
    received_data = received_data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Receive and assemble the frame data until the complete frame is received
    while len(received_data) < msg_size:
        received_data += receive_socket.recv(4096)

    # Extract the frame data
    frame_data = received_data[:msg_size]
    received_data = received_data[msg_size:]

    # Deserialize the received frame
    received_frame = pickle.loads(frame_data)

    # Display the received frame
    cv2.imshow("Receive Video", received_frame)

    # Press ‘q’ to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
receive_socket.close()
