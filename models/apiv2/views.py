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
        try:
            objs = self.model.objects.filter(**query)
            # {'name':'discrete math', 'department': 'cs'}
            # {'all' : true}
            # objs = self.model.objects.filter(name = 'discrete math', department = cs)

        except:
            return _failure(400, 'Invalid Parameters')


        dicts = []
        for obj in objs: dicts.append(model_to_dict(obj))
        if len(dicts) == 0: return _failure(404, 'No Matches Found')
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
        except: return _failure(400, 'Invalid Parameters')
        if len(objs) == 0: return _failure(404, 'No Matches Found')

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
        # Below code satisfies a multi-mnemonic search (e.g for department search)
        if 'mnemonic_list' in request.GET:
            mnemonic_querystring = request.GET.get('mnemonic_list')
            mnemonic_query_list = mnemonic_querystring.split(' ')

            all_courses = Course.objects.all()

            if len(mnemonic_query_list) == 0:
                return _failure(404, 'No Matches Found')
            elif len(mnemonic_query_list) == 1:
                correct_courses = all_courses.filter(mnemonic=mnemonic_query_list[0])
            else:
                q = Q(mnemonic=mnemonic_query_list[0])
                for mnemonic_query in mnemonic_query_list[1:]:
                    q = q | Q(mnemonic=mnemonic_query)
                    # q = q.add(Q(mnemonic=mnemonic_query), Q.OR)

                correct_courses = all_courses.filter(q)

            course_dicts = []
            for course in correct_courses:
                # associated_sections = course.section_set.all()

                # grade_sum = 0
                # grade_counter = 0
                # for section in associated_sections:
                    # section_grade = section.grade #Grade.objects.get(pk=section.grade)
                    # grade_sum += section_grade.average_gpa
                    # grade_counter += 1

                # try:
                #     generic_course_average_gpa = round(grade_sum / grade_counter, 3)
                # except ZeroDivisionError:
                #     generic_course_average_gpa = None
                # g = Grade(average_gpa=generic_course_average_gpa)

                # course.grade = g
                # course.save()
                course_python_dict = model_to_dict(course)
                # course_python_dict['average_gpa'] = generic_course_average_gpa
                course_dicts.append(course_python_dict)


            if len(course_dicts) == 0:
                return _failure(404, 'no matches found.')

            return _success(200, {'match': course_dicts, 'query_list': mnemonic_query_list})

        # If looking for single course detail (for course detail page), associated sections
        # are needed as well!
        elif 'mnemonic' and 'number' in request.GET:
            mnemonic = request.GET.get('mnemonic')
            number = request.GET.get('number')
            try:
                course = Course.objects.get(mnemonic=mnemonic, number=number)
            except Course.DoesNotExist:
                return _failure(404, 'No matches found.')
            except Course.MultipleObjectsReturned:
                return _failure(409, 'Multiple objects found when there should only be one.')

            course_dictionary = model_to_dict(course)

            associated_sections = course.section_set.all()
            section_dicts = []
            grade_sum = 0
            grade_counter = 0
            for section in associated_sections:
                section_dict = model_to_dict(section)

                grade = section.grade
                section_dict['grade'] = model_to_dict(grade)

                try:
                    instructor = Instructor.objects.get(id=section_dict['instructor'])
                    section_dict['instructor'] = model_to_dict(instructor)
                except ObjectDoesNotExist:
                    pass

                section_dicts.append(section_dict)

                grade_sum += grade.average_gpa
                grade_counter += 1

            try:
                generic_course_average_gpa = round(grade_sum / grade_counter, 3)
            except ZeroDivisionError:
                generic_course_average_gpa = None

            course_dictionary['average_gpa'] = generic_course_average_gpa

            course_dictionary['sections'] = section_dicts
            return _success(200, {'match': course_dictionary})

        # Tong's normal code
        else:
            resp = super().get(request, *args, **kwargs)
            resp_dict = json.loads(resp.content.decode('utf-8'))
            if resp_dict['status_code'] != 200:
                return resp
            resp_dict.pop('status_code', None)

            # for obj_dict in resp_dict['match']:
            #     obj = Grade.objects.get(id=obj_dict['grade'])
            #     obj_dict['grade'] = model_to_dict(obj)
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


class SectionView(BaseView):
    model = Section
    form = SectionForm

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        if resp_dict['status_code'] != 200: return resp
        resp_dict.pop('status_code', None)

        for obj_dict in resp_dict['match']:
            try:
                grade = Grade.objects.get(id=obj_dict['grade'])
                instructor = Instructor.objects.get(id=obj_dict['instructor'])
            except (Grade.DoesNotExist, Instructor.DoesNotExist):
                continue

            obj_dict['grade'] = model_to_dict(grade)
            obj_dict['instructor'] = model_to_dict(instructor)

        return _success(200, resp_dict)

class InstructorView(BaseView):
    model = Instructor
    form = InstructorForm

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        if resp_dict['status_code'] != 200: return resp
        resp_dict.pop('status_code', None)

        for instructor_dict in resp_dict['match']:
            try:
                ins = Instructor.objects.get(id=instructor_dict['id'])
                sections_taught = ins.section_set.all()
                sections_taught_dicts = []
                for section in sections_taught:
                    section_dict = model_to_dict(section)
                    try:
                        grade = Grade.objects.get(id=section_dict['grade'])
                        grade_dict = model_to_dict(grade)
                        section_dict['grade'] = grade_dict
                    except:
                        pass

                    sections_taught_dicts.append(section_dict)

                if sections_taught_dicts:
                    instructor_dict['instructor_sections'] = sections_taught_dicts
            except:
                continue

        return _success(200, resp_dict)