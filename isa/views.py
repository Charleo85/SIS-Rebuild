from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import requests, json

from .models import *
from .forms import *

def index(request):
    return render(request, 'home.html')


def course_detail(request, mne, num, sec):
    try:
        target_course = Course.objects.get(
            mnemonic=mne.upper(),
            number=num,
            section=sec,
        )
    except ObjectDoesNotExist:
        raise Http404('Class does not exist')
    
    if request.method == 'GET':
        data = model_to_dict(target_course)
        data['instructor'] = target_course.instructor.__str__()
        return JsonResponse(data)
    else:
        raise Http404('Not a correct request')


def course_form(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(
                mnemonic=request.POST.get('mnemonic'),
                number=request.POST.get('number'),
                section=request.POST.get('section'),
            )
        except ObjectDoesNotExist:
            exist = False
        
        if exist:
            form = CourseForm(request.POST, instance=target_course)
        else:
            form = CourseForm(request.POST)
        
        if form.is_valid():
            form.save()
            url = '/course/' + form.cleaned_data['mnemonic'] + '/'
            url += form.cleaned_data['number'] + '/'
            url += form.cleaned_data['section'] + '/'
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        form = CourseForm()

    else:
        raise Http404('Not a correct request')

    return render(request, 'course.html', {'form': form})

