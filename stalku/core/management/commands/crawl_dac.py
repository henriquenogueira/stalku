from django.core.management.base import BaseCommand
from stalku.core.management.commands._private import crawl_institutes


class Command(BaseCommand):
    help = 'Crawls DAC website'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int,
                            help='Year to get lectures from.')
        parser.add_argument('semester', type=int,
                            help='Semester to get lectures from.')
        parser.add_argument('degree_level',
                            nargs='?',
                            default='grad',
                            type=str,
                            choices=['grad', 'pos'],
                            help='Specify the degree level to get information from.')

    def handle(self, *args, **options):
        self.stdout.write('Handling Crawl Students command...')
        self.stdout.write('Institutes for \'{}\':'.format(options['degree_level']))
        institutes = crawl_institutes(**options)
        for institute in institutes:
            self.stdout.write('\t- {}'.format(institute))
