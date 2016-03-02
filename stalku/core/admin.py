from django.contrib import admin

from .models import Student, Lecture, LectureInstance

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('academic_record', 'name', 'course', 'modality')
    search_fields = ('academic_record', 'name', 'course', 'modality')


class LectureModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description')
    search_fields = ('code', 'name', 'description')


class LectureInstanceModelAdmin(admin.ModelAdmin):
    list_display = ('lecture_code', 'group', 'lecture_description', 'enrolled_students')
    search_fields = ('lecture__code', 'group', 'lecture__description')

    def lecture_code(self, obj):
        return obj.lecture.code

    def lecture_description(self, obj):
        return obj.lecture.description

    def enrolled_students(self, obj):
        return obj.students.count()

    lecture_code.short_description = 'código da disciplina'
    lecture_description.short_description = 'ementa'
    enrolled_students.short_description = 'inscritos'

admin.site.register(Student, StudentModelAdmin)
admin.site.register(Lecture, LectureModelAdmin)
admin.site.register(LectureInstance, LectureInstanceModelAdmin)
