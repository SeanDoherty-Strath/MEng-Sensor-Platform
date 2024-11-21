import os
import numpy as np
import pypylon.pylon as pylon
from time import time
import matplotlib.pyplot as plt


def setup_hyperspectral():
    """Sets up hyperspectral camera and opens connection"""
    cam = pylon.InstantCamera(
        pylon.TlFactory.GetInstance().CreateFirstDevice()
    )
    cam.Open()

    cam.UserSetSelector = "Default"
    cam.UserSetLoad.Execute()

    cam.BinningVertical = 2
    cam.BinningHorizontal = 2

    return cam


def grab_hyperspectral_scene(cam, nframes):
    """Grabs {nframes} number of frames from hyperspectral camera"""
    cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

    scene = np.zeros(
        (cam.Width.Value, nframes, cam.Height.Value), dtype=np.uint8
    )
    i = 0

    print("Grabbing frames")
    t0 = time()
    while cam.IsGrabbing():
        grab = cam.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

        if grab.GrabSucceeded():
            scene[:, i, :] = np.transpose(grab.Array)
            i += 1

        if i == nframes:
            break

    print(f"Acquired {nframes} frames in {time()-t0} seconds")

    return scene


def grab_hyperspectral_frame(cam):
    """Grabs single frames from hyperspectral camera"""

    print("Grabbing frame")
    grab = cam.GrabOne(10000)

    return grab.Array

def get_calibration_array(path):
    """ Gets calibration file at {path} and returns as numpy array"""""
    return np.loadtxt(path)

def get_wavelength_index(cal_array, wavelength, pixel_binning):
    """ Returns closest index of {wavelength} from {cal_array} while accounting for pixel binning """

    if wavelength < cal_array[0]:
        print("Wavelength out of range: Too small.")
        return 0
    elif wavelength > cal_array[-1]:
        print("Wavelength out of range: Too large.")
        return len(cal_array)

    for i in range(0, len(cal_array)):
        diff=wavelength-cal_array[i]
        if diff <= 0:
            break

    return int(i/pixel_binning)


def calibrate_hyperspectral(X, W, D):
    """
    Calibrates a hyperspectral image using white and dark reference images.

    - X: Uncalibrated hyperspectral image
    - W: White reference image.
    - D: Dark reference image.

    """

    I = (X - D) / (W - D)

    return I


def get_white_image(cam):
    """
    Captures the white reference image.

    - cam: Camera object

    """
    print("Capturing white reference image...")
    white_image = grab_hyperspectral_frame(cam)
    return white_image


def get_dark_image(cam, dark_image_path="dark_image.npy"):
    """
    Loads or captures the dark reference image.

    - cam: Camera object.
    - dark_image_path: File path to save/load the dark image.

    """

    if os.path.exists(dark_image_path):
        dark_image = np.load(dark_image_path)
    else:
        print("Capturing new dark image...")
        dark_image = grab_hyperspectral_frame(cam)
        np.save(dark_image_path, dark_image)
        print(f"Dark image saved as {dark_image_path}")

    return dark_image
