from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import os
import hmac

from .models import *
from .forms import *
import models.settings


def _success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)


def _failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)


def login(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    if 'username' not in request.POST:
        return _failure(400, 'missing username')
    if 'password' not in request.POST:
        return _failure(400, 'missing password')
    if 'user_type' not in request.POST:
        return _failure(400, 'missing user type')

    username = request.POST['username']
    password = request.POST['password']
    user_type = int(request.POST['user_type'])

    if user_type == 0:
        try:
            user = Instructor.objects.get(username=username)
        except ObjectDoesNotExist:
            return _failure(404, 'cannot find instructor')
    elif user_type == 1:
        try:
            user = Student.objects.get(username=username)
        except ObjectDoesNotExist:
            return _failure(404, 'cannot find student')
    else:
        return _failure(400, 'incorrect user type')

    if not hashers.check_password(password, user.password):
        return _failure(403, 'incorrect password')

    token = hmac.new(
        key = models.settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256'
    ).hexdigest()

    auth = Authenticator(userid=username,auth=token,user_type=user_type)
    auth.save()

    data = model_to_dict(auth)
    return _success(data, 'authenticator', 200)


def record_coview(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    if 'auth' not in request.POST:
        return _failure(400, 'missing authenticator')
    token = request.POST['auth']
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return _failure(403, 'unknown authenticator')

    data = {}
    data['user_type'] = auth.user_type

    if auth.user_type == 0:
        ins = Instructor.objects.get(username=auth.userid)
        userid = ins.id
    else:
        stud = Student.objects.get(username=auth.userid)
        userid = stud.id

    item_model = request.POST['modelname']
    item_id = request.POST['itemid']

    # Output to courseviews file
    if(item_model=='course'):
        string_for_courseviews_file = userid + ',' + item_id + '\n'
        f = open('/tmp/data/inputs/courselog.in', 'a')
        f.write(string_for_courseviews_file)
        f.close()
    # Output to courseviews file
    elif(item_model=='instructor'):
        string_for_instructorviews_file = userid + ',' + item_id + '\n'
        f = open('/tmp/data/inputs/instructorlog.in', 'a')
        f.write(string_for_instructorviews_file)
        f.close()

    correct = {'status_code': 200}
    return JsonResponse(correct)



def validate(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    if 'auth' not in request.POST:
        return _failure(400, 'missing authenticator')
    token = request.POST['auth']
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return _failure(403, 'unknown authenticator')

    data = {}
    data['user_type'] = auth.user_type

    if auth.user_type == 0:
        ins = Instructor.objects.get(username=auth.userid)
        data['info'] = model_to_dict(ins)
        teaching_courses = []
        for course in ins.course_set.all():
            teaching_courses.append(course.__str__())
        data['info']['teaching_courses'] = teaching_courses
    else:
        stud = Student.objects.get(username=auth.userid)
        data['info'] = model_to_dict(stud)
        taking_courses = []
        for course in stud.taking_courses.all():
            taking_courses.append(course.__str__())
        data['info']['taking_courses'] = taking_courses

    data['info'].pop('password', None)
    return _success(data, 'user', 200)


def logout(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    if 'auth' not in request.POST:
        return _failure(400, 'missing authenticator')
    token = request.POST['auth']
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return _failure(403, 'unknown authenticator')

    Authenticator.objects.filter(auth=token).delete()
    return JsonResponse({ 'status_code': 200 })
