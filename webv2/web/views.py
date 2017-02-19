from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import urllib.request
import json
import requests


from .forms import *

# Version 2 Code
########################


def home_page(request):
    # url = 'http://exp-api:8000/homepage/'
    # resp = _make_get_request(url)
    return render(request, 'homepage.html')


def about(request):
    return render(request, 'about.html')


def department_view(request, specific_department):
    url = 'http://exp-api:8000/department/' + specific_department
    response_dict = (requests.get(url)).json()
    response_dict['department'] = specific_department
    return render(request, 'department.html', response_dict)


def course_detail(request, mnemonic, number):
    url = 'http://exp-api:8000/course/' + mnemonic + number + '/'
    response_dict = (requests.get(url)).json()
    return render(request, 'course_detail.html', mnemonic, number)


# Is this necessary?
def mnemonic_view(request, mnemonic):
    pass


# Version 1 Code (Here for reference)
#########################
#
# def _make_get_request(url):
#     req = urllib.request.Request(url)
#     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
#     resp = json.loads(resp_json)
#     return resp
#
#
# def _make_post_request(url, post_data):
#     post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
#     req = urllib.request.Request(url, data=post_encoded, method='POST')
#     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
#     resp = json.loads(resp_json)
#     return resp
#
#
# def _get_user_info(request, user_type):
#     if user_type == 0:
#         modelname = 'instructor'
#     else:
#         modelname = 'student'
#
#     auth = request.COOKIES.get('auth')
#     post_data = {'auth': auth}
#     url = 'http://exp-api:8000/' + modelname + '/auth/validate/'
#     resp = _make_post_request(url, post_data)
#     return resp
#
#
# def instructor_login_required(f):
#     def wrap(request, *args, **kwargs):
#         resp = _get_user_info(request, 0)
#         if resp['status_code'] != 200:
#             url = reverse('instructor_login') + '?next=' + request.path
#             return HttpResponseRedirect(url)
#         else:
#             return f(request, *args, **kwargs)
#     return wrap
#
#
# def student_login_required(f):
#     def wrap(request, *args, **kwargs):
#         resp = _get_user_info(request, 1)
#         if resp['status_code'] != 200:
#             url = reverse('student_login') + '?next=' + request.path
#             return HttpResponseRedirect(url)
#         else:
#             return f(request, *args, **kwargs)
#     return wrap
#
# def list_item(request, modelname):
#     url = 'http://exp-api:8000/' + modelname + '/'
#     resp = _make_get_request(url)
#     return render(request, modelname + '.html', resp)
#
#
# def item_detail(request, itemid, modelname):
#     url = 'http://exp-api:8000/' + modelname + '/detail/' + itemid + '/'
#     resp = _make_get_request(url)
#
#     # If item detail is successfully retrieved and if
#     # authenticator cookie exists (a user is logged in) send item info and authenticator
#     # to exp -> models layer so that it can be logged for later usage by Spark
#     if resp['status_code'] == 200:
#         if 'auth' in request.COOKIES.keys():
#             auth = request.COOKIES.get('auth')
#             post_data = {'auth': auth, 'itemid': itemid, 'modelname': modelname}
#             url = 'http://exp-api:8000/auth/record_co-view/'
#             trash = _make_post_request(url, post_data)
#
#     return render(request, modelname + '_detail.html', resp)
#
#
# def login(request, modelname):
#     if 'auth' in request.COOKIES:
#         resp = _get_user_info(request, 0)
#         if resp['status_code'] == 200:
#             return HttpResponseRedirect(reverse('instructor_profile'))
#         resp = _get_user_info(request, 1)
#         if resp['status_code'] == 200:
#             return HttpResponseRedirect(reverse('student_profile'))
#
#         response = HttpResponseRedirect(reverse(modelname + '_login'))
#         response.delete_cookie('auth')
#         return response
#
#     if request.method == 'GET':
#         return render(request, 'login.html', {'modelname': modelname})
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if not form.is_valid():
#             error_msg = 'invalid input(s)'
#             data = { 'modelname': modelname, 'error': error_msg }
#             return render(request, 'login.html', data)
#
#         post_data = form.cleaned_data
#         url = 'http://exp-api:8000/' + modelname + '/auth/login/'
#         resp = _make_post_request(url, post_data)
#
#         if resp['status_code'] != 200:
#             data = {'modelname': modelname, 'error': resp['error_message']}
#             return render(request, 'login.html', data)
#
#         authenticator = resp['auth']
#         next = request.GET.get('next') or reverse(modelname + '_profile')
#         response = HttpResponseRedirect(next)
#         response.set_cookie('auth', authenticator)
#         return response
#
#     return HttpResponse('incorrect request type')
#
#
# def signup(request, modelname):
#     if request.method == 'GET':
#         return render(request, 'signup.html', {'modelname': modelname})
#
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if not form.is_valid():
#             error_msg = 'invalid input(s)'
#             data = { 'modelname': modelname, 'error': error_msg }
#             return render(request, 'signup.html', data)
#
#         if not form.is_good_password():
#             error_msg = 'please enter a stronger password'
#             data = { 'modelname': modelname, 'error': error_msg }
#             return render(request, 'signup.html', data)
#
#         if not form.password_match():
#             error_msg = 'passwords do not match'
#             data = { 'modelname': modelname, 'error': error_msg }
#             return render(request, 'signup.html', data)
#
#         post_data = form.cleaned_data
#         url = 'http://exp-api:8000/' + modelname + '/signup/'
#         resp = _make_post_request(url, post_data)
#
#         if resp['status_code'] != 201:
#             data = {'modelname': modelname, 'error': resp['error_message']}
#             return render(request, 'signup.html', data)
#
#         data = {'title': 'Congratulations!'}
#         data['message'] = 'You have successfully signed up. Please '
#         data['message'] += '<a href=\"/' + modelname + '/login/\">login</a>'
#         return render(request, 'info.html', data)
#
#     return HttpResponse('incorrect request type')
#
#
# @instructor_login_required
# def instructor_profile(request):
#     resp = _get_user_info(request, 0)
#     data = {}
#     data['status_code'] = resp['status_code']
#     data['instructor'] = resp['user']
#     return render(request, 'instructor_profile.html', data)
#
#
# @student_login_required
# def student_profile(request):
#     resp = _get_user_info(request, 1)
#     data = {}
#     data['status_code'] = resp['status_code']
#     data['student'] = resp['user']
#     return render(request, 'student_profile.html', data)
#
#
# def logout(request, modelname):
#     if 'auth' not in request.COOKIES:
#         return HttpResponseRedirect(reverse(modelname + '_login'))
#
#     url = 'http://exp-api:8000/' + modelname + '/auth/logout/'
#     post_data = {'auth': request.COOKIES.get('auth')}
#     resp = _make_post_request(url, post_data)
#
#     if resp['status_code'] == 200:
#         data = { 'title': 'Thank you!' }
#         data['message'] = 'You have successfully logged out.'
#         response = render(request, 'info.html', data)
#         response.delete_cookie('auth')
#         return response
#     else:
#         return HttpResponseRedirect(reverse(modelname + '_login'))
#
#
# @instructor_login_required
# def create_course_listing(request, modelname):
#     if request.method == 'GET':
#         form = NewCourseForm()
#         return render(request, "course_create.html", {'form': form})
#
#     url = 'http://exp-api:8000/' + modelname + '/create/'
#     form = NewCourseForm(request.POST)
#     if form.is_valid():
#         post_data = form.cleaned_data
#         response = _make_post_request(url, post_data)
#         if response['status_code'] == 400:
#             render_data = {
#                 'form': form,
#                 'error_message': response['error_message'],
#             }
#             return render(request, "course_create.html", render_data)
#         elif response['status_code'] == 201: #Success!
#             redirect_url = reverse(
#                 'course_detail',
#                 kwargs={'itemid': response['course']['id']},
#             )
#             return HttpResponseRedirect(redirect_url)
#
#     # failure due to invalid form input(s)
#     render_data = {'form': form, 'error_message': 'invalid input(s)'}
#     return render(request, "course_create.html", render_data)
#
#
# def search_page(request):
#     if request.method == 'GET':
#         form = SearchForm()
#         return render(request, "search_page.html", {'form': form})
#
#     data = request.POST.dict()
#     if 'query_specifier' not in data.keys():
#         data['query_specifier'] = 'general'
#
#     form = SearchForm(data)
#     if form.is_valid():
#         url = 'http://exp-api:8000/search/'
#         post_data = form.cleaned_data
#         resp = _make_post_request(url, post_data)
#
#         if resp['status_code'] != 200:
#             render_data = {'form': form, 'error_message': resp['error_msg']}
#             return render(request, 'search_page.html', render_data)
#         if resp['size'] == 0:
#             render_data = {'form': form, 'error_message': 'no results found'}
#             return render(request, "search_page.html", render_data)
#         else:
#             render_data = {'form': form, 'results': resp}
#             return render(request, "search_result.html", render_data)
