from datetime import datetime

from django.test import TestCase
from stalku.core.models import Student, Lecture, Institute


class StudentModelTest(TestCase):
    def setUp(self):
        self.obj = Student(
            name='Henrique Gaspar Nogueira',
            academic_record='73203'
        )
        self.obj.save()

    def test_create(self):
        """Make sure the student can be saved on the DB"""
        self.assertTrue(Student.objects.exists())

    def test_created_at(self):
        """Test created_at attribute type"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_name_str(self):
        """Checking student name"""
        self.assertEqual('Henrique Gaspar Nogueira', self.obj.name)

    def test_full_academic_record(self):
        """Test length of the academic record"""
        self.assertEqual('073203', self.obj.full_academic_record)


class LectureModelTest(TestCase):
    def setUp(self):

        institute = Institute.objects.create(
            code='IC',
            name='Instituto de Computação'
        )

        self.obj = Lecture(
            institute=institute,
            degree_level='grad',
            code='MC102',
            name='Algoritmos e programação de computadores',
            description='Texto muito longo.'
        )
        self.obj.save()

    def test_create(self):
        """Make sure the lecture can be saved on the DB"""
        self.assertTrue(Lecture.objects.exists())

    def test_created_at(self):
        """Test created_at attribute type"""
        self.assertIsInstance(self.obj.created_at, datetime)
