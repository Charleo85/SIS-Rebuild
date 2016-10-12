from django.test import TestCase
from django.contrib.auth import hashers
import django.db

from .models import *

# student creating and updating profile
class StudentProfileTestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        student = Student(
            first_name="Scott", last_name="Gilb", id="sg4fc",
            username="sg4fc", password=hashers.make_password("scottgilb")
        )
        student.save()

    def test_StudentCreated(self):
        student = Student.objects.get(id="sg4fc")
        self.assertEqual(student.__str__(), "Scott Gilb (sg4fc)")

    def test_StudentUpdateProfile(self):
        student = Student.objects.get(id="sg4fc")
        student.first_name = "scotty"
        student.last_name = "gilb"
        student.save()
        self.assertEqual(student.__str__(), "scotty gilb (sg4fc)")

# student modifying enrollment info
class StudentEnrollmentTestCases(TestCase):
    fixtures = ['data.json']

    def test_ChangeEnrollmentStatus(self):
        enrollment = Enrollment.objects.get(student="tq7bw", course="17894")
        enrollment.enroll_status = "W"
        enrollment.save()
        testing_enrollment = Enrollment.objects.get(student="tq7bw", course="17894")
        self.assertEqual(testing_enrollment.enroll_status, "W")

    def test_EnrollInCourse(self):
        student = Student.objects.get(id="tq7bw")
        course = Course.objects.get(id="16976")
        enrollment = Enrollment(student=student, course=course, enroll_status="E")
        enrollment.save()
        testing_student = Student.objects.get(id="tq7bw")
        self.assertEqual(
            testing_student.taking_courses.get(id="16976"),
            Course.objects.get(id="16976")
        )

# instructor create and update course
class CreateAndModifyCourseTestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        course = Course(
            id="17615", mnemonic="CS", number="4970", max_students=150,
            instructor=Instructor.objects.get(id="asb2t"),
            section="001", title="Capstone Practicum",
        )
        course.save()

    def test_CourseCreated(self):
        course = Course.objects.get(id="17615")
        self.assertEqual(course.mnemonic, "CS")
        self.assertEqual(course.number, "4970")

    def test_ModifyCourseInfo(self):
        course = Course.objects.get(id="17615")
        course.title = "Capstone Practicum I"
        course.max_students = 120
        course.save()
        testing_course = Course.objects.get(id="17615")
        self.assertEqual(testing_course.title, "Capstone Practicum I")
        self.assertEqual(testing_course.max_students, 120)

# admin modify student's enrollment
class AdministratorTestCase(TestCase):
    fixtures = ['data.json']

    def test_DeleteEnrollment(self):
        enrollment = Enrollment.objects.filter(student="jw7jb", course="16976")
        enrollment.delete()
        student = Student.objects.get(id="jw7jb")
        for c in student.taking_courses.all():
            self.assertNotEqual(c.id, "16976")

# general user view course info
class GeneralUserTestCase(TestCase):
    fixtures = ['data.json']

    def test_CourseLookUp(self):
        mnemonic = "MATH"
        number = "5653"
        course = Course.objects.get(mnemonic=mnemonic, number=number)
        self.assertEqual(course.title, "Number Theory")
