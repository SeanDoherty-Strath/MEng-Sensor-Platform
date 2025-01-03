from ultralytics import YOLO
import cv2
import math
import time

def bounding_box(img,box,labels):
    # bounding box
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

    # put box on image
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

    # confidence
    confidence = math.ceil((box.conf[0] * 100)) / 100
    # print("Confidence --->", confidence)

    # class name
    cls = int(box.cls[0])
    # print("Class name -->", labels[cls])

    # object details
    org = [x1, y1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2

    cv2.putText(img, f"{labels[cls]} -- {confidence}", org, font, fontScale, color, thickness)
    return img

def rgb_capture():
    model = YOLO("yolo_models/yolo11n.pt")
    count = 0
    start = time.time()

    if CAPTURE_METHOD == "IMAGE":
        img = cv2.imread("dog.jpg")

        results = model.predict(img)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                img = bounding_box(img, box, model.names)

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if CAPTURE_METHOD == "WEBCAM":
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            results = model.predict(frame, stream=True)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    frame = bounding_box(frame, box, model.names)

            # Calculate FPS
            if count % FPS_AVERAGE_NUM_FRAMES == 0:
                end = time.time()
                fps = FPS_AVERAGE_NUM_FRAMES / (end - start)
                start = time.time()

            # Show the FPS
            fps_text = f"{fps:.2f} FPS"
            cv2.putText(frame, fps_text, [20, 20], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            count += 1

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    elif CAPTURE_METHOD == "PICAM":
        # Import picamera libraries
        from picamera2 import Picamera2
        from libcamera import controls

        picam = Picamera2()
        picam.start()
        picam.set_controls({"AfMode": controls.AfModeEnum.Continuous})

        while True:

            frame = picam.capture_array()

            results = model.predict(frame, stream=True)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    frame = bounding_box(frame, box, model.names)

            # Calculate FPS
            if count % FPS_AVERAGE_NUM_FRAMES == 0:
                end = time.time()
                fps = FPS_AVERAGE_NUM_FRAMES / (end - start)
                start = time.time()

            # Show the FPS
            fps_text = f"{fps:.2f} FPS"
            cv2.putText(frame, fps_text, [20, 20], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            count += 1

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


CAPTURE_METHOD = "WEBCAM" # or "PICAM", "WEBCAM" or "IMAGE"
FPS_AVERAGE_NUM_FRAMES = 20

if __name__ == '__main__':
    rgb_capture()
