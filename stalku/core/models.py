from django.db import models

class Student(models.Model):

    name = models.CharField('nome', max_length=255)
    academic_record = models.CharField('RA', max_length=6, unique=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('academic_record', )
        verbose_name = 'estudante'
        verbose_name_plural = 'estudantes'

    def __str__(self):
        return '{} - {}'.format(self.academic_record, self.name)
