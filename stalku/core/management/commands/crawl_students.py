from django.core.management.base import BaseCommand, CommandError
from stalku.core.management.commands._students import get_students_for_lecture_instance
from stalku.core.models import LectureInstance, Student


class Command(BaseCommand):
    help = 'Crawls students from DAC website'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int,
                            help='Year to get lectures from.')
        parser.add_argument('semester', type=int,
                            help='Semester to get lectures from.')
        parser.add_argument('degree_level', nargs='?', default='grad',
                            type=str, choices=['grad', 'pos'],
                            help='Specify the degree level to get information from.')

    def handle(self, *args, **options):
        lecture_instances = LectureInstance.objects.prefetch_related('lecture')
        for l in lecture_instances:
            self.stdout.write('Getting student list for {}'.format(l))
            students = get_students_for_lecture_instance(l, **options)
            for s in students:
                student_obj, updated = Student.objects.get_or_create(**s)
                l.students.add(student_obj)
