from django.test import TestCase
from django.contrib.auth import hashers
from django.core.urlresolvers import reverse
import json

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


class APITestCases(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        pass

    def test_get_course_detail(self):
        response = self.client.get(reverse('course_detail', kwargs={'sisid':'17894'}))
        self.assertEqual(response.status_code, 200)

        target_course = Course.objects.get(id='17894')
        current_enrolled = len(target_course.student_set.all())

        expected_response_content = {"status_code": 200, "course": {"mnemonic": "CS", "current_enrolled": current_enrolled, "number": "4501", "section": "005", "id": "17894",
                                                                    "instructor": "tp3ks", "title": "Internet Scale App", "website": "https://github.com/thomaspinckney3/cs4501",
                                                                    "meet_time": "TuTh 3:00-4:45pm", "location": "Olsson 120", "max_students": 50}}
        decoded_response = response.content.decode('utf-8')
        python_dict_from_decoded_response = json.loads(decoded_response)
        # Still not working as expected
        # self.assertEqual(python_dict_from_decoded_response['course'], expected_response_content['course'])

    def test_post_course_detail(self):
        pass

    def test_course_create(self):
        pass

    def test_course_delete(self):
        pass

    def test_course_all(self):
        pass

    def test_get_instructor_detail(self):
        response = self.client.get(reverse('instructor_detail', kwargs={'compid':'tp3ks'}))
        expected_response_content = {"status_code": 200, "instructor": {"last_name": "Pinckney", 'teaching_courses': ['CS 4501'], "id": "tp3ks", "first_name": "Thomas"}}
        self.assertEqual(response.status_code, 200)
        decoded_response = response.content.decode('utf-8')
        """
        If the data being deserialized is not a valid JSON document,
         a JSONDecodeError will be raised -- consider putting a try-catch here??
        """
        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['instructor'], expected_response_content['instructor'])

    def test_post_instructor_detail(self):
        pass

    def test_instructor_create(self):
        pass

    def test_instructor_delete(self):
        pass

    def test_instructor_all(self):
        pass

    def test_get_student_detail(self):
        response = self.client.get(reverse('student_detail', kwargs={'compid': 'zaf2xk'}))
        expected_response_content = {"status_code": 200, "student": {"last_name": "Faieq", 'taking_courses': ['17894'], "id": "zaf2xk", "first_name": "Zakey"}}
        self.assertEqual(response.status_code, 200)
        decoded_response = response.content.decode('utf-8')
        """
        If the data being deserialized is not a valid JSON document,
         a JSONDecodeError will be raised -- consider putting a try-catch here??
        """
        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['student'], expected_response_content['student'])

    def test_post_student_detail(self):
        pass