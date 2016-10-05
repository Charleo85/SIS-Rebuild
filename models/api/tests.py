from django.test import TestCase
from .models import Instructor, Profile, Course, Student, Enrollment

class ModelCreationTestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
        instructor1.save()
        student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
        student1.save()
        #course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor="gr3e", max_students=135)
        #course1.save()
        #enrollment1 = Enrollment(student="sg4fc", course=16947, enroll_status="E")
        #enrollment1.save()

    def test_InstructorCreated(self):
        newInstructor = Instructor.objects.get(id="gr3e")
        self.assertEqual(newInstructor.__str__(), 'Gabriel Robins (gr3e)')

    def test_StudentCreated(self):
        newStudent = Student.objects.get(id="sg4fc")
        self.assertEqual(newStudent.__str__(), "Scott Gilb (sg4fc)")

    #def test_CourseCreated(self):

    #def test_EnrollmentCreated(self):
"""
class ModelModificationTestCases(TestCase):
    fixtures = ['data.json']

    def test_modifyStudent(self):

    def test_modifyInstructor(self):

    def test_modifyEnrollment(self):

    def test_modifyCourse(self):

class TestCasesToInsureDuplicateIDsAreNotAllowed(TestCase):
    fixtures = ['data.json']

    def test_DuplicateStudentCheck(self):

    def test_DuplicateInstructorCheck(self):

    def test_DuplicateCourseCheck(self):

class TestCasesToInsureAllForeignKeyFieldDataIsInDatabase(TestCase):
    fixtures = ['data.json']

class TestCasesGETandPOST(TestCase):
    #Do I need this?
"""