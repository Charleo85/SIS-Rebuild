from django.forms import ModelForm, TextInput
from .models import *

class CourseForm(ModelForm):
    def clean_mnemonic(self):
        return self.cleaned_data['mnemonic'].upper()

    class Meta:
        model = Course
        fields = '__all__'
        widgets = { 'instructor': TextInput() }
        labels = { 'instructor': 'Instructor ID' }

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ('taking_courses',)

class InstructorForm(ModelForm):
    class Meta:
        model = Instructor
        fields = '__all__'

class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
