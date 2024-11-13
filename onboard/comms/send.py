import socket
import pickle
import struct

import cv2

# Initialize video capture from the default camera
vid = cv2.VideoCapture(0)

# Create a socket server
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.bind(("192.168.1.100", 9999))
send_socket.listen(10)  # max queue size 10

# Accept basestation connection
base_socket, base_address = send_socket.accept()
print(f"[*] Accepted connection from {base_address}")

while True:
    # Read a frame from the camera
    ret, frame = vid.read()

    # Serialise the frame to bytes
    serialised_frame = pickle.dumps(frame)

    # Pack the data size and frame data
    message_size = struct.pack("L", len(serialised_frame))
    base_socket.sendall(message_size + serialised_frame)

    # Display the frame on the send-side
    cv2.imshow("Send Video", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
vid.release()
cv2.destroyAllWindows()
