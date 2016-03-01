from datetime import datetime

from django.test import TestCase
from stalku.core.models import Student


class CoreModelTest(TestCase):
    def setUp(self):
        self.obj = Student(
            name='Henrique Gaspar Nogueira',
            academic_record='073203'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Student.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_name_str(self):
        self.assertEqual('Henrique Gaspar Nogueira', self.obj.name)
