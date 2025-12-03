import ephem
import datetime

from .common_data_structures import GPSCoordinate


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

def calculate_suitable_observation_during_time_period(observer_coordinates: GPSCoordinate, night_start : datetime.datetime, night_end : datetime.datetime, object_ra : float, object_dec : float, min_angle_above_horizon : float) -> list[tuple[datetime.datetime, datetime.datetime]]:
    observer = ephem.Observer()
    observer.lat = str(observer_coordinates.lat)
    observer.lon = str(observer_coordinates.lon)
    observer.date = night_start

    observer.horizon = f'{min_angle_above_horizon}'

    celestial_object = ephem.FixedBody()
    celestial_object._ra = str(object_ra)
    celestial_object._dec = str(object_dec)

    celestial_object.compute(observer)

    above_horizon_at_start = celestial_object.alt*(180.0 / ephem.pi) > min_angle_above_horizon

    try:
        if above_horizon_at_start:
            object_set_time = observer.next_setting(celestial_object, use_center=True).datetime().replace(tzinfo=datetime.timezone.utc).astimezone()
            if object_set_time > night_end:
                object_set_time = night_end
            object_rise_time = night_start
            return [(object_rise_time, object_set_time)]
        else:
            object_rise_time = observer.next_rising(celestial_object, use_center=True).datetime().replace(tzinfo=datetime.timezone.utc).astimezone()
            if object_rise_time < night_start:
                object_rise_time = night_start
            observer.date = object_rise_time
            object_set_time = observer.next_setting(celestial_object, use_center=True).datetime().replace(tzinfo=datetime.timezone.utc).astimezone()
            if object_set_time > night_end:
                object_set_time = night_end
            if object_rise_time >= night_end:
                return []
            return [(object_rise_time, object_set_time)]
    except (ephem.NeverUpError):
        return []
    except (ephem.AlwaysUpError):
        return [(night_start, night_end)]

def object_available_from_location(gps_lat : float, object_dec : float, min_angle_above_horizon : float) -> bool:
    object_max_height = 90.0 - abs(gps_lat - object_dec)
    if object_max_height < min_angle_above_horizon:
        return False
    return True


if __name__ == "__main__":
    # Example usage
    observer_coordinates = GPSCoordinate(48.6589773, 17.4512129)
    date_time = datetime.datetime.now()
    ra = '5:36:35'     # Example RA in HH:MM:SS
    dec = '-05:23:28'  # Example Dec in DD:MM:SS
    min_angle = 30.0  # Minimum angle above horizon in degrees

    from sun_movement import get_astronomical_night_start_end_times
    date = date_time.date()
    night_start, night_end = get_astronomical_night_start_end_times(observer_coordinates, date, 18)

    print("Calculating Suitable Observation Times for Lat:", observer_coordinates.lat, "Lon:", observer_coordinates.lon, "Date:", date)
    print("Astronomical Night Start:", night_start, "Astronomical Night End:", night_end)

    suitable_times = calculate_suitable_observation_during_time_period(observer_coordinates, night_start, night_end, ra, dec, min_angle)

    for morning, evening in suitable_times:
        print("Suitable Observation Time:", morning, "to", evening)
    if not suitable_times:
        print("No suitable observation times during the night.")
