from django.contrib import admin

from .models import Student, Lecture, LectureInstance

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('academic_record', 'name', 'course', 'modality')
    search_fields = ('academic_record', 'name', 'course', 'modality')


class LectureModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description')
    search_fields = ('code', 'name', 'description')


class LectureInstanceModelAdmin(admin.ModelAdmin):
    list_display = ('lecture_code', 'group', 'lecture_description')
    search_fields = ('lecture__code', 'group', 'lecture__description')

    def lecture_code(self, obj):
        return obj.lecture.code

    def lecture_description(self, obj):
        return obj.lecture.description

admin.site.register(Student, StudentModelAdmin)
admin.site.register(Lecture, LectureModelAdmin)
admin.site.register(LectureInstance, LectureInstanceModelAdmin)
