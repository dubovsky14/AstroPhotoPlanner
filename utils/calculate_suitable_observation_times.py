import ephem
import datetime

from common_data_structures import GPSCoordinate


def calculate_suitable_observation_times(observer_coordinates: GPSCoordinate, date : datetime.date, object_ra : float, object_dec : float, min_angle_above_horizon : float) -> tuple[datetime.datetime, datetime.datetime]:
    observer = ephem.Observer()
    observer.lat = str(observer_coordinates.lat)
    observer.lon = str(observer_coordinates.lon)
    observer.date = date

    observer.horizon = f'{min_angle_above_horizon}'

    celestial_object = ephem.FixedBody()
    celestial_object._ra = str(object_ra)
    celestial_object._dec = str(object_dec)

    try:
        morning_time = observer.next_rising(celestial_object, use_center=True).datetime()
        evening_time = observer.next_setting(celestial_object, use_center=True).datetime()
    except (ephem.NeverUpError):
        day_start = datetime.datetime.combine(date, datetime.time(0, 0), tzinfo=datetime.timezone.utc)
        return day_start, day_start
    except (ephem.AlwaysUpError):
        day_start = datetime.datetime.combine(date, datetime.time(0, 0), tzinfo=datetime.timezone.utc)
        day_end = datetime.datetime.combine(date, datetime.time(23, 59, 59), tzinfo=datetime.timezone.utc)
        return day_start, day_end

    # Adjust to local time
    morning_time = morning_time.replace(tzinfo=datetime.timezone.utc).astimezone()
    evening_time = evening_time.replace(tzinfo=datetime.timezone.utc).astimezone()

    return morning_time, evening_time


if __name__ == "__main__":
    # Example usage
    coordinates = GPSCoordinate(48.6589773, 17.4512129)
    date = datetime.date.today()
    ra = '5:36:35'     # Example RA in HH:MM:SS
    dec = '-05:23:28'  # Example Dec in DD:MM:SS
    min_angle = 30.0  # Minimum angle above horizon in degrees

    morning, evening = calculate_suitable_observation_times(lat, lon, date, ra, dec, min_angle)

    print("Suitable Observation Times for Object at RA:", ra, "Dec:", dec)
    print("Morning Time:", morning)
    print("Evening Time:", evening)

