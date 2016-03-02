import re
from bs4 import BeautifulSoup as HtmlBrowser
from re import search, findall, MULTILINE
from requests import get


# URLS pointing to DAC directories
URLS = {
    'grad': {
        'institutes': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/indiceP.htm',
        'lectures': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/{}.htm',
        'lecture': 'http://www.dac.unicamp.br/sistemas/horarios/grad/G{}S0/{}.htm'
    },
    'pos': {
        'institutes': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/indiceP.htm',
        'lectures': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/{}.htm',
        'lecture': 'http://www.dac.unicamp.br/sistemas/horarios/pos/P{}S/{}.htm'
    }
}


def crawl_institutes(**options):
    """
    Gets list of institutes
    """
    degree, semester = options['degree_level'], options['semester']
    catalog_url = URLS[degree]['institutes'].format(semester)
    institutes_html = get(catalog_url).text
    return findall(r'href="(.*)\.htm\s*"', institutes_html)


def crawl_lectures_grad(institute, **options):
    """
    Get list of lectures for the given institute
    for the graduation degree level
    """
    semester = options['semester']
    lectures_url = URLS['grad']['lectures'].format(semester, institute)
    lectures_html = get(lectures_url).text
    return findall(r'href="(.*)\.htm\s*"', lectures_html)


def crawl_lecture_grad(lecture, **options):
    """
    Get the list of groups for a given lecture
    on the graduation degree level
    """
    semester = options['semester']
    lecture_url = URLS['grad']['lecture'].format(semester, lecture)
    html = HtmlBrowser(get(lecture_url).text, 'html.parser')

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
        'groups': turmas
    }


def _test_institutes():
    expected = {
        'grad': {
            'count': 26
        },
        'pos': {
            'count': 23
        }
    }

    for degree_level, exp in expected.items():
        institutes = crawl_institutes(degree_level=degree_level, semester=1)
        assert exp['count'] == len(institutes)
        assert len(institutes) == len(set(institutes))
        print('Institutes for {}: {}'.format(degree_level, institutes))


def _test_lectures():
    expected = {
        'IA': {
            'count': 425
        }
    }
    for institute, exp in expected.items():
        lectures = crawl_lectures_grad(institute, semester=1)
        assert exp['count'] == len(lectures)
        assert len(lectures) == len(set(lectures))
        print('Lectures on {}: {}'.format(institute, lectures))

def _test_lecture():
    tests = ['F_037', 'MC102', 'CV916']
    for t in tests:
        print(crawl_lecture_grad(t, semester=1))


if __name__ == '__main__':
    _test_institutes()
    _test_lectures()
    _test_lecture()
