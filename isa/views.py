from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import requests, json

from .models import *
from .forms import *

def index(request):
    return render(request, 'home.html')


def course_detail(request, sisid):
    try:
        target_course = Course.objects.get(id=sisid)
    except ObjectDoesNotExist:
        raise Http404('Course does not exist')
    
    if request.method == 'GET':
        data = model_to_dict(target_course)
        data['instructor'] = target_course.instructor.__str__()
        return JsonResponse(data)
    elif request.method == 'POST':
        if request.POST.get('id') == sisid:
            form = CourseForm(request.POST, instance=target_course)
            if form.is_valid():
                form.save()
                return HttpResponse('Success')
        return HttpResponse('Failure')
    else:
        raise Http404('Not a correct request')


def course_form(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False
        
        if exist:
            form = CourseForm(request.POST, instance=target_course)
        else:
            form = CourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            url = '/course/' + str(form.cleaned_data['id']) + '/'
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        form = CourseForm()

    else:
        raise Http404('Not a correct request')

    return render(request, 'postform.html', {'form': form, 'model': 'Course'})


def course_create(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False
        
        if not exist:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Success')
        
        return HttpResponse('Failure')
    else:
        raise Http404('Not a correct request')

