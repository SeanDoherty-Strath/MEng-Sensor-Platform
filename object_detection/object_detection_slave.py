from ultralytics import YOLO

import RPi.GPIO as GPIO

from picamera2 import Picamera2
from libcamera import controls
import cv2
from time import time
import multiprocessing
import json
import math

def setup_GPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(TRIGGER_PIN, GPIO.RISING, callback=capture)


def setup_cameras():
    """Setup and start both cameras"""
    camA = Picamera2(0)
    camB = Picamera2(1)

    # Set image size
    # config = camA.create_still_configuration({"size":()})
    # camA.align_configuration(config)
    # camB.align_configuration(config)
    # camA.configure(config)
    # camB.configure(config)

    # Setup focus
    camA.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    camB.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    # Start cameras
    camA.start()
    camB.start()

    return (camA, camB)


def capture(cams, save_dir=None):
    """Triggers capture on the cameras {cams}. If {save_dir} specified, the images will be saved to {save_dir} as (timestamp)_#.jpg, otherwise the frames will be returned as a tuple."""
    # TODO: Take multiple image captures and choose best to ensure non-blurry images used
    frames = []

    save_dir="./captures/"

    for i in range(len(cams)):
        if save_dir != None:
            cams[i].capture_file(save_dir + "/" + int(time()) + i)
        else:
            frames[i] = cams[i].capture_array("main")

    return frames


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
    setup_GPIO()
    # capture(cams, "./captures/")
    while True:
        pass

    exit()

    # Setup object detection model
    model = YOLO("yolo_models/yolo11n.pt")

    # Grab test images
    img1 = cv2.imread("A_image1.jpg")
    img2 = cv2.imread("A_image2.jpg")

    # # Run sequentially
    start_time = time()
    results = object_detection(model, img1)
    # _ = object_detection(model, img2)
    print("###################################################################")
    print(f"Time taken to process two images sequentially {time()-start_time}s")
    print("###################################################################")

    print(type(results[0]))

    # for r in results:
    #     r.save_txt("output.txt", True)
    #     r.save_crop("./")

    # json_result = results[0].to_json()
    # print(json_result)

    # Export results to json
    data = []
    for b in results[0].boxes:
        data.append(
            {
                "coords": list(map(int, b.xywh[0].tolist())),
                "RGB Classification": [
                    model.names[int(b.cls[0])],
                    math.ceil((b.conf[0] * 100)) / 100,
                ],
            }
        )

    with open("results.json", mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    # Run with multiprocessing
    # p1 = multiprocessing.Process(
    #     target=object_detection,
    #     args=(model, img1,),
    # )
    # p2 = multiprocessing.Process(
    #     target=object_detection,
    #     args=(model, img2,),
    # )

    # start_time = time()
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # print("###################################################################")
    # print(f"Time taken to process two images concurrently {time()-start_time}s")
    # print("###################################################################")
