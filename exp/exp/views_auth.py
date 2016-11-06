from django.http import JsonResponse, HttpResponse
from kafka import KafkaProducer

import urllib.request
import urllib.parse
import json


def _make_post_request(url, post_data):
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp


def _failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)


def login(request, user_type):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    post_data['user_type'] = user_type
    url = 'http://models-api:8000/api/auth/login/'
    resp = _make_post_request(url, post_data)

    if resp['status_code'] == 200:
        data = {}
        data['status_code'] = resp['status_code']
        data['auth'] = resp['authenticator']['auth']
        return JsonResponse(data)
    else:
        return _failure(resp['status_code'], resp['error_message'])


def validate(request, user_type):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    url = 'http://models-api:8000/api/auth/validate/'
    resp = _make_post_request(url, post_data)

    if resp['status_code'] == 200:
        if user_type == resp['user']['user_type']:
            resp['user'] = resp['user']['info']

            if user_type == 0:
                msg = ""
                for i in range(len(resp['user']['teaching_courses'])):
                    msg += resp['user']['teaching_courses'][i]
                    if i != len(resp['user']['teaching_courses']) - 1:
                        msg += ', '
                resp['user']['teaching_courses'] = msg
                if msg == "":
                    resp['user'].pop('teaching_courses', None)
            else:
                msg = ""
                for i in range(len(resp['user']['taking_courses'])):
                    msg += resp['user']['taking_courses'][i]
                    if i != len(resp['user']['taking_courses']) - 1:
                        msg += ', '
                resp['user']['taking_courses'] = msg
                if msg == "":
                    resp['user'].pop('taking_courses', None)

            return JsonResponse(resp)

        else:
            return _failure(400, 'incorrect user type')

    else:
        return _failure(resp['status_code'], resp['error_message'])


def logout(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    url = 'http://models-api:8000/api/auth/logout/'
    resp = _make_post_request(url, post_data)
    return JsonResponse(resp)


def signup(request, user_type):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.POST.dict()
    post_data.pop('password_again', None)

    if user_type == 0:
        modelname = 'instructor'
    else:
        modelname = 'student'
    url = 'http://models-api:8000/api/' + modelname + '/create/'
    resp = _make_post_request(url, post_data)

    if resp['status_code'] != 201:
        return _failure(resp['status_code'], resp['error_message'])
    else:
        # Push the new instructor/student listing into Kafka
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        new_dict = {}
        if user_type == 0:
            model_field = 'api.Instructor'
        else:
            model_field = 'api.Student'
        new_dict['model'] = model_field
        new_dict['fields'] = post_data
        new_dict['fields'].pop('password', None)
        producer.send('new-listings-topic', json.dumps(new_dict).encode('utf-8'))

        return JsonResponse({ 'status_code' : 201 })
