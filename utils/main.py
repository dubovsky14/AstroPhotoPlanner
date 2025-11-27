import pandas as pd
from calculate_suitable_observation_times import calculate_suitable_observation_times, calculate_suitable_observation_during_time_period
from sun_movement import get_sun_dec_and_ra, get_sun_elevation_and_azimuth, get_astronomical_night_start_end_times
from common_data_structures import GPSCoordinate
import datetime

if __name__ == "__main__":
    # Load Messier and Caldwell catalogues
    messier_catalogue = pd.read_csv('data/astronomical_catalogues/Messier.csv')
    caldwell_catalogue = pd.read_csv('data/astronomical_catalogues/Caldwell.csv')

    # Example observer location and date
    observer_coordinates = GPSCoordinate(48.6589773, 17.4512129)
    observation_date = datetime.date.today()

    night_start, night_end = get_astronomical_night_start_end_times(observer_coordinates, observation_date, 18.0)
    print("Astronomical Night Start:", night_start)
    print("Astronomical Night End:", night_end)

    print("Messier Catalogue Suitable Observation Times:")
    for index, row in messier_catalogue.iterrows():
        ra = row['RA']
        dec = row['dec']
        min_angle = 30.0  # Minimum angle above horizon in degrees

        observation_periods = calculate_suitable_observation_during_time_period(observer_coordinates, night_start, night_end, ra, dec, min_angle)

        print(f"Object: {row['name']} (RA: {ra}, Dec: {dec})")
        for morning, evening in observation_periods:
            print(f"  Suitable Observation Time: {morning} to {evening}")
        if not observation_periods:
            print("  No suitable observation times during the night.")
        print()

#    print("\nCaldwell Catalogue Suitable Observation Times:")
#    for index, row in caldwell_catalogue.iterrows():
#        ra = row['RA']
#        dec = row['dec']
#        min_angle = 30.0  # Minimum angle above horizon in degrees
#
#        morning, evening = calculate_suitable_observation_during_time_period(observer_coordinates, observation_date, ra, dec, min_angle)
#
#        print(f"Object: {row['name']} (RA: {ra}, Dec: {dec})")
#        print("  Morning Time:", morning)
#        print("  Evening Time:", evening)