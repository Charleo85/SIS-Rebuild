from django.http import JsonResponse, HttpResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

import urllib.request
import urllib.parse
import json, random

# Create your views here
def _make_get_request(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def _make_post_request(url, post_data):
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def _get_instructor(ins_id):
    url = 'http://models-api:8000/api/instructor/detail/' + ins_id + '/'
    resp_ins = _make_get_request(url)
    data = resp_ins['instructor']

    result = data['first_name'] + ' ' + data['last_name']
    result += ' (' + data['id'] + ')'
    return result


def _get_student(stud_id):
    url = 'http://models-api:8000/api/student/detail/' + stud_id + '/'
    resp_stud = _make_get_request(url)
    data = resp_stud['student']

    result = data['first_name'] + ' ' + data['last_name']
    result += ' (' + data['id'] + ')'
    return result


def _get_course(course_id):
    url = 'http://models-api:8000/api/course/detail/' + course_id + '/'
    resp_c = _make_get_request(url)
    return resp_c['course']['mnemonic'] + ' ' + resp_c['course']['number']


def _process_course(course_dict):
    new_dict = {}
    new_dict['coursehref'] = '/course/detail/' + course_dict['id'] + '/'
    new_dict['instructorhref'] = '/instructor/detail/'
    new_dict['instructorhref'] += course_dict['instructor'] + '/'

    new_dict['course_name'] = course_dict['mnemonic'] + ' '
    new_dict['course_name'] += course_dict['number']
    if course_dict['section'] != '':
        new_dict['course_name'] += " - " + course_dict['section']
    if course_dict['title'] != '':
        new_dict['course_name'] += "<br>" + course_dict['title']

    new_dict['instructor'] = _get_instructor(course_dict['instructor'])
    return new_dict


def index(request):
    return HttpResponse('Success!')


def home_page(request):
    url = 'http://models-api:8000/api/course/all/'
    resp = _make_get_request(url)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    selected_courses = [{}, {}, {}]
    num_enrolled = [0, 0, 0]
    for course_dict in resp['all_courses']:
        for i in range(3):
            num = course_dict['current_enrolled']
            if num > num_enrolled[i]:
                num_enrolled.insert(i, num)
                selected_courses.insert(i, course_dict)
                num_enrolled = num_enrolled[0:3]
                selected_courses = selected_courses[0:3]
                break

    other_courses = []
    for course_dict in resp['all_courses']:
        selected = False
        for popular in selected_courses:
            if course_dict['id'] == popular['id']:
                selected = True
                break
        if not selected:
            other_courses.append(course_dict)

    popular_courses = []
    for course_dict in selected_courses:
        new_dict = _process_course(course_dict)
        popular_courses.append(new_dict)

    explore_courses = []
    index = random.randint(0, len(other_courses)-4)
    for i in range(index, index+3):
        new_dict = _process_course(other_courses[i])
        explore_courses.append(new_dict)

    new_data['popular_courses'] = popular_courses
    new_data['explore_courses'] = explore_courses
    return JsonResponse(new_data)


def course_all(request):
    url = 'http://models-api:8000/api/course/all/'
    resp = _make_get_request(url)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    course_data = []
    for course_dict in resp['all_courses']:
        new_dict = {}
        new_dict['coursehref'] = '/course/detail/' + course_dict['id'] + '/'
        new_dict['instructorhref'] = '/instructor/detail/'
        new_dict['instructorhref'] += course_dict['instructor'] + '/'

        new_dict['course_name'] = course_dict['mnemonic'] + ' '
        new_dict['course_name'] += course_dict['number']
        if course_dict['section'] != '':
            new_dict['course_name'] += " - " + course_dict['section']
        if course_dict['title'] != '':
            new_dict['course_name'] += ": " + course_dict['title']

        new_dict['instructor'] = _get_instructor(course_dict['instructor'])
        new_dict['enrollment_info'] = str(course_dict['current_enrolled'])
        new_dict['enrollment_info'] += '/' + str(course_dict['max_students'])
        course_data.append(new_dict)

    new_data['all_courses'] = course_data
    return JsonResponse(new_data)


def course_detail(request, sisid):
    url = 'http://models-api:8000/api/course/detail/' + sisid + '/'
    resp = _make_get_request(url)

    if resp['status_code'] == 200:
        new_dict = resp['course']
        for key in list(new_dict):
            if new_dict[key] == '':
                new_dict.pop(key, None)

        new_dict['instructor'] = _get_instructor(new_dict['instructor'])
        resp['course'] = new_dict

    return JsonResponse(resp)


def course_create(request):
    new_course_data = request.POST.dict()
    instructor_id = new_course_data['instructor']

    # Determine if course already exists
    sisid = new_course_data['id']
    url_for_course_duplicate_check = 'http://models-api:8000/api/course/detail/' + sisid + '/'
    resp = _make_get_request(url_for_course_duplicate_check)
    if resp['status_code'] == 404:
        url_for_course_creation = 'http://models-api:8000/api/course/create/'
        post_response = _make_post_request(url_for_course_creation, new_course_data)
        if post_response["status_code"] == 201:
            # Index the new course into elastic search
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            new_dict = {}
            new_dict['model'] = 'api.Course'
            new_dict['fields'] = new_course_data
            producer.send('new-listings-topic', json.dumps(new_dict).encode('utf-8'))
            return JsonResponse(post_response)  # Success!!!
        else:
            error = {'status_code': 400, 'error_message': 'cannot create course; check your inputs'}
            return JsonResponse(error)
    else:
        # Course already exists, return error message
        error = {'status_code': 400, 'error_message': 'course already exists'}
        return JsonResponse(error)


def search(request):
    if request.method != 'POST':
        data = {'status_code': 400, 'error_msg': 'incorrect request type'}
        return JsonResponse(data)

    search_request = request.POST.dict()
    search_string = search_request['search_query']
    search_index_specifier = search_request['query_specifier']
    elasticsearch_index = search_index_specifier + '_index'

    es = Elasticsearch(['es'])
    try:
        search_result = es.search(index=elasticsearch_index, body={
            "query": {'query_string': {'query': search_string}},
            'size': 100,
        })
    except:
        data = {'status_code': 400, 'error_msg': 'improper search query'}
        return JsonResponse(data)

    result = {'status_code': 200}
    result['time_taken'] = search_result['took'] / 1000
    result['size'] = search_result['hits']['total']

    result['size_model'] = {'course': 0, 'instructor': 0, 'student': 0}
    result['hits'] = []
    for item in search_result['hits']['hits']:
        detail = {'model': item['_source']['model']}

        if item['_source']['model'] == 'api.Course':
            detail['label'] = item['_source']['fields']['mnemonic']
            detail['label'] += ' ' + item['_source']['fields']['number']
            if 'title' in item['_source']['fields']:
                detail['label'] += ': ' + item['_source']['fields']['title']

            url = 'http://models-api:8000/api/instructor/detail/'
            url += item['_source']['fields']['instructor'] + '/'
            resp = _make_get_request(url)

            detail['label'] += ' (' + resp['instructor']['first_name']
            detail['label'] += ' ' + resp['instructor']['last_name'] + ')'
        else:
            detail['label'] = item['_source']['fields']['first_name']
            detail['label'] += ' ' + item['_source']['fields']['last_name']
            detail['label'] += ' (' + item['_source']['fields']['id'] + ')'

        if detail['model'] == 'api.Course':
            result['size_model']['course'] += 1
            detail['href'] = '/course/detail/' + item['_id'] + '/'
        elif detail['model'] == 'api.Instructor':
            result['size_model']['instructor'] += 1
            detail['href'] = '/instructor/detail/' + item['_id'] + '/'
        else:
            result['size_model']['student'] += 1
            detail['href'] = '/student/detail/' + item['_id'] + '/'

        result['hits'].append(detail)

    # returns the final constructed data set
    return JsonResponse(result)


def instructor_all(request):
    url = 'http://models-api:8000/api/instructor/all/'
    resp = _make_get_request(url)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    instructor_data = []
    for ins_dict in resp['all_instructors']:
        new_dict = {}
        new_dict['href'] = '/instructor/detail/' + ins_dict['id'] + '/'
        new_dict['instructor_name'] = ins_dict['first_name'] + ' '
        new_dict['instructor_name'] += ins_dict['last_name']
        new_dict['instructor_name'] += ' (' + ins_dict['id'] + ')'
        instructor_data.append(new_dict)

    new_data['all_instructors'] = instructor_data
    return JsonResponse(new_data)


def instructor_detail(request, compid):
    url = 'http://models-api:8000/api/instructor/detail/' + compid + '/'
    resp = _make_get_request(url)

    if resp['status_code'] == 200:
        teaching = ''
        teaching_courses = resp['instructor']['teaching_courses']
        if teaching_courses == []:
            resp['instructor'].pop('teaching_courses', None)
        else:
            for i in range(len(teaching_courses)):
                teaching += teaching_courses[i]
                if (i != len(teaching_courses) - 1):
                    teaching += ', '
            resp['instructor']['teaching_courses'] = teaching

    return JsonResponse(resp)


def student_all(request):
    url = 'http://models-api:8000/api/student/all/'
    resp = _make_get_request(url)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    student_data = []
    for stud_dict in resp['all_students']:
        new_dict = {}
        new_dict['href'] = '/student/detail' + stud_dict['id'] + '/'
        new_dict['student_name'] = stud_dict['first_name'] + ' '
        new_dict['student_name'] += stud_dict['last_name']
        new_dict['student_name'] += ' (' + stud_dict['id'] + ')'
        student_data.append(new_dict)

    new_data['all_students'] = student_data
    return JsonResponse(new_data)


def student_detail(request, compid):
    url = 'http://models-api:8000/api/student/detail/' + compid + '/'
    resp = _make_get_request(url)

    if resp['status_code'] == 200:
        if resp['student']['taking_courses'] == []:
            resp['student'].pop('taking_courses', None)
        else:
            new_course = ''
            for i in range(len(resp['student']['taking_courses'])):
                new_course += _get_course(resp['student']['taking_courses'][i])
                if (i != len(resp['student']['taking_courses']) - 1):
                    new_course += ', '
            resp['student']['taking_courses'] = new_course

    return JsonResponse(resp)


def enrollment_all(request):
    url = 'http://models-api:8000/api/enrollment/all/'
    resp = _make_get_request(url)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    enrollment_data = []
    for enr_dict in resp['all_enrollments']:
        new_dict = {}
        new_dict['href'] = '/enrollment/detail' + str(enr_dict['id']) + '/'
        new_dict['enrollment_name'] = enr_dict['student'] + ':'
        new_dict['enrollment_name'] += enr_dict['course']
        enrollment_data.append(new_dict)

    new_data['all_enrollments'] = enrollment_data
    return JsonResponse(new_data)


def enrollment_detail(request, enrid):
    url = 'http://models-api:8000/api/enrollment/detail/' + enrid + '/'
    resp = _make_get_request(url)

    if resp['status_code'] == 200:
        data = resp['enrollment']
        data['student'] = _get_student(data['student'])
        data['course'] = _get_course(data['course'])
        resp['enrollment'] = data

    return JsonResponse(resp)
