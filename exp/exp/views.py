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
    return JsonResponse(resp)


def course_detail(request, sisid):
    req = urllib.request.Request('http://models-api:8000/api/course/' + sisid + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
