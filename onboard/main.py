from hyperspectral.zaber_driver import *
from hyperspectral.hyperspectral_driver import *
import matplotlib.pyplot as plt

PORT="COM5"
NFRAMES=200
ANGLE=60

if "__main__" == __name__:
    # Setup hyperspectral
    cam = setup_hyperspectral()
    cam.ExposureTimeAbs.Value = cam.ExposureTimeAbs.Max # Set to max exposure time
    cam.GainRaw.SetValue(500) # Set gain to max value
    fps = cam.ResultingFrameRateAbs.Value

    # Get required rotation speed
    speed = get_rotation_speed(NFRAMES,fps,ANGLE)

    # Setup rotational stage
    zaber_conn, axis = setup_zaber(PORT)

    # Grab image
    rotate_relative(axis,ANGLE,speed)
    scene = grab_hyperspectral(cam,NFRAMES)
    axis.wait_until_idle() # needed?

    # Show RGB from hyperspectral image
    plt.imshow(scene[:, :, (511, 410, 260)], aspect="auto")

    # Close Connections
    zaber_conn.close()
    cam.Close()