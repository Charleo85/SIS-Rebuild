import os, hmac, json, copy

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import View
from django.http import QueryDict
from django.db.models import Model
from django.forms import ModelForm

from .models import *
from .forms import *
import models.settings

from django.db.models import Q


def index(request):
    return HttpResponse('Success!\n')


def _success(code, data_dict={}):
    data_dict['status_code'] = code
    return JsonResponse(data_dict)


def _failure(code, msg=''):
    if msg == '': error = {'status_code' : code}
    else: error = {'status_code' : code, 'error_message' : msg}
    return JsonResponse(error)


class BaseView(View):
    model = Model
    form = ModelForm

    def get(self, request, *args, **kwargs):
        query = request.GET.dict()
<<<<<<< HEAD
        try:
            objs = self.model.objects.filter(**query)
            # {'name':'discrete math', 'department': 'cs'}
            # {'all' : true}
            # objs = self.model.objects.filter(name = 'discrete math', department = cs)

        except:
            return _failure(400, 'invalid parameters')
=======
        try: objs = self.model.objects.filter(**query)
        except: return _failure(400, 'invalid parameters')
>>>>>>> master

        dicts = []
        for obj in objs: dicts.append(model_to_dict(obj))
        if len(dicts) == 0: return _failure(404, 'no matches found')
        return _success(200, {'match': dicts})

    def post(self, request, *args, **kwargs):
        query = request.GET.dict()
        post_dict = request.POST.dict()
        if not post_dict:
            post_dict = json.loads(request.body.decode('utf-8'))
        if query: return self._update(query, post_dict)
        else: return self._create(post_dict)

    def delete(self, request, *args, **kwargs):
        query = request.GET.dict()
        if 'force' in query:
            force = query['force']
            query.pop('force', None)

        try: objs = self.model.objects.filter(**query)
        except: return _failure(400, 'invalid parameters')
        if len(objs) == 0: return _failure(404, 'no matches found')

        if not force and len(objs) > 1:
            msg = 'attempting to delete multiple objects, '
            msg += 'use force=true to force this deletion'
            return _failure(400, msg)

        objs.delete()
        return _success(204)

    def _create(self, post_dict, exclude=[]):
        f = self.form(post_dict)
        if not f.is_valid(): return _failure(400, 'invalid create info')

        filter_dict = copy.deepcopy(post_dict)
        for item in exclude: filter_dict.pop(item, None)
        try:
            if len(self.model.objects.filter(**filter_dict)) > 0:
                return _failure(409, 'object already exists')
        except:
            return _failure(400, 'invalid create info')

        obj = f.save()
        return _success(201, {'object_id': obj.id})

    def _update(self, get_dict, post_dict):
        try: objs = self.model.objects.filter(**get_dict)
        except: return _failure(400, 'invalid parameters')

        if len(objs) == 0: return _failure(404, 'no matches found')
        elif len(objs) > 1: return _failure(400, 'multiple objects')

        obj = objs[0]
        for key, value in post_dict.items(): setattr(obj, key, value)

        try: obj.save()
        except: return _failure(400, 'invalid update info')
        return _success(202, {'object_id': obj.id})


class CourseView(BaseView):
    model = Course
    form = CourseForm

    def get(self, request, *args, **kwargs):
        # Below code satisfies a multi-mnemonic search
        if 'mnemonic_list' in request.GET:
            mnemonic_querystring = request.GET.get('mnemonic_list')
            mnemonic_query_list = mnemonic_querystring.split(' ')

            all_courses = Course.objects.all()

            if len(mnemonic_query_list) == 0:
                return _failure(404, 'no matches found')
            elif len(mnemonic_query_list) == 1:
                correct_courses = all_courses.filter(mnemonic=mnemonic_query_list[0])
            else:
                q = Q(mnemonic=mnemonic_query_list[0])
                for mnemonic_query in mnemonic_query_list[1:]:
                    q = q.add(Q(mnemonic=mnemonic_query), Q.OR)

                correct_courses = all_courses.filter(q)

            course_dicts = []
            for course in correct_courses:
                course_dicts.append(model_to_dict(course))

            if len(course_dicts) == 0:
                return _failure(404, 'no matches found')
            else:
                for course_dictionary in course_dicts:
                    course_grade = Grade.objects.get(id=course_dictionary['grade'])
                    course_dictionary['grade'] = model_to_dict(course_grade)
            return _success(200, {'match': course_dicts})

        # If looking for single course detail (for course detail page), sections
        # are needed as well.
        elif 'mnemonic' and 'number' in request.GET:
            mnemonic = request.GET.get('mnemonic')
            number = request.GET.get('number')
            try:
                course = Course.ojects.get(mnemonic=mnemonic, number=number)
            except:
                return _failure(404, 'no matches found')

            course_dictionary = model_to_dict(course)

            course_grade = Grade.objects.get(id=course_dictionary['grade'])
            course_dictionary['grade'] = model_to_dict(course_grade)

            associated_sections = course.section_set.all()
            section_dicts = []
            for section in associated_sections:
                section_dicts.append(model_to_dict(section))

            course_dictionary['sections'] = section_dicts
            return _success(200, {'match': course_dictionary})

        # Tong's normal code
        else:
            resp = super().get(request, *args, **kwargs)
            resp_dict = json.loads(resp.content.decode('utf-8'))
            if resp_dict['status_code'] != 200:
                return resp
            resp_dict.pop('status_code', None)

            for obj_dict in resp_dict['match']:
                obj = Grade.objects.get(id=obj_dict['grade'])
                obj_dict['grade'] = model_to_dict(obj)
            return _success(200, resp_dict)


    def _create(self, post_dict):
        if 'grade' in post_dict:
            grade_dict = post_dict['grade']
            try: obj = Grade.objects.create(**grade_dict)
            except: return _failure(400, 'invalid create info')
            post_dict['grade'] = obj.id

        resp = super()._create(post_dict, ['grade'])
        resp_dict = json.loads(resp.content.decode('utf-8'))
        if resp_dict['status_code'] != 201:
            Grade.objects.filter(id=post_dict['grade']).delete()
        return resp

    def _update(self, get_dict, post_dict):
        grade_dict = {}
        if 'grade' in post_dict:
            grade_dict = post_dict['grade']
            post_dict.pop('grade', None)

        resp = super()._update(get_dict, post_dict)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        if resp_dict['status_code'] != 202: return resp

        obj = self.model.objects.get(**get_dict).grade
        if obj:
            for key, value in grade_dict.items():
                setattr(obj, key, value)
            try: obj.save()
            except: return _failure(400, 'invalid update info')
        else:
            try:
                obj = Grade.objects.create(**grade_dict)
                obj.save()
                course_obj = self.model.objects.get(**get_dict)
                course_obj.grade = obj
                course_obj.save()
            except: return _failure(400, 'invalid update info')

        return _success(202, {'object_id': resp_dict['object_id']})


#
#
# def course_detail(request, sisid):
#     try:
#         target_course = Course.objects.get(id=sisid)
#     except ObjectDoesNotExist:
#         return _failure(404)
#
#     if request.method == 'GET':
#         data = model_to_dict(target_course)
#         data['current_enrolled'] = len(target_course.student_set.all())
#         # This str function doesn't always work consistently!!
#         data['instructor'] = data['instructor'].__str__()
#         return _success(data, 'course', 200)
#
#     elif request.method == 'POST':
#         if request.POST.get('id') == sisid:
#             form = CourseForm(request.POST, instance=target_course)
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 data['current_enrolled'] = len(target_course.student_set.all())
#                 data['instructor'] = data['instructor'].__str__()
#                 return _success(data, 'course', 201)
#
#     return _failure(400)
#
#
# def course_create(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             target_course = Course.objects.get(id=request.POST.get('id'))
#         except (ObjectDoesNotExist, ValueError):
#             exist = False
#
#         if not exist:
#             form = CourseForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 #This str function doesn't always work consistently!!
#                 data['instructor'] = data['instructor'].__str__()
#                 data['current_enrolled'] = 0
#                 return _success(data, 'course', 201)
#
#     return _failure(400)
#
#
# def course_delete(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             target_course = Course.objects.get(id=request.POST.get('id'))
#         except (ObjectDoesNotExist, ValueError):
#             exist = False
#
#         if exist:
#             Enrollment.objects.filter(course=target_course).delete()
#             Course.objects.filter(id=request.POST.get('id')).delete()
#             return JsonResponse({ 'status_code': 202 })
#
#     return _failure(400)
#
#
# def course_all(request):
#     if request.method == 'GET':
#         courses = Course.objects.all()
#         course_list = []
#         for course in courses:
#             data = model_to_dict(course)
#             data['current_enrolled'] = len(course.student_set.all())
#             course_list.append(data)
#         return _success(course_list, 'all_courses', 200)
#
#     return _failure(400)
#
#
# def instructor_detail(request, compid):
#     try:
#         ins = Instructor.objects.get(id=compid)
#     except ObjectDoesNotExist:
#         return _failure(404)
#
#     if request.method == 'GET':
#         data = model_to_dict(ins)
#
#         teaching_courses = []
#         teaching = ins.course_set.all()
#         for course in teaching:
#             teaching_courses.append(course.__str__())
#         data['teaching_courses'] = teaching_courses
#
#         data.pop('username', None)
#         data.pop('password', None)
#
#         return _success(data, 'instructor', 200)
#
#     elif request.method == 'POST':
#         if request.POST.get('id') == compid:
#             form = InstructorForm(request.POST, instance=ins)
#
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 data.pop('username', None)
#                 data.pop('password', None)
#                 return _success(data, 'instructor', 202)
#
#     return _failure(400)
#
#
# def instructor_create(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             ins = Instructor.objects.get(id=request.POST.get('id'))
#         except ObjectDoesNotExist:
#             exist = False
#
#         if exist:
#             return _failure(400, 'instructor already exists')
#         else:
#             form = InstructorForm(request.POST)
#
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 data.pop('username', None)
#                 data.pop('password', None)
#                 return _success(data, 'instructor', 201)
#             else:
#                 return _failure(400, 'invalid input(s)')
#
#     return _failure(400, 'incorrect request type')
#
#
# def instructor_delete(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             ins = Instructor.objects.get(id=request.POST.get('id'))
#         except (ObjectDoesNotExist, ValueError):
#             exist = False
#
#         if exist:
#             courses = Course.objects.filter(instructor=ins)
#             for course in courses:
#                 Enrollment.objects.filter(course=course).delete()
#             courses.delete()
#             Instructor.objects.filter(id=request.POST.get('id')).delete()
#             return JsonResponse({ 'status_code': 202 })
#
#     return _failure(400)
#
#
# def instructor_all(request):
#     if request.method == 'GET':
#         instructors = Instructor.objects.all()
#         instructor_list = []
#
#         for ins in instructors:
#             data = model_to_dict(ins)
#             data.pop('username', None)
#             data.pop('password', None)
#             instructor_list.append(data)
#
#         return _success(instructor_list, 'all_instructors', 200)
#
#     return _failure(400)
#
#
# def student_detail(request, compid):
#     try:
#         stud = Student.objects.get(id=compid)
#     except ObjectDoesNotExist:
#         return _failure(404)
#
#     if request.method == 'GET':
#         data = model_to_dict(stud)
#         data.pop('username', None)
#         data.pop('password', None)
#         return _success(data, 'student', 200)
#
#     elif request.method == 'POST':
#         if request.POST.get('id') == compid:
#             form = StudentForm(request.POST, instance=stud)
#
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 data.pop('username', None)
#                 data.pop('password', None)
#                 return _success(data, 'student', 201)
#
#     return _failure(400)
#
#
# def student_create(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             stud = Student.objects.get(id=request.POST.get('id'))
#         except ObjectDoesNotExist:
#             exist = False
#
#         if exist:
#             return _failure(400, 'student already exists')
#         else:
#             form = StudentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 data = form.cleaned_data
#                 data.pop('username', None)
#                 data.pop('password', None)
#                 return _success(data, 'student', 201)
#             else:
#                 return _failure(400, 'invalid input(s)')
#
#     return _failure(400, 'incorrect request type')
#
#
# def student_delete(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             stud = Student.objects.get(id=request.POST.get('id'))
#         except (ObjectDoesNotExist, ValueError):
#             exist = False
#
#         if exist:
#             Enrollment.objects.filter(student=stud).delete()
#             Student.objects.filter(id=request.POST.get('id')).delete()
#             return JsonResponse({ 'status_code': 202 })
#
#     return _failure(400)
#
#
# def student_all(request):
#     if request.method == 'GET':
#         students = Student.objects.all()
#         student_list = []
#
#         for stud in students:
#             data = model_to_dict(stud)
#             data.pop('username', None)
#             data.pop('password', None)
#             student_list.append(data)
#
#         return _success(student_list, 'all_students', 200)
#
#     return _failure(400)
#
#
# def enrollment_detail(request, enrid):
#     try:
#         enroll = Enrollment.objects.get(id=enrid)
#     except ObjectDoesNotExist:
#         return _failure(404)
#
#     if request.method == 'GET':
#         data = model_to_dict(enroll)
#         data['enroll_status'] = enroll.get_enroll_status_display()
#         return _success(data, 'enrollment', 200)
#
#     elif request.method == 'POST':
#         credential1 = (request.POST.get('student') == enroll.student.id)
#         credential2 = (request.POST.get('course') == enroll.course.id)
#
#         if credential1 and credential2:
#             form = EnrollmentForm(request.POST, instance=enroll)
#             if form.is_valid():
#                 form.save()
#                 enroll = Enrollment.objects.get(
#                     student=request.POST.get('student'),
#                     course=request.POST.get('course'),
#                 )
#                 data = model_to_dict(enroll)
#                 data['enroll_status'] = enroll.get_enroll_status_display()
#                 return _success(data, 'enrollment', 202)
#
#     return _failure(400)
#
#
# def enrollment_create(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             enroll = Enrollment.objects.get(
#                 student=request.POST.get('student'),
#                 course=request.POST.get('course'),
#             )
#         except ObjectDoesNotExist:
#             exist = False
#
#         if not exist:
#             form = EnrollmentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 enroll = Enrollment.objects.get(
#                     student=request.POST.get('student'),
#                     course=request.POST.get('course'),
#                 )
#                 data = model_to_dict(enroll)
#                 data['enroll_status'] = enroll.get_enroll_status_display()
#                 return _success(data, 'enrollment', 201)
#
#     return _failure(400)
#
#
# def enrollment_delete(request):
#     if request.method == 'POST':
#         exist = True
#         try:
#             enr = Enrollment.objects.get(id=request.POST.get('id'))
#         except (ObjectDoesNotExist, ValueError):
#             exist = False
#
#         if exist:
#             Enrollment.objects.filter(id=request.POST.get('id')).delete()
#             return JsonResponse({ 'status_code': 202 })
#
#     return _failure(400)
#
#
# def enrollment_all(request):
#     if request.method == 'GET':
#         enrollments = Enrollment.objects.all()
#         enrollment_list = []
#         for enr in enrollments:
#             data = model_to_dict(enr)
#             data['enroll_status'] = enr.get_enroll_status_display()
#             enrollment_list.append(data)
#         return _success(enrollment_list, 'all_enrollments', 200)
#
#     return _failure(400)
#
# def login(request):
#     if request.method != 'POST':
#         return _failure(400, 'incorrect request type')
#
#     if 'username' not in request.POST:
#         return _failure(400, 'missing username')
#     if 'password' not in request.POST:
#         return _failure(400, 'missing password')
#     if 'user_type' not in request.POST:
#         return _failure(400, 'missing user type')
#
#     username = request.POST['username']
#     password = request.POST['password']
#     user_type = int(request.POST['user_type'])
#
#     if user_type == 0:
#         try:
#             user = Instructor.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return _failure(404, 'cannot find instructor')
#     elif user_type == 1:
#         try:
#             user = Student.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return _failure(404, 'cannot find student')
#     else:
#         return _failure(400, 'incorrect user type')
#
#     if not hashers.check_password(password, user.password):
#         return _failure(403, 'incorrect password')
#
#     token = hmac.new(
#         key = models.settings.SECRET_KEY.encode('utf-8'),
#         msg = os.urandom(32),
#         digestmod = 'sha256'
#     ).hexdigest()
#
#     auth = Authenticator(userid=username,auth=token,user_type=user_type)
#     auth.save()
#
#     data = model_to_dict(auth)
#     return _success(data, 'authenticator', 200)
#
#
# def record_coview(request):
#     if request.method != 'POST':
#         return _failure(400, 'incorrect request type')
#
#     if 'auth' not in request.POST:
#         return _failure(400, 'missing authenticator')
#     token = request.POST['auth']
#     try:
#         auth = Authenticator.objects.get(auth=token)
#     except ObjectDoesNotExist:
#         return _failure(403, 'unknown authenticator')
#
#     data = {}
#     data['user_type'] = auth.user_type
#
#     if auth.user_type == 0:
#         ins = Instructor.objects.get(username=auth.userid)
#         userid = ins.id
#     else:
#         stud = Student.objects.get(username=auth.userid)
#         userid = stud.id
#
#     item_model = request.POST['modelname']
#     item_id = request.POST['itemid']
#
#     # Output to courseviews file
#     if(item_model=='course'):
#         string_for_courseviews_file = userid + ',' + item_id + '\n'
#         f = open('/tmp/data/inputs/courselog.in', 'a')
#         f.write(string_for_courseviews_file)
#         f.close()
#     # Output to courseviews file
#     elif(item_model=='instructor'):
#         string_for_instructorviews_file = userid + ',' + item_id + '\n'
#         f = open('/tmp/data/inputs/instructorlog.in', 'a')
#         f.write(string_for_instructorviews_file)
#         f.close()
#
#     correct = {'status_code': 200}
#     return JsonResponse(correct)
#
#
#
# def validate(request):
#     if request.method != 'POST':
#         return _failure(400, 'incorrect request type')
#
#     if 'auth' not in request.POST:
#         return _failure(400, 'missing authenticator')
#     token = request.POST['auth']
#     try:
#         auth = Authenticator.objects.get(auth=token)
#     except ObjectDoesNotExist:
#         return _failure(403, 'unknown authenticator')
#
#     data = {}
#     data['user_type'] = auth.user_type
#
#     if auth.user_type == 0:
#         ins = Instructor.objects.get(username=auth.userid)
#         data['info'] = model_to_dict(ins)
#         teaching_courses = []
#         for course in ins.course_set.all():
#             teaching_courses.append(course.__str__())
#         data['info']['teaching_courses'] = teaching_courses
#     else:
#         stud = Student.objects.get(username=auth.userid)
#         data['info'] = model_to_dict(stud)
#         taking_courses = []
#         for course in stud.taking_courses.all():
#             taking_courses.append(course.__str__())
#         data['info']['taking_courses'] = taking_courses
#
#     data['info'].pop('password', None)
#     return _success(data, 'user', 200)
#
#
# def logout(request):
#     if request.method != 'POST':
#         return _failure(400, 'incorrect request type')
#
#     if 'auth' not in request.POST:
#         return _failure(400, 'missing authenticator')
#     token = request.POST['auth']
#     try:
#         auth = Authenticator.objects.get(auth=token)
#     except ObjectDoesNotExist:
#         return _failure(403, 'unknown authenticator')
#
#     Authenticator.objects.filter(auth=token).delete()
#     return JsonResponse({ 'status_code': 200 })
