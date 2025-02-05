from object_detection.object_detection import *
from comms.receive import *
from datetime import datetime
from time import sleep

TRIGGER_PIN=26

if __name__ == "__main__":
    # Setup cameras and GPIO
    cams = setup_cameras()

    port = 5002
    host = "0.0.0.0" # i.e. listening

    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    save_location = f"./{timestamp}-capture/"
    
    server_socket, conn = make_server_connection(host, port)
    
    # Trigger capture on PiB

    capture(cams, "PiA", save_location)
    request_client_capture(server_socket, conn)
    receive_images(save_location, server_socket, conn)
    sleep(1)