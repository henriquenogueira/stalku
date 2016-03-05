from django.test import TestCase
from stalku.core.management.commands._lectures import crawl_institutes, crawl_lectures_grad, crawl_lecture_grad
from stalku.core.management.commands._students import get_students_for_lecture_instance
from stalku.core.models import Lecture, Institute, LectureInstance


class LectureCrawlerTest(TestCase):
    def test_institutes(self):
        expected = {'grad': 26, 'pos': 23}
        with self.subTest():
            for degree_level, exp in expected.items():
                institutes = crawl_institutes(degree_level=degree_level, semester=1)
                self.assertEqual(exp, len(institutes))
                self.assertEqual(len(institutes), len(set([i['code'] for i in institutes])))

    def test_lectures(self):
        expected = {'IA': 425}
        for institute, exp in expected.items():
            lectures = crawl_lectures_grad(institute, semester=1)
            self.assertEqual(exp, len(lectures))
            self.assertEqual(len(lectures), len(set(lectures)))

    def test_lecture(self):
        expected = (
            ('F_037', 'Astrofísica', 1),
            ('MC102', 'Algoritmos', 26),
            ('CV916', 'Método', 1),
            ('EF315', 'Luta', 2)
        )

        with self.subTest():
            for code, name, groups in expected:
                result = crawl_lecture_grad(code, semester=1, degree_level='grad')
                self.assertIn(name, result['name'])
                self.assertEqual(len(result['groups']), groups)


class StudentsCrawlerTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            code='IC',
            name='Instituto de computação'
        )

        lecture = Lecture.objects.create(
            institute=institute,
            code='MC102',
            name='Algoritmos',
            description='Algoritmos',
            degree_level='grad'
        )

        self.lecture_instance = LectureInstance.objects.create(
            lecture=lecture,
            year=2016,
            semester=1,
            group='A'
        )

    def test_get_students(self):
        s = get_students_for_lecture_instance(self.lecture_instance, semester=1, year=2016)
        self.assertEqual(25, len(s))
        self.assertIn({'course': '8', 'academic_record': '146143', 'name': 'Gabriel Lopes Nenov', 'modality': 'G'}, s)
