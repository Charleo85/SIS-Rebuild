from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import urllib.request
import json

from .forms import *


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


def _get_user_info(request, user_type):
    if user_type == 0:
        modelname = 'instructor'
    else:
        modelname = 'student'

    if 'auth' not in request.COOKIES:
        return { 'status_code': 400 }

    auth = request.COOKIES.get('auth')
    post_data = {'auth': auth}
    url = 'http://exp-api:8000/' + modelname + '/auth/validate/'
    resp = _make_post_request(url, post_data)
    return resp


def home_page(request):
    url = 'http://exp-api:8000/homepage/'
    resp = _make_get_request(url)
    return render(request, 'homepage.html', resp)


def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def list_item(request, modelname):
    url = 'http://exp-api:8000/' + modelname + '/'
    resp = _make_get_request(url)
    return render(request, modelname + '.html', resp)


def item_detail(request, itemid, modelname):
    url = 'http://exp-api:8000/' + modelname + '/detail/' + itemid + '/'
    resp = _make_get_request(url)
    return render(request, modelname + '_detail.html', resp)


def login(request, modelname):
    if 'auth' in request.COOKIES:
        if modelname == 'instructor':
            user_type = 0
        else:
            user_type = 1
        resp = _get_user_info(request, user_type)
        if resp['status_code'] == 200:
            return HttpResponseRedirect(reverse(modelname + '_validate'))

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
        url = 'http://exp-api:8000/' + modelname + '/auth/login/'
        resp = _make_post_request(url, post_data)

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


def instructor_login_required(f):
    def wrap(request, *args, **kwargs):
        resp = _get_user_info(request, 0)
        if resp['status_code'] != 200:
            return HttpResponseRedirect(reverse('instructor_login'))
        else:
            return f(request, *args, **kwargs)
    return wrap


def student_login_required(f):
    def wrap(request, *args, **kwargs):
        resp = _get_user_info(request, 1)
        if resp['status_code'] != 200:
            return HttpResponseRedirect(reverse('student_login'))
        else:
            return f(request, *args, **kwargs)
    return wrap


@instructor_login_required
def instructor_validate(request):
    resp = _get_user_info(request, 0)
    last_name = resp['user']['last_name']
    message = 'You have logged in! Instructor ' + last_name + '. '
    message += '<a href=\"/instructor/logout/\">Logout</a>'
    return HttpResponse(message)


@student_login_required
def student_validate(request):
    resp = _get_user_info(request, 1)
    last_name = resp['user']['last_name']
    message = 'You have logged in! Student ' + last_name + '. '
    message += '<a href=\"/student/logout/\">Logout</a>'
    return HttpResponse(message)


def logout(request, modelname):
    if 'auth' not in request.COOKIES:
        return HttpResponseRedirect(reverse(modelname + '_login'))

    url = 'http://exp-api:8000/' + modelname + '/auth/logout/'
    post_data = {'auth': request.COOKIES.get('auth')}
    resp = _make_post_request(url, post_data)

    if resp['status_code'] == 200:
        response = HttpResponse('You have successfully logged out.')
        response.delete_cookie('auth')
        return response
    else:
        return HttpResponseRedirect(reverse(modelname + '_login'))
