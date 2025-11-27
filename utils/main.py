import pandas as pd
from calculate_suitable_observation_times import calculate_suitable_observation_times
from sun_movement import get_sun_dec_and_ra, get_sun_elevation_and_azimuth, get_astronomical_twilight_times
from common_data_structures import GPSCoordinate
import datetime

if __name__ == "__main__":
    # Load Messier and Caldwell catalogues
    messier_catalogue = pd.read_csv('data/astronomical_catalogues/Messier.csv')
    caldwell_catalogue = pd.read_csv('data/astronomical_catalogues/Caldwell.csv')

    # Example observer location and date
    observer_coordinates = GPSCoordinate(48.6589773, 17.4512129)
    observation_date = datetime.date.today()

    astronomical_twilight_start, astronomical_twilight_end = get_astronomical_twilight_times(observer_coordinates.lat, observer_coordinates.lon, observation_date, 18.0)
    print("Astronomical Twilight Start:", astronomical_twilight_start)
    print("Astronomical Twilight End:", astronomical_twilight_end)

    print("Messier Catalogue Suitable Observation Times:")
    for index, row in messier_catalogue.iterrows():
        ra = row['RA']
        dec = row['dec']
        min_angle = 30.0  # Minimum angle above horizon in degrees

        morning, evening = calculate_suitable_observation_times(observer_coordinates, observation_date, ra, dec, min_angle)

        # calculate overlap with astronomical night
        if morning < astronomical_twilight_start:
            morning = astronomical_twilight_start
        if evening > astronomical_twilight_end:
            evening = astronomical_twilight_end

        print(f"Object: {row['name']} (RA: {ra}, Dec: {dec})")
        print("  Morning Time:", morning)
        print("  Evening Time:", evening)

#    print("\nCaldwell Catalogue Suitable Observation Times:")
#    for index, row in caldwell_catalogue.iterrows():
#        ra = row['RA']
#        dec = row['dec']
#        min_angle = 30.0  # Minimum angle above horizon in degrees
#
#        morning, evening = calculate_suitable_observation_times(observer_coordinates, observation_date, ra, dec, min_angle)
#
#        print(f"Object: {row['name']} (RA: {ra}, Dec: {dec})")
#        print("  Morning Time:", morning)
#        print("  Evening Time:", evening)