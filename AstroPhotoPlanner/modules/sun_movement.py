
import datetime
import ephem

from .common_data_structures import GPSCoordinate

def get_sun_dec_and_ra(observation_time : datetime.datetime) -> tuple[float, float]:
    utc_time = observation_time.astimezone(datetime.timezone.utc)
    sun = ephem.Sun(utc_time)

    sun_ra = sun.ra * (12 / ephem.pi)  # Convert from radians to hours
    sun_dec = sun.dec * (180.0 / ephem.pi)  # Convert from radians to degrees

    return sun_dec, sun_ra

def get_sun_elevation_and_azimuth(observer_coordinates: GPSCoordinate, observation_time : datetime.datetime) -> tuple[float, float]:
    observer = ephem.Observer()
    observer.lat = str(observer_coordinates.lat)
    observer.lon = str(observer_coordinates.lon)

    # Convert observation_time to UTC
    utc_time = observation_time.astimezone(datetime.timezone.utc)

    observer.date = utc_time

    sun = ephem.Sun(observer)

    sun.compute(observer)

    sun_elevation = sun.alt * (180.0 / ephem.pi)  # Convert from radians to degrees
    sun_azimuth = sun.az * (180.0 / ephem.pi)  # Convert from radians to degrees

    return sun_elevation, sun_azimuth

def get_astronomical_night_start_end_times(observer_coordinates: GPSCoordinate, date : datetime.date, angle_below_horizon : float) -> tuple[datetime.datetime, datetime.datetime]:
    observer = ephem.Observer()
    observer.lat = str(observer_coordinates.lat)
    observer.lon = str(observer_coordinates.lon)
    observer.date = date

    sun = ephem.Sun()

    observer.horizon = f'-{angle_below_horizon}'  # Astronomical twilight

    night_start = observer.next_setting(sun, use_center=True).datetime()

    # calculate dawn for tomorrow
    observer.date += 1  # Move to the next day
    night_end = observer.next_rising(sun, use_center=True).datetime()

    # Adjust night_end and night_start to local time
    night_end = night_end.replace(tzinfo=datetime.timezone.utc).astimezone()
    night_start = night_start.replace(tzinfo=datetime.timezone.utc).astimezone()

    return night_start, night_end


if __name__ == "__main__":
    # Example usage
    observer_coordinates = GPSCoordinate(48.6589773, 17.4512129)
    obs_time = datetime.datetime.now()

    print("Calculating Sun Position and Twilight Times for Lat:", observer_coordinates.lat, "Lon:", observer_coordinates.lon, "Time:", obs_time)

    sun_dec, sun_ra = get_sun_dec_and_ra(obs_time)
    print(f"Sun Dec: {sun_dec}, Sun RA: {sun_ra}")

    sun_elev, sun_azim = get_sun_elevation_and_azimuth(observer_coordinates, obs_time)
    print(f"Sun Elevation: {sun_elev}, Sun Azimuth: {sun_azim}")

    night_start, night_end = get_astronomical_night_start_end_times(observer_coordinates, obs_time.date(), 18)
    print(f"Astronomical Night Start: {night_start}, Astronomical Night End: {night_end}")