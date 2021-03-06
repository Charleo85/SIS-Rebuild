from django.http import JsonResponse, HttpResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

import urllib.request
import urllib.parse
import json, random
import requests


# Retrieve and format generic courses for evey department (that were offered in the past two semesters)
# (in a list?) sorted in numerical order
# 28 depts in the college
# 11 engineering depts
# 4 depts in Curry School
# Various other schools as well (A School, nursing school..) will address later
def department_courses(request, specific_department):

    if specific_department == 'african-american-and-african-studies':
        query = {'mnemonic_list': 'AAS'}
    elif specific_department == 'american-sign-language':
        query = {'mnemonic_list': 'ASL'}
    elif specific_department == 'american-studies':
        query = {'mnemonic_list': 'AMST'}
    elif specific_department == 'anthropology':
        query = {'mnemonic_list': 'ANTH'}
    elif specific_department == 'art':
        query = {'mnemonic_list': 'ARTS ARTH ARAD ARAH ARAD'}
    elif specific_department == 'astronomy':
        query = {'mnemonic_list': 'ASTR'}
    elif specific_department == 'biology':
        query = {'mnemonic_list': 'BIOL HBIO'}
    elif specific_department == 'chemistry':
        query = {'mnemonic_list': 'CHEM'}
    elif specific_department == 'classics':
        query = {'mnemonic_list': 'CLAS GREE LATI'}
    elif specific_department == 'cognitive-science':
        query = {'mnemonic_list': 'COGS'}
    elif specific_department == 'college-advising-seminars':
        query = {'mnemonic_list': 'COLA'}
    elif specific_department == 'computer-science':
        query = {'mnemonic_list': 'CS'}
    elif specific_department == 'drama':
        query = {'mnemonic_list': 'DANC DRAM'}
    elif specific_department == 'east-asian-languages-literatures-cultures':
        query = {'mnemonic_list': 'CHIN CHTR EALC EAST JAPN JPTR KOR KRTR TBTN'}
    elif specific_department == 'economics':
        query = {'mnemonic_list': 'ECON'}
    elif specific_department == 'english':
        query = {'mnemonic_list': 'CPLT ENAM ENCR ENCW ENEC ENGL ENGN ENLP ENLT ENMC ENMD ENNC ENPG ENPW ENRN ENSP ENWR'}
    elif specific_department == 'environmental-sciences':
        query = {'mnemonic_list': 'EVAT EVEC EVGE EVHY EVSC'}
    elif specific_department == 'environmental-thought-practice':
        query = {'mnemonic_list': 'ETP'}
    elif specific_department == 'french-languages-literatures':
        query = {'mnemonic_list': 'CREO FREN FRTR'}
    elif specific_department == 'german-languages-literatures':
        query = {'mnemonic_list': 'GERM GETR'}
    elif specific_department == 'global-development-studies':
        query = {'mnemonic_list': 'GDS GSGS GSSJ GSVS'}
    elif specific_department == 'history':
        query = {'mnemonic_list': 'HIAF HIEA HIEU HILA HIME HISA HIST HIUS MSP'}
    elif specific_department == 'jewish-studies':
        query = {'mnemonic_list': 'JWST'}
    # SPECIAL CASE - ONLY SOME CLASSES FROM BELOW DEPTS NEEDED, NOT ALL
    # Must address this in future.
    elif specific_department == 'latin-american-studies':
        query = {'mnemonic_list': 'HILA LAST SOC SPAN'}
    elif specific_department == 'liberal-arts-seminars':
        query = {'mnemonic_list': 'LASE'}
    # SPECIAL CASE - ONLY SOME CLASSES FROM BELOW DEPTS NEEDED, NOT ALL
    # Must address this in future.
    elif specific_department == 'linguistics':
        query = {'mnemonic_list': 'AMST ANTH EDHS FREN LING LNGS MDST MEST PSYC SPAN'}
    elif specific_department == 'mathematics':
        query = {'mnemonic_list': 'MATH'}
    elif specific_department == 'media-studies':
        query = {'mnemonic_list': 'MDST'}
    # SPECIAL CASE - MUST ADDRESS
    elif specific_department == 'medieval-studies':
        query = {'mnemonic_list': ''}
    elif specific_department == 'middle-eastern-south-asian-languages-cultures':
        query = {'mnemonic_list': 'ARAB HEBR HIND MESA MEST PERS PETR SANS SAST SATR URDU'}
    # SPECIAL CASE - MUST ADDRESS
    elif specific_department == 'middle eastern-studies':
        query = {'mnemonic_list': ''}
    elif specific_department == 'music':
        query = {'mnemonic_list': 'MUBD MUEN MUPF MUSI'}
    elif specific_department == 'neuroscience':
        query = {'mnemonic_list': 'NESC'}
    elif specific_department == 'pavilion-seminars':
        query = {'mnemonic_list': 'PAVS'}
    elif specific_department == 'philosophy':
        query = {'mnemonic_list': 'PHIL'}
    elif specific_department == 'physics':
        query = {'mnemonic_list': 'PHYS'}
    elif specific_department == 'political-social-thought':
        query = {'mnemonic_list': 'PST'}
    elif specific_department == 'politics':
        query = {'mnemonic_list': 'PLAD PLAP PLCP PLIR PLPT '}
    elif specific_department == 'psychology':
        query = {'mnemonic_list': 'PSYC'}
    elif specific_department == 'public-health-sciences':
        query = {'mnemonic_list': 'PHS PHSE'}
    elif specific_department == 'religious-studies':
        query = {'mnemonic_list': 'RELA RELB RELC RELG RELH RELI RELJ RELS'}
    elif specific_department == 'slavic-languages-literatures':
        query = {'mnemonic_list': 'POL RUSS RUTR SLAV SLFK SLTR'}
    elif specific_department == 'sociology':
        query = {'mnemonic_list': 'SOC'}
    # SPECIAL CASE - MUST ADDRESS
    elif specific_department == 'south-asian-studies':
        query = {'mnemonic_list': ''}
    elif specific_department == 'spanish-italian-portuguese':
        query = {'mnemonic_list': 'ITAL ITTR KICH PORT SPAN SPTR'}
    elif specific_department == 'statistics':
        query = {'mnemonic_list': 'STAT'}
    # SPECIAL CASE _ MUST ADDRESS
    elif specific_department == 'women-gender-sexuality':
        query = {'mnemonic_list': 'WGS'}

    # TODO: ENGINEERING SCHOOL AND CURRY SCHOOL

    response_dict = requests.get('http://models-api:8000/apiv2/course/', query).json()
    # JSON looks like this: {match: [list of course dicts], status code : 200}

    if response_dict['status_code'] == 200 and response_dict['match']:
        for course in response_dict['match']:
            course['course_href'] = '/course/' + course['mnemonic'] + course['number']

    return JsonResponse(response_dict)


# Retrieve and format data (generic course lists) pertaining to a single mnemonic
# TODO: Allow for arbitrary mnemonic search, i.e. a "mnemonic selector" in the web that passes the selections here
def mnemonic_courses(request, mnemonic):

    query = {'mnemonic_list': mnemonic}
    response_dict = requests.get('http://models-api:8000/apiv2/course/', query).json()

    if response_dict['status_code'] == 200 and response_dict['match']:
        for course in response_dict['match']:
            course['course_href'] = '/course/' + course['mnemonic'] + course['number']  + '/'

    return JsonResponse(response_dict)


# Retrieve and format info needed to display all information for a generic course page
# Including all past instructors/sections and associated links.
def course_detail(request, mnemonic, number):

    query = {'mnemonic': mnemonic, 'number': number}
    response_dict = requests.get('http://models-api:8000/apiv2/course/', query).json()

    if response_dict['status_code'] == 200 and response_dict['match']:
        # TODO: str(section['id']) must eventually change to str(section['sisid'])
        for section in response_dict['match']['sections']:
            section['section_href'] = '/section/' + str(section['id']) + '/' + str(section['semester']) + '/'

    return JsonResponse(response_dict)


# TODO: SIS-ID isn't in fixture yet, so using django-generated id for now ( section_id isn't sufficient for uniqueness)
# TODO: Figure out a way to get SIS-IDs into the fixture
# Retrieve and format info needed to display all information for a section page
def section_detail(request, id, semester):

    # NOT SUFFICIENT!
    query = {'id': id, 'semester': semester}
    response_dict = requests.get('http://models-api:8000/apiv2/section/', query).json()

    if response_dict['status_code'] == 200 and response_dict['match']:
        for section in response_dict['match']:
            section['instructor']['instructor_href'] = '/instructor/' +  section['instructor']['computing_id'] + '/'

    return JsonResponse(response_dict)


# Retrieve and format data pertaining to an instructor (courses taught, average GPA total, etc.)
def instructor_detail(request, computing_id):

    query = {'computing_id': computing_id}
    response_dict = requests.get('http://models-api:8000/apiv2/instructor', query).json()

    if response_dict['status_code'] == 200 and response_dict['match']:
        instructor = response_dict['match'][0]

        for section in instructor['instructor_sections']:
            section['section_href'] = '/section/' + str(section['id']) + '/' + str(section['semester']) + '/'

    # TODO: Calculate average GPA over all associated sections

    return JsonResponse(response_dict)


# Retrieve and format data pertaining to ALL Courses - is this necessary/needed? Seems like an expensive operation.
def course_all(request):
    # Tong or Charlie, what does the query dict need so that the API gives me all courses??
    pass


# Perhaps this could be used to show 'easiest courses'? Or most clicked courses? (Using logged data)
def home_page(request):
    pass


def index(request):
    return HttpResponse('Success!')


##########################
# def search(request):
#     if request.method != 'POST':
#         data = {'status_code': 400, 'error_msg': 'incorrect request type'}
#         return JsonResponse(data)
#
#     search_request = request.POST.dict()
#     search_string = search_request['search_query']
#     search_index_specifier = search_request['query_specifier']
#     elasticsearch_index = search_index_specifier + '_index'
#
#     es = Elasticsearch(['es'])
#     try:
#         search_result = es.search(index=elasticsearch_index, body={
#             "query": {'query_string': {'query': search_string}},
#             'size': 100,
#         })
#     except:
#         data = {'status_code': 400, 'error_msg': 'improper search query'}
#         return JsonResponse(data)
#
#     result = {'status_code': 200}
#     result['time_taken'] = search_result['took'] / 1000
#     result['size'] = search_result['hits']['total']
#
#     result['size_model'] = {'course': 0, 'instructor': 0, 'student': 0}
#     result['hits'] = []
#     for item in search_result['hits']['hits']:
#         detail = {'model': item['_source']['model']}
#
#         if item['_source']['model'] == 'api.Course':
#             detail['label'] = item['_source']['fields']['mnemonic']
#             detail['label'] += ' ' + item['_source']['fields']['number']
#             if 'title' in item['_source']['fields']:
#                 detail['label'] += ': ' + item['_source']['fields']['title']
#
#             url = 'http://models-api:8000/api/instructor/detail/'
#             url += item['_source']['fields']['instructor'] + '/'
#             resp = _make_get_request(url)
#
#             detail['label'] += ' (' + resp['instructor']['first_name']
#             detail['label'] += ' ' + resp['instructor']['last_name'] + ')'
#         else:
#             detail['label'] = item['_source']['fields']['first_name']
#             detail['label'] += ' ' + item['_source']['fields']['last_name']
#             detail['label'] += ' (' + item['_source']['fields']['id'] + ')'
#
#         if detail['model'] == 'api.Course':
#             result['size_model']['course'] += 1
#             detail['href'] = '/course/detail/' + item['_id'] + '/'
#         elif detail['model'] == 'api.Instructor':
#             result['size_model']['instructor'] += 1
#             detail['href'] = '/instructor/detail/' + item['_id'] + '/'
#         else:
#             result['size_model']['student'] += 1
#             detail['href'] = '/student/detail/' + item['_id'] + '/'
#
#         result['hits'].append(detail)
#
#     # returns the final constructed data set
#     return JsonResponse(result)
