from object_detection.object_detection import *
from comms.send import *
from cameras import *
from time import sleep

TRIGGER_PIN=26
last = 0

if __name__ == "__main__":
    # Setup cameras and capture images
    cams = setup_cameras()
    line = setup_GPIO()
    
    ip = "10.12.23.188"
    test_ip = "10.12.71.113"
    port = 5002
    path = "./captures/"
  
    client_socket = make_client_connection(ip, port)

    # Poll for trigger capture signal
    while True:
        if receive_capture_request(client_socket) != 1:
            sleep(1)
            continue
        else:
            print("Triggered Capture")
            capture(cams, "PiB", path)
            # Process captures
            # Send captures to PiA
            send_images(path, client_socket)
            os.rmdir(path)
    
