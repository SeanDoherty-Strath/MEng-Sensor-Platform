from ultralytics import YOLO
import gpiod
from picamera2 import Picamera2
from libcamera import controls
import cv2
from time import time
import os
from cameras import *
                                                        

def setup_GPIO():
    chip = gpiod.Chip('gpiochip4')
    trigger_line = chip.get_line(TRIGGER_PIN)
    trigger_line.request(consumer="Trigger", type=gpiod.LINE_REQ_DIR_OUT)

    return trigger_line


# def setup_cameras():
#     """Setup and start both cameras"""
#     camA = Picamera2(0)
#     camB = Picamera2(1)

#     # Set image size
#     config = camA.create_still_configuration({"size":(4608,2592),"format":"RGB888"})
#     camA.align_configuration(config)
#     camB.align_configuration(config)
#     camA.configure(config)
#     camB.configure(config)

#     # Setup focus
#     camA.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#     camB.set_controls({"AfMode": controls.AfModeEnum.Continuous})

#     # Start cameras
#     camA.start()
#     camB.start()

#     return (camA, camB)


# def capture(cams, pi_type, save_dir=None):
#     """Triggers capture on the cameras {cams}. If {save_dir} specified, the images will be saved to {save_dir} as (timestamp)_#.jpg, otherwise the frames will be returned as a tuple."""
#     # TODO: Take multiple image captures and choose best to ensure non-blurry images used
#     frames = []

#     for i in range(len(cams)):
#         frames.append(cams[i].capture_array("main"))
#         if save_dir != None:
#             os.makedirs(f"./{save_dir}", exist_ok=True)
#             # cv2.imwrite(save_dir + "/" + str(int(time()))+"_" + str(i)+".jpg",frames[i])
#             cv2.imwrite(f"{save_dir}/{pi_type}_{i}.jpg", frames[i])

#     return frames


def object_detection(model, frame):
    results = model.predict(frame)
    # format results
    return results


def to_json(result):
    """Takes ultralytics result and returns json format"""
    pass


TRIGGER_PIN=26

if __name__ == "__main__":
    # Setup cameras and capture images
    cams = setup_cameras()

    line = setup_GPIO()

    # Trigger
    line.set_value(1)

    capture(cams, "./captures/")

    line.set_value(0)

  