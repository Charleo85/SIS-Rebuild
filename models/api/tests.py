from django.test import TestCase
import django.db
from .models import *

# student creating and updating profile
class StudentProfileTestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        student = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
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


# class ModelCreationTestCases(TestCase):
#     fixtures = ['data.json']
#
#     def setUp(self):
#         instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
#         instructor1.save()
#         student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
#         student1.save()
#         course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor=Instructor.objects.get(id="gr3e"), max_students=135)
#         course1.save()
#         enrollment1 = Enrollment(student=Student.objects.get(id="sg4fc"), course=Course.objects.get(id=16947), enroll_status="E")
#         enrollment1.save()
#
#     def test_InstructorCreated(self):
#         newInstructor = Instructor.objects.get(id="gr3e")
#         self.assertEqual(newInstructor.__str__(), 'Gabriel Robins (gr3e)')
#
#     def test_StudentCreated(self):
#         newStudent = Student.objects.get(id="sg4fc")
#         self.assertEqual(newStudent.__str__(), "Scott Gilb (sg4fc)")
#
#     def test_CourseCreated(self):
#         newCourse = Course.objects.get(id=16947)
#         self.assertEqual(newCourse.__str__(), "CS 3102")
#
#     def test_EnrollmentCreated(self):
#         newEnrollment = Enrollment.objects.get(student="sg4fc")
#         self.assertEqual(newEnrollment.course, Course.objects.get(id=16947))
#
#
# class ModelModificationTestCases(TestCase):
#     fixtures = ['data.json']
#
#     def setUp(self):
#         instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
#         instructor1.save()
#         student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
#         student1.save()
#         course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor=Instructor.objects.get(id="gr3e"), max_students=135)
#         course1.save()
#         enrollment1 = Enrollment(student=Student.objects.get(id="sg4fc"), course=Course.objects.get(id=16947), enroll_status="E")
#         enrollment1.save()
#
#     def test_modifyStudent(self):
#         studentToModify = Student.objects.get(id="zaf2xk")
#         studentToModify.first_name = "Scotty"
#         studentToModify.save()
#         self.assertEqual(Student.objects.get(id="zaf2xk").__str__(), "Scotty Faieq (zaf2xk)")
#
#     def test_modifyInstructor(self):
#         instructorToModify = Instructor.objects.get(id="gr3e")
#         instructorToModify.first_name = "Gabe"
#         instructorToModify.save()
#         self.assertEqual(Instructor.objects.get(id="gr3e").__str__(), "Gabe Robins (gr3e)")
#
#     def test_modifyEnrollment(self):
#         enrollmentToModify = Enrollment.objects.get(student=Student.objects.get(id="sg4fc"))
#         enrollmentToModify.course=Course.objects.get(id=17894)
#         enrollmentToModify.save()
#         self.assertEqual(Enrollment.objects.get(student=Student.objects.get(id="sg4fc")).course, Course.objects.get(id=17894))
#
#     def test_modifyCourse(self):
#         courseToModify = Course.objects.get(id="16947")
#         courseToModify.max_students = 150
#         courseToModify.save()
#         self.assertEqual(Course.objects.get(id="16947").max_students, 150)
#
#
# class TestCasesToInsureDuplicateIDsAreNotAllowed(TestCase):
#     fixtures = ['data.json']
#
#     def setUp(self):
#         instructor1 = Instructor(first_name="Gabriel", last_name="Robins", id="gr3e")
#         instructor1.save()
#         student1 = Student(first_name="Scott", last_name="Gilb", id="sg4fc")
#         student1.save()
#         course1 = Course(mnemonic="CS", number="3102", section="001", id=16947, instructor=Instructor.objects.get(id="gr3e"), max_students=135)
#         course1.save()
#         enrollment1 = Enrollment(student=Student.objects.get(id="sg4fc"), course=Course.objects.get(id=16947), enroll_status="E")
#         enrollment1.save()
#
#     def test_DuplicateStudentCheck(self):
#         studentDuplicate = Student.objects.get(id="sg4fc")
#         studentDuplicate.id = "zaf2xk"
#         studentDuplicate.save()
#         studentList = Student.objects.all()
#         for student in studentList:
#             if student != studentDuplicate:
#                 self.assertNotEqual(student.id, "zaf2xk")
#
#
#     def test_DuplicateInstructorCheck(self):
#         instructorDuplicate = Instructor.objects.get(id="gr3e")
#         instructorDuplicate.id = "tp3ks"
#         instructorDuplicate.save()
#         instructorList = Instructor.objects.all()
#         for instructor in instructorList:
#             if instructor != instructorDuplicate:
#                 self.assertNotEqual(instructor.id, "tp3ks")
#
#     def test_DuplicateCourseCheck(self):
#         courseDuplicate = Course.objects.get(id=16947)
#         courseDuplicate.id = 17894
#         courseDuplicate.save()
#         courseList = Course.objects.all()
#         for course in courseList:
#             if course != courseDuplicate:
#                 self.assertNotEqual(course.id, 17894)
