from requests import post
from bs4 import BeautifulSoup as HtmlBrowser

def _get_headers(**options):
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=557887B218E828548D56C1E56ABD1980',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }


def get_students_for_lecture_instance(li, **options):
    data = {
        'org.apache.struts.taglib.html.TOKEN': 'f3bb87a550df01d96ccb9f45e0026727',
        'cboSubG': options['semester'],
        'cboSubP': 0,
        'cboAno': options['year'],
        'txtDisciplina': li.lecture.code,
        'txtTurma': li.group,
        'btnAcao': 'Continuar'
    }

    url = 'http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do'
    r = post(url, data, headers=_get_headers())
    html = HtmlBrowser(r.text, 'html.parser')

    students = []
    students_data = html.select('tr[height="18"] td[bgcolor="white"]')[1:]
    for student_data in students_data[::6]:
        data = tuple(student_data.parent.text.replace('\xa0', '').split('\n')[2:])
        record, name, course, modality, *_ = data
        students.append({
            'academic_record': record,
            'name': name.strip(),
            'course': course,
            'modality': modality
        })
    return students


def main():
    print(get_students_for_lecture_instance(None, semester=1, year=2016))


if __name__ == '__main__':
    main()

