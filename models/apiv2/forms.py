from django.forms import ModelForm, TextInput, NumberInput
from django.contrib.auth import hashers

from .models import *


# class CourseForm(ModelForm):
#     def clean_mnemonic(self):
#         return self.cleaned_data['mnemonic'].upper()
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#         widgets = { 'instructor': TextInput() }
#         labels = { 'instructor': 'Instructor ID' }
#
#
# class StudentForm(ModelForm):
#     class Meta:
#         model = Student
#         exclude = ('taking_courses',)
#
#     def clean_password(self):
#         pw = self.cleaned_data['password']
#         pw = hashers.make_password(pw)
#         return pw
#
#
# class InstructorForm(ModelForm):
#     class Meta:
#         model = Instructor
#         fields = '__all__'
#
#     def clean_password(self):
#         pw = self.cleaned_data['password']
#         pw = hashers.make_password(pw)
#         return pw
#
#
# class EnrollmentForm(ModelForm):
#     class Meta:
#         model = Enrollment
#         fields = '__all__'
#         widgets = {
#             'student': TextInput(),
#             'course':  TextInput(),
#         }
#         labels = {
#             'student': 'Student ID',
#             'course': 'Course SIS ID',
#         }
