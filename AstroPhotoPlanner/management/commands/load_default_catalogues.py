from AstroPhotoPlanner.modules.import_from_csv import import_catalogue_from_csv

from django.core.management.base import BaseCommand
from AstroPhotoPlanner.models import Catalogue, UserProfile

from sys import argv
import os

class Command(BaseCommand):
    help = "Loads a catalogue from a CSV file"

    def add_arguments(self, parser):
        # Required positional argument
        parser.add_argument("filepath", type=str, help="Path to the CSV file")
        parser.add_argument("--catalogue_name", type=str, default="")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        catalogue_name = options["catalogue_name"]

        self.stdout.write(f"Loading catalogue from {filepath}...")
        self.stdout.write(f"Catalogue name: {catalogue_name if catalogue_name else 'Not provided, will use filename'}")

        filename = os.path.basename(filepath)
        if not catalogue_name:
            catalogue_name, _ = os.path.splitext(filename)

        catalogue = Catalogue(name=catalogue_name, owner=None)
        catalogue.save()

        import_catalogue_from_csv(catalogue, filepath)

        self.stdout.write(self.style.SUCCESS("Catalogue loaded successfully"))