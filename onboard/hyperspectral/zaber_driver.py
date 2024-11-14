from zaber_motion import Units
from zaber_motion.ascii import Connection

def get_rotation_speed(nframe,fps,angle):
    """ Returns estimate for rotation speed in degrees per second
    for input fps, angle and number of frames to be taken"""
    return angle/(nframe/fps)

def setup_zaber(port):
    """ Sets up Zaber rotation stage and returns rotation axis
    (Not tested alongside other USB devices)    """

    conn=Connection.open_serial_port(port)
    conn.enable_alerts()
    device=conn.detect_devices()[0]
    axis=device.get_axis(1)

    return conn, axis

# Rotate stage
def rotate_relative(axis, angle, speed):
    """ Rotates axis by {angle} degrees at {speed} degrees per second. Non-blocking"""
    axis.settings.set("maxspeed", speed, Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)
    axis.move_relative(angle, Units.ANGLE_DEGREES,wait_until_idle=False)
