from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *


def success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)


def failure(code):
    error = { 'status_code' : code }
    return JsonResponse(error)


def index(request):
    return HttpResponse("Success!")


def course_detail(request, sisid):
    try:
        target_course = Course.objects.get(id=sisid)
    except ObjectDoesNotExist:
        return failure(404)

    if request.method == 'GET':
        data = model_to_dict(target_course)
        data['instructor'] = target_course.instructor.__str__()
        return success(data, 'course', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == sisid:
            form = CourseForm(request.POST, instance=target_course)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data['instructor'] = data['instructor'].__str__()
                return success(data, 'course', 202)

    return failure(400)


def course_create(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        if not exist:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data['instructor'] = data['instructor'].__str__()
                return success(data, 'course', 201)

    return failure(400)


def instructor_detail(request, compid):
    try:
        ins = Instructor.objects.get(id=compid)
    except ObjectDoesNotExist:
        return failure(404)

    if request.method == 'GET':
        data = model_to_dict(ins)
        return success(data, 'instructor', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = InstructorForm(request.POST, instance=ins)
            if form.is_valid():
                form.save()
                return success(form.cleaned_data, 'instructor', 202)

    return failure(400)


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
                return success(form.cleaned_data, 'instructor', 201)

    return failure(400)


def student_detail(request, compid):
    try:
        stud = Student.objects.get(id=compid)
    except ObjectDoesNotExist:
        return failure(404)

    if request.method == 'GET':
        data = model_to_dict(stud)

        courses_result = []
        for course_id in data['taking_courses']:
            course_name = Course.objects.get(id=course_id).__str__()
            courses_result.append(course_name)
        data['taking_courses'] = courses_result

        return success(data, 'student', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = StudentForm(request.POST, instance=stud)
            if form.is_valid():
                form.save()
                return success(form.cleaned_data, 'student', 202)

    return failure(400)


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
                return success(form.cleaned_data, 'student', 201)

    return failure(400)


def enrollment_detail(request, enrid):
    try:
        enroll = Enrollment.objects.get(id=enrid)
    except ObjectDoesNotExist:
        return failure(404)

    if request.method == 'GET':
        data = model_to_dict(enroll)
        data['enroll_status'] = enroll.get_enroll_status_display()
        return success(data, 'enrollment', 200)

    elif request.method == 'POST':
        credential1 = (request.POST.get('student') == enroll.student.id)
        credential2 = (request.POST.get('course') == enroll.course.id)

        if credential1 and credential2:
            form = EnrollmentForm(request.POST, instance=enroll)
            if form.is_valid():
                form.save()

                data = form.cleaned_data
                data['student'] = data['student'].__str__()
                data['course'] = data['course'].__str__()
                data['enroll_status'] = enroll.get_enroll_status_display()

                return success(data, 'enrollment', 202)

    return failure(400)


def enrollment_create(request):
    if request.method == 'POST':
        exist = True
        try:
            enroll = Enrollment.objects.get(
                student=request.POST.get('student'),
                course=request.POST.get('course'),
            )
        except ObjectDoesNotExist:
            exist = False

        if not exist:
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                form.save()

                data = form.cleaned_data
                data['student'] = data['student'].__str__()
                data['course'] = data['course'].__str__()
                data['enroll_status'] = form.get_enroll_status_display()

                return success(data, 'enrollment', 201)

    return failure(400)
