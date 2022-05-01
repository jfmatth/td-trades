from django.core.management.base import BaseCommand
from os.path import exists

from transactions.models import ingestfile

class Command(BaseCommand):
    help = "ingests a file into the system"

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):

        filename = options['filename'][0]

        print(f"Ingesting file {filename}")

        if not exists(filename):
            print(f'File {filename} does not exist, sorry')
            
            return

        ingestfile(filename)
