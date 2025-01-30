from object_detection.object_detection import *
from comms.send import *

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
  
    client_socket = make_client_connection(test_ip, port)

    # Poll for trigger capture signal
    while True:
        val = line.get_value()
        if val == 1 and last == 0:
            capture(cams, "PiB", path)
            # Process captures
            # Send captures to PiA
            send_images(path, client_socket)
            os.rmdir(path)
            last=1
        if val == 0:
            last = 0
    
