from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import urllib.request
import urllib.parse
import json


# Create your views here.
def index(request):
    return HttpResponse('Success!')


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
        new_dict['course_name'] = course_dict['mnemonic'] + " " + course_dict['number']
        if course_dict['section'] != '':
            new_dict['course_name'] += " - " + course_dict['section']
        if course_dict['title'] != '':
            new_dict['course_name'] += ": " + course_dict['title']
        new_dict['instructor'] = course_dict['instructor']
        course_data.append(new_dict)
    new_data['all_courses'] = course_data

    return JsonResponse(new_data)


def course_detail(request, sisid):
    req = urllib.request.Request('http://models-api:8000/api/course/' + sisid + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    
    new_dict = resp['course']
    for key in list(new_dict):
        if new_dict[key] == '':
            new_dict.pop(key, None)
    resp['course'] = new_dict

    return JsonResponse(resp)
