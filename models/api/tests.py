from django.test import TestCase
import django.db
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


class ModelModificationTestCases(TestCase):
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

    def test_modifyStudent(self):
        studentToModify = Student.objects.get(id="sg4fc")
        studentToModify.first_name = "Scotty"
        studentToModify.save()
        self.assertEqual(Student.objects.get(id="sg4fc").__str__(), "Scotty Gilb (sg4fc)")

    def test_modifyInstructor(self):
        instructorToModify = Instructor.objects.get(id="gr3e")
        instructorToModify.first_name = "Gabe"
        instructorToModify.save()
        self.assertEqual(Instructor.objects.get(id="gr3e").__str__(), "Gabe Robins (gr3e)")

    def test_modifyEnrollment(self):
        enrollmentToModify = Enrollment.objects.get(student=Student.objects.get(id="sg4fc"))
        enrollmentToModify.course=Course.objects.get(id=17894)
        enrollmentToModify.save()
        self.assertEqual(Enrollment.objects.get(student=Student.objects.get(id="sg4fc")).course, Course.objects.get(id=17894))

    def test_modifyCourse(self):
        courseToModify = Course.objects.get(id="16947")
        courseToModify.max_students = 150
        courseToModify.save()
        self.assertEqual(Course.objects.get(id="16947").max_students, 150)


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
        try:
            studentDuplicate.save()
        except django.db.IntegrityError:
            raise AssertionError

    def test_DuplicateInstructorCheck(self):
        instructorDuplicate = Instructor.objects.get(id="gr3e")
        instructorDuplicate.id = "tp3ks"
        try:
            instructorDuplicate.save()
        except django.db.IntegrityError:
            raise AssertionError

    def test_DuplicateCourseCheck(self):
        courseDuplicate = Course.objects.get(id=16947)
        courseDuplicate.id = 17894
        try:
            courseDuplicate.save()
        except django.db.IntegrityError:
            raise AssertionError

"""
class TestCasesToInsureAllForeignKeyFieldDataIsInDatabase(TestCase):
    fixtures = ['data.json']

class TestCasesGETandPOST(TestCase):
    #Do I need this?
"""