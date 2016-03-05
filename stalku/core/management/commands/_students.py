from bs4 import BeautifulSoup as HtmlBrowser
from django.conf import settings
from . import cookie, token, session


def get_students_for_lecture_instance(li, **options):
    # Data to submit on the POST request
    data = {
        'org.apache.struts.taglib.html.TOKEN': token,
        'cboSubG': options['semester'],
        'cboSubP': 0,
        'cboAno': options['year'],
        'txtDisciplina': li.lecture.code,
        'txtTurma': li.group,
        'btnAcao': 'Continuar'
    }

    # Getting and parsing page
    r = session.post(settings.SEARCH_LECTURE_URL, data, headers={'Cookie': cookie})
    html = HtmlBrowser(r.text, 'html.parser')

    students = []
    students_data = html.select('tr[height="18"] td[bgcolor="white"]')[1:]
    for student_data in students_data[::6]:
        # Extracting students data from <table>
        data = tuple(student_data.parent.text.replace('\xa0', '').split('\n')[2:])
        record, name, course, modality, *_ = data

        # Keeping the student recod
        students.append({
            'academic_record': record,
            'name': name.strip(),
            'course': course,
            'modality': modality
        })

    return students
