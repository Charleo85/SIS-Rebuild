from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import os
import hmac

from .models import *
from .forms import *
import settings


def success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)


def failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)


def login(request):
    if request.method != 'POST':
        return failure(400, 'incorrect request type')

    if 'username' not in request.POST:
        return failure(400, 'missing username')
    if 'password' not in request.POST:
        return failure(400, 'missing password')
    if 'user_type' not in request.POST:
        return failure(400, 'missing user type')

    username = request.POST['username']
    password = request.POST['password']
    user_type = int(request.POST['user_type'])

    if user_type == 0:
        try:
            user = Instructor.objects.get(username=username)
        except ObjectDoesNotExist:
            return failure(404, 'cannot find instructor')
    elif user_type == 1:
        try:
            user = Student.objects.get(username=username)
        except ObjectDoesNotExist:
            return failure(404, 'cannot find student')
    else:
        return failure(400, 'incorrect user type')

    if not hashers.check_password(password, user.password):
        return failure(403, 'incorrect password')

    token = hmac.new(
        key = settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256'
    ).hexdigest()

    auth = Authenticator(userid=username,auth=token,user_type=user_type)
    auth.save()

    data = model_to_dict(auth)
    return success(data, 'authenticator', 200)


def validate(request):
    if request.method != 'POST':
        return failure(400, 'incorrect request type')

    if 'auth' not in request.POST:
        return failure(400, 'missing authenticator')
    token = request.POST['auth']
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return failure(403, 'unknown authenticator')

    data = {}
    data['user_type'] = auth.user_type

    if auth.user_type == 0:
        ins = Instructor.objects.get(username=auth.userid)
        data['info'] = model_to_dict(ins)
    else:
        stud = Student.objects.get(username=auth.userid)
        data['info'] = model_to_dict(stud)

    data['info'].pop(username, None)
    data['info'].pop(password, None)
    return success(data, 'user', 200)


def logout(request):
    if request.method != 'POST':
        return failure(400, 'incorrect request type')

    if 'auth' not in request.POST:
        return failure(400, 'missing authenticator')
    token = request.POST['auth']
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return failure(403, 'unknown authenticator')
    
    Authenticator.objects.filter(auth=token).delete()
    return JsonResponse({ 'status_code': 200 })
