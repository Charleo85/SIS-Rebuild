from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import urllib.request
import urllib.parse
import json

# Create your views here.
def index(request):
    return HttpResponse('Success!')


def getInstructor(ins_id):
    req_ins = urllib.request.Request(
        'http://models-api:8000/api/instructor/detail/' + ins_id + '/'
    )
    resp_json_ins = urllib.request.urlopen(req_ins).read().decode('utf-8')
    resp_ins = json.loads(resp_json_ins)
    data = resp_ins['instructor']

    result = data['first_name'] + ' ' + data['last_name']
    result += ' (' + data['id'] + ')'
    return result


def getStudent(stud_id):
    req_stud = urllib.request.Request(
        'http://models-api:8000/api/student/detail/' + stud_id + '/'
    )
    resp_json_stud = urllib.request.urlopen(req_stud).read().decode('utf-8')
    resp_stud = json.loads(resp_json_stud)
    data = resp_stud['student']

    result = data['first_name'] + ' ' + data['last_name']
    result += ' (' + data['id'] + ')'
    return result


def getCourse(course_id):
    req_c = urllib.request.Request(
        'http://models-api:8000/api/course/detail/' + course_id + '/'
    )
    resp_json_c = urllib.request.urlopen(req_c).read().decode('utf-8')
    resp_c = json.loads(resp_json_c)
    return resp_c['course']['mnemonic'] + ' ' + resp_c['course']['number']


def course_all(request):
    req = urllib.request.Request('http://models-api:8000/api/course/all/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    course_data = []
    for course_dict in resp['all_courses']:
        new_dict = {}
        new_dict['href'] = course_dict['id'] + '/'
        new_dict['course_name'] = course_dict['mnemonic'] + ' '
        new_dict['course_name'] += course_dict['number']
        if course_dict['section'] != '':
            new_dict['course_name'] += " - " + course_dict['section']
        if course_dict['title'] != '':
            new_dict['course_name'] += ": " + course_dict['title']

        new_dict['instructor'] = getInstructor(course_dict['instructor'])
        course_data.append(new_dict)

    new_data['all_courses'] = course_data
    return JsonResponse(new_data)


def course_detail(request, sisid):
    req = urllib.request.Request(
        'http://models-api:8000/api/course/detail/' + sisid + '/'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['status_code'] == 200:
        new_dict = resp['course']
        for key in list(new_dict):
            if new_dict[key] == '':
                new_dict.pop(key, None)

        new_dict['instructor'] = getInstructor(resp['instructor'])
        resp['course'] = new_dict

    return JsonResponse(resp)


def instructor_all(request):
    req = urllib.request.Request('http://models-api:8000/api/instructor/all/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    instructor_data = []
    for ins_dict in resp['all_instructors']:
        new_dict = {}
        new_dict['href'] = ins_dict['id'] + '/'
        new_dict['instructor_name'] = ins_dict['first_name'] + ' '
        new_dict['instructor_name'] += ins_dict['last_name']
        new_dict['instructor_name'] += ' (' + ins_dict['id'] + ')'
        instructor_data.append(new_dict)

    new_data['all_instructors'] = instructor_data
    return JsonResponse(new_data)


def instructor_detail(request, compid):
    req = urllib.request.Request(
        'http://models-api:8000/api/instructor/detail/' + compid + '/'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)


def student_all(request):
    req = urllib.request.Request('http://models-api:8000/api/student/all/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    student_data = []
    for stud_dict in resp['all_students']:
        new_dict = {}
        new_dict['href'] = stud_dict['id'] + '/'
        new_dict['student_name'] = stud_dict['first_name'] + ' '
        new_dict['student_name'] += stud_dict['last_name']
        new_dict['student_name'] += ' (' + stud_dict['id'] + ')'
        student_data.append(new_dict)

    new_data['all_students'] = student_data
    return JsonResponse(new_data)


def student_detail(request, compid):
    req = urllib.request.Request(
        'http://models-api:8000/api/student/detail/' + compid + '/'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['status_code'] == 200:
        new_course = []
        if resp['student']['taking_courses'] == []:
            resp['student'].pop('taking_courses', None)
        else:
            for course_id in resp['student']['taking_courses']:
                new_course.append(getCourse(course_id))
            resp['student']['taking_courses'] = new_course

    return JsonResponse(resp)


def enrollment_all(request):
    req = urllib.request.Request('http://models-api:8000/api/enrollment/all/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    new_data = {}
    new_data['status_code'] = resp['status_code']

    enrollment_data = []
    for enr_dict in resp['all_enrollments']:
        new_dict = {}
        new_dict['href'] = str(enr_dict['id']) + '/'
        new_dict['enrollment_name'] = enr_dict['student'] + ':'
        new_dict['enrollment_name'] += enr_dict['course']
        enrollment_data.append(new_dict)

    new_data['all_enrollments'] = enrollment_data
    return JsonResponse(new_data)


def enrollment_detail(request, enrid):
    req = urllib.request.Request(
        'http://models-api:8000/api/enrollment/detail/' + enrid + '/'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['status_code'] == 200:
        data = resp['enrollment']
        data['student'] = getStudent(data['student'])
        data['course'] = getCourse(data['course'])
        resp['enrollment'] = data

    return JsonResponse(resp)
