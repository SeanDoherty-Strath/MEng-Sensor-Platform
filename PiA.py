from object_detection.object_detection import *
from comms.receive import *
from datetime import datetime

TRIGGER_PIN=26

if __name__ == "__main__":
    # Setup cameras and GPIO
    cams = setup_cameras()
    line = setup_GPIO()

    capture(cams, "PiA", "./captures/")

    port = 5002
    host = "0.0.0.0" # i.e. listening


    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    save_location = f"./{timestamp}-capture/"
    
    server_socket, conn = make_server_connection(host, port)
    
    # Trigger capture on PiB
    line.set_value(1)

    receive_image(save_location, server_socket, conn)


    # Reset GPIO
    line.set_value(0)