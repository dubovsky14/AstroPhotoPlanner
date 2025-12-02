import pandas as pd
from AstroPhotoPlanner.models import Catalogue, DeepSkyObject

def import_catalogue_from_csv(catalogue, csv_file_path):
    df = pd.read_csv(csv_file_path)
    required_columns = {'name', 'ra', 'dec'}
    df.columns = [col.lower() for col in df.columns]

    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV file must contain the following columns: {required_columns}")

    for _, row in df.iterrows():
        DeepSkyObject.objects.create(
            catalogue=catalogue,
            name=row['name'],
            ra=row['ra'],
            dec=row['dec'],
            magnitude=row.get('magnitude', None),
            object_type=row.get('object_type', ""),
        )
