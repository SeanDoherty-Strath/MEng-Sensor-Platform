from ultralytics import YOLO

import gpiod
from picamera2 import Picamera2
from libcamera import controls
import cv2
from time import time
import multiprocessing
import json
import math

def setup_GPIO():
    chip = gpiod.Chip('gpiochip4')
    trigger_line = chip.get_line(TRIGGER_PIN)
    trigger_line.request(consumer="Trigger", type=gpiod.LINE_REQ_DIR_IN)

    return trigger_line

def setup_cameras():
    """Setup and start both cameras"""
    camA = Picamera2(0)
    camB = Picamera2(1)

    # Set image size
    config = camA.create_still_configuration({"size":(4608,2592),"format":"RGB888"})
    camA.align_configuration(config)
    camB.align_configuration(config)
    camA.configure(config)
    camB.configure(config)

    # Setup focus
    camA.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    camB.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    # Start cameras
    camA.start()
    camB.start()

    return (camA, camB)


def capture(cams, save_dir=None):
    print("CAPTURE")
    """Triggers capture on the cameras {cams}. If {save_dir} specified, the images will be saved to {save_dir} as (timestamp)_#.jpg, otherwise the frames will be returned as a tuple."""
    # TODO: Take multiple image captures and choose best to ensure non-blurry images used
    frames = []

    save_dir="./captures/"

    for i in range(len(cams)):
        frames.append(cams[i].capture_array("main"))
        if save_dir != None:
            cv2.imwrite(save_dir + "/" + str(int(time())) + "_"+str(i)+".jpg",frames[i])

    return frames


def object_detection(model, frame):

    results = model.predict(frame)
    # format results
    return results


def to_json(result):
    """Takes ultralytics result and returns json format"""
    pass

TRIGGER_PIN=26
last = 0
if __name__ == "__main__":
    # Setup cameras and capture images
    cams = setup_cameras()
    line = setup_GPIO()
    # capture(cams, "./captures/")
    while True:
        val = line.get_value()
        if val == 1 and last == 0:
            capture(cams, "./captures/")
            last=1
        if val == 0:
            last = 0

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
