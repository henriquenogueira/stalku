from django.db import models


class Student(models.Model):
    name = models.CharField('nome', max_length=255)
    academic_record = models.CharField('RA', max_length=6, unique=True)
    course = models.CharField('curso', max_length=255, blank=True)
    modality = models.CharField('modalidade', max_length=255, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('academic_record',)
        verbose_name = 'estudante'
        verbose_name_plural = 'estudantes'

    @property
    def full_academic_record(self):
        return self.academic_record.zfill(6)

    def __str__(self):
        return '{} - {}'.format(self.academic_record, self.name)

    full_academic_record.fget.short_description = 'registro acadêmico'


class Institute(models.Model):
    code = models.CharField('código', max_length=255)
    name = models.CharField('nome', max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)


class Lecture(models.Model):
    DEGREE_LEVELS = (
        ('grad', 'Graduação'),
        ('pos', 'Pós-graduação')
    )

    institute = models.ForeignKey('Institute', related_name='lectures')
    degree_level = models.CharField('nível', max_length=255, choices=DEGREE_LEVELS)
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
    students = models.ManyToManyField('Student', help_text='alunos matriculados',
                                      related_name='enrolled_in', blank=True)
    group = models.CharField('turma', max_length=2)
    year = models.IntegerField('ano')
    semester = models.IntegerField('semestre')
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('group',)
        verbose_name = 'turma'
        verbose_name_plural = 'turmas'

    @property
    def number_of_students(self):
        return self.students.count()

    def __str__(self):
        return '{} {} - {}'.format(self.lecture.code, self.group, self.lecture.name)
