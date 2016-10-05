from django.test import TestCase
from .models import Instructor, Profile, Course, Student, Enrollment

class ModelCreationTestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
        instructor1.save()
        student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
        student1.save()
        course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor=Instructor.objects.get(id="gr3e"), max_students=135)
        course1.save()
        enrollment1 = Enrollment(student=Student.objects.get(id="sg4fc"), course=Course.objects.get(id=16947), enroll_status="E")
        enrollment1.save()

    def test_InstructorCreated(self):
        newInstructor = Instructor.objects.get(id="gr3e")
        self.assertEqual(newInstructor.__str__(), 'Gabriel Robins (gr3e)')

    def test_StudentCreated(self):
        newStudent = Student.objects.get(id="sg4fc")
        self.assertEqual(newStudent.__str__(), "Scott Gilb (sg4fc)")

    def test_CourseCreated(self):
        newCourse = Course.objects.get(id=16947)
        self.assertEqual(newCourse.__str__(), "CS 3102")

    def test_EnrollmentCreated(self):
        newEnrollment = Enrollment.objects.get(student="sg4fc")
        self.assertEqual(newEnrollment.course, Course.objects.get(id=16947))

"""
class ModelModificationTestCases(TestCase):
    fixtures = ['data.json']

    def test_modifyStudent(self):

    def test_modifyInstructor(self):

    def test_modifyEnrollment(self):

    def test_modifyCourse(self):

"""
class TestCasesToInsureDuplicateIDsAreNotAllowed(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
        instructor1.save()
        student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
        student1.save()
        course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor=Instructor.objects.get(id="gr3e"), max_students=135)
        course1.save()
        enrollment1 = Enrollment(student=Student.objects.get(id="sg4fc"), course=Course.objects.get(id=16947), enroll_status="E")
        enrollment1.save()

    def test_DuplicateStudentCheck(self):
        studentDuplicate = Student.objects.get(id="sg4fc")
        studentDuplicate.id = "zaf2xk"
        studentDuplicate.save()

    def test_DuplicateInstructorCheck(self):
        instructorDuplicate = Instructor.objects.get(id="gr3e")
        instructorDuplicate.id = "tp3ks"
        instructorDuplicate.save()

    def test_DuplicateCourseCheck(self):
        courseDuplicate = Course.objects.get(id=16947)
        courseDuplicate.id = 17894
        courseDuplicate.save()
"""
class TestCasesToInsureAllForeignKeyFieldDataIsInDatabase(TestCase):
    fixtures = ['data.json']

class TestCasesGETandPOST(TestCase):
    #Do I need this?
"""