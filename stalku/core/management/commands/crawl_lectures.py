from django.core.management.base import BaseCommand, CommandError
from stalku.core.management.commands._lectures import crawl_institutes, \
    crawl_lectures_grad, crawl_lecture_grad
from stalku.core.models import Lecture, LectureInstance


class Command(BaseCommand):
    help = 'Crawls DAC website'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int,
                            help='Year to get lectures from.')
        parser.add_argument('semester', type=int,
                            help='Semester to get lectures from.')
        parser.add_argument('degree_level', nargs='?', default='grad',
                            type=str, choices=['grad', 'pos'],
                            help='Specify the degree level to get information from.')

    def handle(self, *args, **options):
        institutes = crawl_institutes(**options)
        self.stdout.write('Institutes for \'{}\' ({}):'.format(options['degree_level'], len(institutes)))
        for institute in institutes:
            self.stdout.write('\t- {}'.format(institute))

        for institute in institutes:
            self.stdout.write('Getting lectures for {}. '.format(institute))
            lectures = crawl_lectures_grad(institute, **options)
            self.stdout.write('\t{} found: {}, {}, {}, ..., {}'.format(
                len(lectures), *lectures[:3], lectures[-1]))

            for idx, l in enumerate(lectures):
                try:
                    lecture = crawl_lecture_grad(l, **options)
                    groups = lecture.pop('groups', [])
                    obj, created = Lecture.objects.update_or_create(**lecture)

                    for g in groups:
                        LectureInstance.objects.get_or_create(lecture=obj, group=g,
                                                              year=options['year'], semester=options['semester'])
                except Exception as e:
                    raise CommandError('Error trying to parse {}: {}'.format(l, e))


