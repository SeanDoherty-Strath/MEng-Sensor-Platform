import serial
import pynmea2


class Neo6M:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = serial.Serial(port, baudrate, timeout=timeout)

    def read_raw_data(self):
        """Reads raw NMEA sentence from the GPS module. Returns Raw NMEA sentence as a string or None if no data is available."""
        try:
            raw_data = (
                self.connection.readline().decode("utf-8", errors="ignore").strip()
            )
            return raw_data
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        return None

    def get_location(self):
        """Reads and parses the GPS location from NMEA sentences. Returns Dictionary containing latitude, longitude, altitude, and fix quality or None if no fix."""
        # TODO include timeout incase serial error 
        # TODO return error if no GPS fix?
        while True:
            raw_data = self.read_raw_data()
            if raw_data and raw_data.startswith("$GPGGA"):  # GGA contains location data
                try:
                    msg = pynmea2.parse(raw_data)
                    if msg.latitude and msg.longitude:
                        return {
                            "latitude": msg.latitude,
                            "longitude": msg.longitude,
                            "altitude": msg.altitude,
                            "fix_quality": msg.gps_qual,
                        }
                except pynmea2.ParseError:
                    pass

    def close(self):
        """Closes the serial connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()


if __name__ == "__main__":
    gps = Neo6M(port="/dev/ttyAMA0")

    location = gps.get_location()
    if location:
        print(
            f"Latitude: {location['latitude']}, Longitude: {location['longitude']}, Altitude: {location['altitude']}m, Fix Quality: {location['fix_quality']}"
        )
    else:
        print("No GPS fix.")

    gps.close()
