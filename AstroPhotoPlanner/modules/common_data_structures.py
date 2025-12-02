

class GPSCoordinate:
    """
    A class to represent a GPS coordinate with latitude and longitude.
    """

    def __init__(self, latitude: float, longitude: float):
        self.lat = latitude
        self.lon = longitude

    def __repr__(self):
        return f"{self.lat}N, {self.lon}E"

    def to_tuple(self):
        return (self.lat, self.lon)