from django.core.management.base import BaseCommand, CommandError
from stalku.core.management.commands._lectures import crawl_institutes, \
    crawl_lectures_grad, crawl_lecture_grad
from stalku.core.models import Lecture, LectureInstance, Institute


class Command(BaseCommand):
    help = 'Crawls DAC website'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int,
                            help='Year to get lectures from.')
        parser.add_argument('semester', type=int,
                            help='Semester to get lectures from.')
        parser.add_argument('degree_level', nargs='?', default='grad',
                            type=str, choices=[code for code, _ in Lecture.DEGREE_LEVELS],
                            help='Specify the degree level to get information from.')

    def handle(self, *args, **options):

        institutes = crawl_institutes(**options)
        self.stdout.write('Institutes for \'{}\' ({}):'.format(
            options['degree_level'],
            len(institutes))
        )

        for institute in institutes:
            self.stdout.write('\t- {}'.format(institute['name']))
            Institute.objects.update_or_create(**institute)

        for institute in Institute.objects.all():

            # Getting lectures
            code, name = institute.code, institute.name
            lectures = crawl_lectures_grad(code, **options)
            self.stdout.write('Getting lectures for {}: {} found. '.format(name, len(lectures)))

            existing_lecs = [x['code'] for x in Lecture.objects.values('code')]
            for l in [lec for lec in lectures if lec.replace('_', ' ') not in existing_lecs]:
                try:
                    lecture_args = crawl_lecture_grad(l, **options)
                    lecture_args['institute'] = institute
                    groups = lecture_args.pop('groups', [])
                    obj = Lecture.objects.create(**lecture_args)

                    for g in groups:
                        LectureInstance.objects.create(
                            lecture=obj, group=g,
                            year=options['year'],
                            semester=options['semester']
                        )
                except Exception as e:
                    raise CommandError('Error trying to parse {}: {}'.format(l, e))
