from django.http import JsonResponse, HttpResponse

import urllib.request
import urllib.parse
import json

# Create your views here
def _make_get_request(url):
    req = urllib.request.Request(url)
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

    course_data = []
    for course_dict in selected_courses:
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
        course_data.append(new_dict)

    new_data['popular_courses'] = course_data
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
