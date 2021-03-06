from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *


def _success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)


def _failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)


def index(request):
    return HttpResponse("Success!")


def course_detail(request, sisid):
    try:
        target_course = Course.objects.get(id=sisid)
    except ObjectDoesNotExist:
        return _failure(404)

    if request.method == 'GET':
        data = model_to_dict(target_course)
        data['current_enrolled'] = len(target_course.student_set.all())
        # This str function doesn't always work consistently!!
        data['instructor'] = data['instructor'].__str__()
        return _success(data, 'course', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == sisid:
            form = CourseForm(request.POST, instance=target_course)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data['current_enrolled'] = len(target_course.student_set.all())
                data['instructor'] = data['instructor'].__str__()
                return _success(data, 'course', 201)

    return _failure(400)


def course_create(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        status_code = 401
        if not exist:
            form = CourseForm(request.POST)
            status_code = 402
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                #This str function doesn't always work consistently!!
                data['instructor'] = data['instructor'].__str__()
                data['current_enrolled'] = 0
                return _success(data, 'course', 201)

    return _failure(status_code)


def course_delete(request):
    if request.method == 'POST':
        exist = True
        try:
            target_course = Course.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        if exist:
            Enrollment.objects.filter(course=target_course).delete()
            Course.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({ 'status_code': 202 })

    return _failure(400)


def course_all(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        course_list = []
        for course in courses:
            data = model_to_dict(course)
            data['current_enrolled'] = len(course.student_set.all())
            course_list.append(data)
        return _success(course_list, 'all_courses', 200)

    return _failure(400)


def instructor_detail(request, compid):
    try:
        ins = Instructor.objects.get(id=compid)
    except ObjectDoesNotExist:
        return _failure(404)

    if request.method == 'GET':
        data = model_to_dict(ins)

        teaching_courses = []
        teaching = ins.course_set.all()
        for course in teaching:
            teaching_courses.append(course.__str__())
        data['teaching_courses'] = teaching_courses

        data.pop('username', None)
        data.pop('password', None)

        return _success(data, 'instructor', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = InstructorForm(request.POST, instance=ins)

            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data.pop('username', None)
                data.pop('password', None)
                return _success(data, 'instructor', 202)

    return _failure(400)


def instructor_create(request):
    if request.method == 'POST':
        exist = True
        try:
            ins = Instructor.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if exist:
            return _failure(400, 'instructor already exists')
        else:
            form = InstructorForm(request.POST)

            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data.pop('username', None)
                data.pop('password', None)
                return _success(data, 'instructor', 201)
            else:
                return _failure(400, 'invalid input(s)')

    return _failure(400, 'incorrect request type')


def instructor_delete(request):
    if request.method == 'POST':
        exist = True
        try:
            ins = Instructor.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        if exist:
            courses = Course.objects.filter(instructor=ins)
            for course in courses:
                Enrollment.objects.filter(course=course).delete()
            courses.delete()
            Instructor.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({ 'status_code': 202 })

    return _failure(400)


def instructor_all(request):
    if request.method == 'GET':
        instructors = Instructor.objects.all()
        instructor_list = []

        for ins in instructors:
            data = model_to_dict(ins)
            data.pop('username', None)
            data.pop('password', None)
            instructor_list.append(data)

        return _success(instructor_list, 'all_instructors', 200)

    return _failure(400)


def student_detail(request, compid):
    try:
        stud = Student.objects.get(id=compid)
    except ObjectDoesNotExist:
        return _failure(404)

    if request.method == 'GET':
        data = model_to_dict(stud)
        data.pop('username', None)
        data.pop('password', None)
        return _success(data, 'student', 200)

    elif request.method == 'POST':
        if request.POST.get('id') == compid:
            form = StudentForm(request.POST, instance=stud)

            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data.pop('username', None)
                data.pop('password', None)
                return _success(data, 'student', 201)

    return _failure(400)


def student_create(request):
    if request.method == 'POST':
        exist = True
        try:
            stud = Student.objects.get(id=request.POST.get('id'))
        except ObjectDoesNotExist:
            exist = False

        if exist:
            return _failure(400, 'student already exists')
        else:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                data.pop('username', None)
                data.pop('password', None)
                return _success(data, 'student', 201)
            else:
                return _failure(400, 'invalid input(s)')

    return _failure(400, 'incorrect request type')


def student_delete(request):
    if request.method == 'POST':
        exist = True
        try:
            stud = Student.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        if exist:
            Enrollment.objects.filter(student=stud).delete()
            Student.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({ 'status_code': 202 })

    return _failure(400)


def student_all(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_list = []

        for stud in students:
            data = model_to_dict(stud)
            data.pop('username', None)
            data.pop('password', None)
            student_list.append(data)

        return _success(student_list, 'all_students', 200)

    return _failure(400)


def enrollment_detail(request, enrid):
    try:
        enroll = Enrollment.objects.get(id=enrid)
    except ObjectDoesNotExist:
        return _failure(404)

    if request.method == 'GET':
        data = model_to_dict(enroll)
        data['enroll_status'] = enroll.get_enroll_status_display()
        return _success(data, 'enrollment', 200)

    elif request.method == 'POST':
        credential1 = (request.POST.get('student') == enroll.student.id)
        credential2 = (request.POST.get('course') == enroll.course.id)

        if credential1 and credential2:
            form = EnrollmentForm(request.POST, instance=enroll)
            if form.is_valid():
                form.save()
                enroll = Enrollment.objects.get(
                    student=request.POST.get('student'),
                    course=request.POST.get('course'),
                )
                data = model_to_dict(enroll)
                data['enroll_status'] = enroll.get_enroll_status_display()
                return _success(data, 'enrollment', 202)

    return _failure(400)


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
                enroll = Enrollment.objects.get(
                    student=request.POST.get('student'),
                    course=request.POST.get('course'),
                )
                data = model_to_dict(enroll)
                data['enroll_status'] = enroll.get_enroll_status_display()
                return _success(data, 'enrollment', 201)

    return _failure(400)


def enrollment_delete(request):
    if request.method == 'POST':
        exist = True
        try:
            enr = Enrollment.objects.get(id=request.POST.get('id'))
        except (ObjectDoesNotExist, ValueError):
            exist = False

        if exist:
            Enrollment.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({ 'status_code': 202 })

    return _failure(400)


def enrollment_all(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        enrollment_list = []
        for enr in enrollments:
            data = model_to_dict(enr)
            data['enroll_status'] = enr.get_enroll_status_display()
            enrollment_list.append(data)
        return _success(enrollment_list, 'all_enrollments', 200)

    return _failure(400)
