from object_detection.object_detection import *

TRIGGER_PIN=26

if __name__ == "__main__":
    # Setup cameras and GPIO
    cams = setup_cameras()
    line = setup_GPIO()

    # Trigger capture on PiB
    line.set_value(1)

    capture(cams, "./captures/")

    # Reset GPIO
    line.set_value(0)