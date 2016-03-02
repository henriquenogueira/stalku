from django.db import models

class Student(models.Model):

    name = models.CharField('nome', max_length=255)
    academic_record = models.CharField('RA', max_length=6, unique=True)
    course = models.CharField(max_length=3, blank=True)
    modality = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('academic_record', )
        verbose_name = 'estudante'
        verbose_name_plural = 'estudantes'

    def __str__(self):
        return '{} - {}'.format(self.academic_record, self.name)


class Lecture(models.Model):
    code = models.CharField('código', max_length=7, unique=True)
    name = models.CharField('nome', max_length=255)
    description = models.TextField('ementa', blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('code',)
        verbose_name = 'disciplina'
        verbose_name_plural = 'disciplinas'

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)


class LectureInstance(models.Model):
    lecture = models.ForeignKey('Lecture', help_text='disciplina', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', help_text='alunos matriculados', blank=True)
    group = models.CharField('turma', max_length=2)

    class Meta:
        ordering = ('group',)
        verbose_name = 'turma'
        verbose_name_plural = 'turmas'

    @property
    def number_of_students(self):
        return self.students.count()

    def __str__(self):
        return '{} {} - {}'.format(self.lecture.code, self.group, self.lecture.name)
