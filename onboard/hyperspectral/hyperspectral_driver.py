import numpy as np
import pypylon.pylon as pylon
from time import time

def setup_hyperspectral():
    """Sets up hyperspectral camera and opens connection"""
    cam=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    cam.Open()

    cam.UserSetSelector = "Default"
    cam.UserSetLoad.Execute()
    return cam

def grab_hyperspectral(cam,nframes):
    """ Grabs {nframes} number of frames from hyperspectral camera"""
    cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

    scene = np.zeros((cam.Width.Value, nframes, cam.Height.Value), dtype=np.uint8)
    i=0

    print("Grabbing frames")
    t0=time()
    while cam.IsGrabbing():
        grab=cam.RetrieveResult(100,pylon.TimeoutHandling_ThrowException)

        if grab.GrabSucceeded():
            scene[:,i,:] = np.transpose(grab.Array)
            i+=1

        if i==nframes:
            break

    print(f"Acquired {nframes} frames in {time()-t0} seconds")

    return scene