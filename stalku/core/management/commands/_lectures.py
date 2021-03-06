from re import findall

from bs4 import BeautifulSoup as HtmlBrowser
from django.conf import settings
from . import session


def crawl_institutes(**options):
    """
    Gets list of institutes
    """
    degree, semester = options['degree_level'], options['semester']
    catalog_url = settings.LECTURES_URLS[degree]['institutes'].format(semester)
    institutes_html = session.get(catalog_url).text
    result = findall(r'href="(.*)\.htm\s*">(.*)\s?</a+', institutes_html)
    return [{'code': code, 'name': name.strip()} for code, name in result]


def crawl_lectures_grad(institute, **options):
    """
    Get list of lectures for the given institute
    for the graduation degree level
    """
    semester = options['semester']
    lectures_url = settings.LECTURES_URLS['grad']['lectures'].format(semester, institute)
    lectures_html = session.get(lectures_url).text
    return findall(r'href="(.*)\.htm\s*"', lectures_html)


def crawl_lecture_grad(lecture, **options):
    """
    Get the list of groups for a given lecture
    on the graduation degree level
    """
    semester = options['semester']
    lecture_url = settings.LECTURES_URLS['grad']['lecture'].format(semester, lecture)
    html = HtmlBrowser(session.get(lecture_url).text, 'html.parser')

    title = html.select('a[name]')[0].parent.text
    details = html.select('table > tr > td:nth-of-type(2) > font > font')[0].text
    turmas = findall(r'Turma:\s*(\S)', html.text)

    cleaned_code = lecture.replace('_', ' ')
    cleaned_title = title.replace(cleaned_code, '').strip()
    cleaned_details = details[:-1].replace('\n', '').strip()

    # TODO: Get timetables (hard, really heard)
    return {
        'code': cleaned_code,
        'name': cleaned_title,
        'description': cleaned_details,
        'groups': turmas,
        'degree_level': options['degree_level']
    }
