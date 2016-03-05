from django.contrib import admin

from .models import Student, Lecture, LectureInstance, Institute


class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('full_academic_record', 'name', 'course',
                    'modality', 'enrolled_count')
    search_fields = ('academic_record', 'name', 'course', 'modality')

    def enrolled_count(self, obj):
        return obj.enrolled_in.count()

    enrolled_count.short_description = 'inscrições'


class InstituteModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'count_lectures')
    search_fields = ('code', 'name')

    def count_lectures(self, obj):
        return obj.lectures.count()

    count_lectures.short_description = 'número de disciplinas'


class LectureModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description')
    search_fields = ('code', 'name', 'description')


class LectureInstanceModelAdmin(admin.ModelAdmin):
    list_display = ('lecture_code', 'group', 'year', 'semester',
                    'lecture_description', 'enrolled_students')
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
admin.site.register(Institute, InstituteModelAdmin)
