import json
from django.core.management.base import BaseCommand, CommandError
from forex_python.converter import RatesNotAvailableError
from rates.main import RatesValidationException, converter

class Command(BaseCommand):
    help = 'Converts amount to different currencies. '

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=float,
            required=True,
            help='Source amount',
        )

        parser.add_argument(
            '--input_currency',
            type=str,
            required=True,
            help='Source currency',
        )

        parser.add_argument(
            '--output_currency',
            type=str,
            required=False,
            help='Output currency',
        )


    def handle(self, *args, **options):
        try:
            ret = converter(options['amount'], options['input_currency'], options['output_currency'])
            self.stdout.write(json.dumps(ret))
        except RatesValidationException as e:
            self.stdout.write("Inpurt validation error: {}".format(e))
        except RatesNotAvailableError:
            self.stdout.write("Problem with api connection, please try later")