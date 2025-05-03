from django.core.management.base import BaseCommand

from experiments.models import DEFAULT_BULK_SIZE, ExperimentBase


class Command(BaseCommand):
    help = "Generate rows. Example: python manage.py generate_rows --bulk-size 100000"

    def add_arguments(self, parser):
        parser.add_argument("--bulk-size", type=int, default=DEFAULT_BULK_SIZE)

    def handle(self, *args, **options):
        bulk_size = options.get("bulk_size")
        for experiment_table in ExperimentBase.submodels_by_size().values():
            experiment_table.bulk_generate_rows(bulk_size=bulk_size)
