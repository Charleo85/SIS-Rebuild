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
    elif specific_department == 'french-language-literature':
        query = {'mnemonic_list': 'CREO FREN FRTR'}
    elif specific_department == 'german-language-literature':
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

    # TODO: ENGINEERING SCHOOL

    response_dict = json.loads(((requests.get('http://models-api:8000/apiv2/course/', query)).json()))
    # JSON looks like this: {match: [list of course dicts], status code : 200}

    for course in response_dict['match']:
        course['course_href'] = '/' + course['mnemonic'] + course['number']

    # Additional Data processing here:
    # - Add the course hrefs - done
    # - Error checking
    #       - Perhaps if courses['match'] is empty, return a 404
    #       - Or if courses status code is not 200, give a helpful error message

    return JsonResponse(response_dict)


# Retrieve and format data (generic course lists) pertaining to a single mnemonic
# TODO: Allow for arbitrary mnemonic search
def mnemonic_courses(request, mnemonic):

    query = {'mnemonic_list': mnemonic}
    response_dict = json.loads((requests.get('http://models-api:8000/apiv2/course/', query)).json())

    for course in response_dict['match']:
        course['course_href'] = '/' + course['mnemonic'] + course['number']  + '/'

    return JsonResponse(response_dict)


# Retrieve and format info needed to display all information for a generic course page
# Including all past instructors/sections and associated links.
def course_detail(request, mnemonic, number):

    query = {'mnemonic': mnemonic, 'number': number}
    response_dict = json.loads((requests.get('http://models-api:8000/apiv2/course/', query)).json())
    # Response dict will contain all of the average grade data as well a list of dicts of sections

    for section in response_dict['match']['sections']:
        section['section_href'] = '/' + section['sis_id'] + '/' + section['semester'] + '/'

    return JsonResponse(response_dict)


# Retrieve and format data pertaining to ALL Courses - is this necessary/needed? Seems like an expensive operation.
def course_all(request):
    # Tong or Charlie, what does the query dict need so that the API gives me all courses??
    pass


# Retrieve and format info needed to display all information for a section page
def section_detail(request, sis_id, semester):

    query = {'sis_id': sis_id, 'semester': semester}
    response_dict = json.loads((requests.get('http://models-api:8000/apiv2/course/', query)).json())
    # UNFINISHED
    return JsonResponse(response_dict)


# Retrieve and format data pertaining to an instructor (courses taught, average GPA total, etc.)
def instructor_information(request):
    pass


# Perhaps this could be used to show 'easiest courses'? Or most clicked courses? (Using logged data)
def home_page(request):
    pass


def index(request):
    return HttpResponse('Success!')


##########################
#
# def _process_course(course_dict):
#     new_dict = {}
#     new_dict['coursehref'] = '/course/detail/' + course_dict['id'] + '/'
#     new_dict['instructorhref'] = '/instructor/detail/'
#     new_dict['instructorhref'] += course_dict['instructor'] + '/'
#
#     new_dict['course_name'] = course_dict['mnemonic'] + ' '
#     new_dict['course_name'] += course_dict['number']
#     if course_dict['section'] != '':
#         new_dict['course_name'] += " - " + course_dict['section']
#     if course_dict['title'] != '':
#         new_dict['course_name'] += "<br>" + course_dict['title']
#
#     new_dict['instructor'] = _get_instructor(course_dict['instructor'])
#     return new_dict


# def course_all(request):
#     url = 'http://models-api:8000/api/course/all/'
#     resp = _make_get_request(url)
#
#     new_data = {}
#     new_data['status_code'] = resp['status_code']
#
#     course_data = []
#     for course_dict in resp['all_courses']:
#         new_dict = {}
#         new_dict['coursehref'] = '/course/detail/' + course_dict['id'] + '/'
#         new_dict['instructorhref'] = '/instructor/detail/'
#         new_dict['instructorhref'] += course_dict['instructor'] + '/'
#
#         new_dict['course_name'] = course_dict['mnemonic'] + ' '
#         new_dict['course_name'] += course_dict['number']
#         if course_dict['section'] != '':
#             new_dict['course_name'] += " - " + course_dict['section']
#         if course_dict['title'] != '':
#             new_dict['course_name'] += ": " + course_dict['title']
#
#         new_dict['instructor'] = _get_instructor(course_dict['instructor'])
#         new_dict['enrollment_info'] = str(course_dict['current_enrolled'])
#         new_dict['enrollment_info'] += '/' + str(course_dict['max_students'])
#         course_data.append(new_dict)
#
#     new_data['all_courses'] = course_data
#     return JsonResponse(new_data)
#
#
# def course_detail(request, sisid):
#     url = 'http://models-api:8000/api/course/detail/' + sisid + '/'
#     resp = _make_get_request(url)
#
#     if resp['status_code'] == 200:
#         new_dict = resp['course']
#         for key in list(new_dict):
#             if new_dict[key] == '':
#                 new_dict.pop(key, None)
#
#         new_dict['instructor'] = _get_instructor(new_dict['instructor'])
#         resp['course'] = new_dict
#
#     return JsonResponse(resp)



# Course creation should not be done through exp layer
# since it is only done through fixture parsing/loading in models layer

# def course_create(request):
#     new_course_data = request.POST.dict()
#     instructor_id = new_course_data['instructor']
#
#     # Determine if course already exists
#     sisid = new_course_data['id']
#     url_for_course_duplicate_check =  'http://models-api:8000/api/course/detail/' + sisid + '/'
#     resp = _make_get_request(url_for_course_duplicate_check)
#     if resp['status_code'] == 404:
#         url_for_course_creation = 'http://models-api:8000/api/course/create/'
#         post_response = _make_post_request(url_for_course_creation, new_course_data)
#         if post_response["status_code"] == 201:
#             # Index the new course into elastic search
#             producer = KafkaProducer(bootstrap_servers='kafka:9092')
#             new_dict = {}
#             new_dict['model'] = 'api.Course'
#             new_dict['fields'] = new_course_data
#             producer.send('new-listings-topic', json.dumps(new_dict).encode('utf-8'))
#             return JsonResponse(post_response) #Success!!!
#         else:
#             error = {'status_code': 400, 'error_message': 'cannot create course; check your inputs'}
#             return JsonResponse(error)
#     else:
#         # Course already exists, return error message
#         error = {'status_code': 400, 'error_message': 'course already exists'}
#         return JsonResponse(error)
#
#
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
#
#
# def instructor_all(request):
#     url = 'http://models-api:8000/api/instructor/all/'
#     resp = _make_get_request(url)
#
#     new_data = {}
#     new_data['status_code'] = resp['status_code']
#
#     instructor_data = []
#     for ins_dict in resp['all_instructors']:
#         new_dict = {}
#         new_dict['href'] = '/instructor/detail/' + ins_dict['id'] + '/'
#         new_dict['instructor_name'] = ins_dict['first_name'] + ' '
#         new_dict['instructor_name'] += ins_dict['last_name']
#         new_dict['instructor_name'] += ' (' + ins_dict['id'] + ')'
#         instructor_data.append(new_dict)
#
#     new_data['all_instructors'] = instructor_data
#     return JsonResponse(new_data)
#
#
# def instructor_detail(request, compid):
#     url = 'http://models-api:8000/api/instructor/detail/' + compid + '/'
#     resp = _make_get_request(url)
#
#     if resp['status_code'] == 200:
#         teaching = ''
#         teaching_courses = resp['instructor']['teaching_courses']
#         if teaching_courses == []:
#             resp['instructor'].pop('teaching_courses', None)
#         else:
#             for i in range(len(teaching_courses)):
#                 teaching += teaching_courses[i]
#                 if (i != len(teaching_courses) - 1):
#                     teaching += ', '
#             resp['instructor']['teaching_courses'] = teaching
#
#     return JsonResponse(resp)
