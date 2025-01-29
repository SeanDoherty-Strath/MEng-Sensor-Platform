from object_detection.object_detection import *

TRIGGER_PIN=26
last = 0

if __name__ == "__main__":
    # Setup cameras and capture images
    cams = setup_cameras()
    line = setup_GPIO()

    # Poll for trigger capture signal
    while True:
        val = line.get_value()
        if val == 1 and last == 0:
            capture(cams, "./captures/")
            # Process captures
            # Send captures to PiA
            last=1
        if val == 0:
            last = 0