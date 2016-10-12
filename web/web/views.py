from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import urllib.request
import json

from .forms import *


def home_page(request):
    req = urllib.request.Request('http://exp-api:8000/course/popular/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'homepage.html', resp)


def about(request):
    return render(request, 'about.html')


def list_item(request, modelname):
    req = urllib.request.Request('http://exp-api:8000/' + modelname + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, modelname + '.html', resp)


def item_detail(request, itemid, modelname):
    req = urllib.request.Request(
        'http://exp-api:8000/' + modelname + '/detail/' + itemid + '/'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, modelname + '_detail.html', resp)


def login(request, modelname):
    if request.method == 'GET':
        form = LoginForm()
        data = { 'form': form, 'modelname': modelname }
        return render(request, 'test_login.html', data)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            data = { 'form': form, 'modelname': modelname }
            return render(request, 'test_login.html', data)

        post_data = form.cleaned_data
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request(
            'http://exp-api:8000/' + modelname + '/login/',
            data=post_encoded, method='POST',
        )
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        if resp['status_code'] != 200:
            data = {
                'form': form, 'modelname': modelname,
                'error' : resp['error_message']
            }
            return render(request, 'test_login.html', data)

        authenticator = resp['auth']
        next = request.POST.get('next') or reverse(modelname + '_validate')
        response = HttpResponseRedirect(next)
        response.set_cookie('auth', authenticator)
        return response

    return HttpResponse('incorrect request type')


def get_user_info(request, user_type):
    if user_type == 0:
        modelname = 'instructor'
    else:
        modelname = 'student'

    if 'auth' not in request.COOKIES:
        return { 'status_code': 400 }

    auth = request.COOKIES.get('auth')
    post_data = {'auth': auth}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

    req = urllib.request.Request(
        'http://exp-api:8000/' + modelname + '/auth/validate/',
        data=post_encoded, method='POST'
    )
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp


def instructor_login_required(f):
    def wrap(request, *args, **kwargs):
        resp = get_user_info(request, 0)
        if resp['status_code'] != 200:
            return HttpResponseRedirect(reverse('instructor_login'))
        else:
            return f(request, *args, **kwargs)

    return wrap


def student_login_required(f):
    def wrap(request, *args, **kwargs):
        resp = get_user_info(request, 1)
        if resp['status_code'] != 200:
            return HttpResponseRedirect(reverse('student_login'))
        else:
            return f(request, *args, **kwargs)

    return wrap


@instructor_login_required
def instructor_validate(request):
    resp = get_user_info(request)
    last_name = resp['user']['last_name']
    return HttpResponse('You have logged in! Instructor ' + last_name)


@student_login_required
def student_validate(request):
    resp = get_user_info(request)
    last_name = resp['user']['last_name']
    return HttpResponse('You have logged in! Student ' + last_name)
