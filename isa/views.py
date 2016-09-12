from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

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

    return render(request, 'postform.html', {'form': form, 'model': 'course'})


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


def instructor_detail(request, compid):
    try:
        ins = Instructor.objects.get(id=compid)
    except ObjectDoesNotExist:
        raise Http404('Instructor does not exist')

    if request.method == 'GET':
        data = model_to_dict(ins)
        return JsonResponse(data)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = InstructorForm(request.POST, instance=ins)

            if form.is_valid():
                form.save()
                return HttpResponse('Success')

        return HttpResponse('Failure')

    else:
        raise Http404('Not a correct request')


def instructor_form(request):
    if request.method == 'POST':
        exist = True
        try:
            ins = Instructor.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if exist:
            form = InstructorForm(request.POST, instance=ins)
        else:
            form = InstructorForm(request.POST)

        if form.is_valid():
            form.save()
            url = '/instructor/' + str(form.cleaned_data['id']) + '/'
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        form = InstructorForm()

    else:
        raise Http404('Not a correct request')

    return render(request, 'postform.html', {'form': form, 'model': 'instructor'})


def instructor_create(request):
    if request.method == 'POST':
        exist = True
        try:
            ins = Instructor.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if not exist:
            form = InstructorForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Success')

        return HttpResponse('Failure')

    else:
        raise Http404('Not a correct request')


def student_detail(request, compid):
    try:
        stud = Student.objects.get(id=compid)
    except ObjectDoesNotExist:
        raise Http404('Student does not exist')

    if request.method == 'GET':
        data = model_to_dict(stud)
        return JsonResponse(data)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = StudentForm(request.POST, instance=stud)

            if form.is_valid():
                form.save()
                return HttpResponse('Success')

        return HttpResponse('Failure')

    else:
        raise Http404('Not a correct request')


def student_form(request):
    if request.method == 'POST':
        exist = True
        try:
            stud = Student.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if exist:
            form = StudentForm(request.POST, instance=stud)
        else:
            form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            url = '/student/' + str(form.cleaned_data['id']) + '/'
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        form = StudentForm()

    else:
        raise Http404('Not a correct request')

    return render(request, 'postform.html', {'form': form, 'model': 'student'})


def student_create(request):
    if request.method == 'POST':
        exist = True
        try:
            stud = Student.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if not exist:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Success')

        return HttpResponse('Failure')

    else:
        raise Http404('Not a correct request')


def enrollment_form(request):
    if request.method == 'POST':
        exist = True
        try:
            enroll = Enrollment.objects.get(
                student=request.POST.get('student'),
                course=request.POST.get('course'),
            )
        except ObjectDoesNotExist:
            exist = False

        if exist:
            form = EnrollmentForm(request.POST, instance=enroll)
        else:
            form = EnrollmentForm(request.POST)

        if form.is_valid():
            form.save()
            url = '/student/' + str(form.cleaned_data['student'].id) + '/'
            return HttpResponseRedirect(url)

    elif request.method == 'GET':
        form = EnrollmentForm()

    else:
        raise Http404('Not a correct request')

    return render(request, 'postform.html', {'form': form, 'model': 'enrollment'})
