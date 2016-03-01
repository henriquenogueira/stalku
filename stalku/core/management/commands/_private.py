from re import findall
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
    semester = options['semester']
    lectures_url = URLS['grad']['lectures'].format(semester, institute)
    lectures_html = get(lectures_url).text
    return findall(r'href="(.*)\.htm\s*"', lectures_html)

def test_institutes():
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


def test_lectures():
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

if __name__ == '__main__':
    test_institutes()
    test_lectures()
