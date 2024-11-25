from hyperspectral.zaber_driver import *
from hyperspectral.hyperspectral_driver import *
import matplotlib.pyplot as plt
import os

CALIBRATION_FILE_PATH = "hyperspectral/BaslerPIA1600_CalibrationA.txt"
PORT = "COM5"  # CHANGE PER USER
NFRAMES = 50
ANGLE = 10

if "__main__" == __name__:
    try:
        # Get Calibration
        calibration_array = get_calibration_array(CALIBRATION_FILE_PATH)
        # print(get_wavelength_index(calibration_array,450,1))

        # Setup hyperspectral
        cam = setup_hyperspectral()
        cam.ExposureTimeAbs.Value = cam.ExposureTimeAbs.Max  # Set to max exposure time
        cam.GainRaw.SetValue(500)  # Set gain to max value
        fps = cam.ResultingFrameRateAbs.Value

        print("Setup Hyperspectral Camera")
        # Get required rotation speed
        speed = get_rotation_speed(NFRAMES, fps, ANGLE)
        print(f"Speed: {speed} degree/s")

        # Setup rotational stage
        zaber_conn, axis = setup_zaber(PORT)

        print("Setup rotation stage")

        # Grab full scene
        rotate_relative(axis, ANGLE, speed)

        scene = grab_hyperspectral_scene(cam, NFRAMES)
        print("Plotting RGB Image...")
        plt.imshow(
            scene[:, :, (int(504 / 2), int(400 / 2), int(260 / 2))],
            aspect="auto",
        )

        # Grab single hyperspectral frame
        # grab = grab_hyperspectral_frame(cam)
        # print("Grabbed image")
        # plt.imshow(grab)

        rotate_relative(axis, -ANGLE, 40)

        # Close Connections
        zaber_conn.close()
        cam.Close()

        plt.show()

    except Exception as e:
        print(e)
        cam.Close()
        zaber_conn.close()
        print("ALL CONNECTIONS CLOSED")
