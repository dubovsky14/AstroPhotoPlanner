import pandas as pd
from AstroPhotoPlanner.models import Catalogue, DeepSkyObject

def import_catalogue_from_csv(catalogue : Catalogue, csv_file_path : str) -> None:
    df = pd.read_csv(csv_file_path)
    required_columns = {'name', 'ra', 'dec'}
    df.columns = [col.lower() for col in df.columns]

    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV file must contain the following columns: {required_columns}")

    for _, row in df.iterrows():
        object_type = row.get('type')
        if pd.isna(object_type) or type(object_type) != str:
            row['type'] = ""
        if pd.isna(row.get('plan_to_photograph')):
            row['plan_to_photograph'] = True
        else:
            row['plan_to_photograph'] = bool(row['plan_to_photograph'])
        DeepSkyObject.objects.create(
            catalogue=catalogue,
            name=row['name'],
            ra=row['ra'],
            dec=row['dec'],
            magnitude=row.get('magnitude', None),
            object_type=row.get('type', "").strip(),
            plan_to_photograph=row['plan_to_photograph']
        )

def export_catalogue_to_csv(catalogue : Catalogue) -> str:
    deep_sky_objects = catalogue.deep_sky_objects.all()
    result = "name,ra,dec,magnitude,type,plan_to_photograph\n"
    for obj in deep_sky_objects:
        result += f"{obj.name},{obj.ra},{obj.dec},{obj.magnitude if obj.magnitude is not None else ''},{obj.object_type if obj.object_type else ''},{obj.plan_to_photograph}\n"
    return result
