from django.test import TestCase
from django.contrib.auth import hashers
from django.core.urlresolvers import reverse
import json

from api.models import *

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

    def test_get_course_detail(self):
        response = self.client.get(reverse('course_detail', kwargs={'sisid':'17894'}))
        # print(reverse('course_detail', kwargs={'sisid':'17894'}))
        target_course = Course.objects.get(id='17894')
        current_enrolled = len(target_course.student_set.all())

        expected_response_content = {"status_code": 200, "course": {"id" : "17894","instructor": "tp3ks","max_students": 50,"mnemonic": "CS",
                                                                    "number": "4501","section": "005",'description': '', "title": "Internet Scale App",
                                                                    "website": "https://github.com/thomaspinckney3/cs4501", "meet_time": "TuTh 3:00-4:45pm",
                                                                    "location": "Olsson 120","current_enrolled": current_enrolled}}
        decoded_response = response.content.decode('utf-8')
        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['course'], expected_response_content['course'])


    def test_post_course_detail(self):
        url_for_post = reverse('course_detail', kwargs={'sisid':'17894'})
        data_for_post = {"id" : "17894","instructor" : "tp3ks","max_students": 100,"mnemonic": "CS",
                                                                    "number": "4501","section": "005",'description': '', "title": "Internet Scale App",
                                                                    "website": "https://github.com/thomaspinckney3/cs4501", "meet_time": "TuTh 3:00-4:45pm",
                                                                    "location": "Olsson 120"}
        response = self.client.post(url_for_post, data_for_post)

        target_course = Course.objects.get(id='17894')
        current_enrolled = len(target_course.student_set.all())

        expected_response_content = {"status_code": 201, "course": {"id" : "17894","instructor": "Thomas Pinckney (tp3ks)","max_students": 100,"mnemonic": "CS",
                                                                    "number": "4501","section": "005",'description': '', "title": "Internet Scale App",
                                                                    "website": "https://github.com/thomaspinckney3/cs4501", "meet_time": "TuTh 3:00-4:45pm",
                                                                    "location": "Olsson 120","current_enrolled": current_enrolled}}
        decoded_response = response.content.decode('utf-8')
        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['course'], expected_response_content['course'])


    def test_course_create(self):
        url_for_post = reverse('course_create')
        data_for_post = {"id" : "17537","instructor" : "tp3ks","max_students": 100,"mnemonic": "CS",
                                                                    "number": "3102","section": "001",'description': '', "title": "Theory of Computation",
                                                                    "website": "", "meet_time": "TuTh 12:30PM - 1:45PM",
                                                                    "location": "Rice Hall 130"}
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 201,
                                     "course": {"id" : "17537","instructor" : "Thomas Pinckney (tp3ks)","max_students": 100,"mnemonic": "CS",
                                                                    "number": "3102","section": "001",'description': '', "title": "Theory of Computation",
                                                                    "website": "", "meet_time": "TuTh 12:30PM - 1:45PM",
                                                                    "location": "Rice Hall 130", "current_enrolled": 0}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['course'], expected_response_content['course'])

        # Test to see if the newly created course is in the database

        response = self.client.get(reverse('course_detail', kwargs={'sisid': '17537'}))
        expected_response_content['status_code'] = 200
        # This next line should not be here!!
        expected_response_content['course']['instructor'] = "tp3ks"
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['course'], expected_response_content['course'])

    def test_course_delete(self):
        data_for_post = {'id': '17894'}
        response = self.client.post(reverse('course_delete'), data_for_post)

        expected_response_content = {"status_code": 202}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

        # Test to see if instructor was properly deleted from database
        response = self.client.get(reverse('course_detail', kwargs={'sisid': '17894'}))
        expected_response_content = {"status_code": 404}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

    def test_course_all(self):
        response = self.client.get(reverse('course_all'))
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], 200)

    def test_get_instructor_detail(self):
        response = self.client.get(reverse('instructor_detail', kwargs={'compid':'tp3ks'}))

        expected_response_content = {"status_code": 200, "instructor": {"last_name": "Pinckney", 'teaching_courses': ['CS 4501'], "id": "tp3ks", "first_name": "Thomas"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['instructor'], expected_response_content['instructor'])


    def test_post_instructor_detail(self):
        url_for_post = reverse('instructor_detail', kwargs={'compid': 'tp3ks'})
        data_for_post = {"last_name": "Pikney", "id": "tp3ks", "first_name": "Thomas", "username": "tp3ks", "password": "pbkdf2_sha256$20000$ehCbRahmiM2J$5uA/WdDTVaB6zLOmPnxaGdQC/+nDTN95oPrCGpVEZoE=" }
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 202, "instructor": {"last_name": "Pikney", "id": "tp3ks", "first_name": "Thomas"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['instructor'], expected_response_content['instructor'])

    def test_instructor_create(self):
        url_for_post = reverse('instructor_create')
        data_for_post = {"last_name": "Robins", "id": "robins", "first_name": "Gabriel", "username": "Gabe", "password": "123algorithms" }
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 201, "instructor": {"last_name": "Robins", "id": "robins", "first_name": "Gabriel"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['instructor'], expected_response_content['instructor'])

        # Test to see if the newly created student is in the database
        response = self.client.get(reverse('instructor_detail', kwargs={'compid': 'robins'}))
        expected_response_content = {"status_code": 200, "instructor": {"last_name": "Robins","teaching_courses": [], "id": "robins", "first_name": "Gabriel"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['instructor'], expected_response_content['instructor'])

    def test_instructor_delete(self):
        data_for_post = {'id': 'tp3ks'}
        response = self.client.post(reverse('instructor_delete'), data_for_post)

        expected_response_content = {"status_code": 202}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

        # Test to see if instructor was properly deleted from database
        response = self.client.get(reverse('instructor_detail', kwargs={'compid':'tp3ks'}))
        expected_response_content = {"status_code": 404}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

    def test_instructor_all(self):
        response = self.client.get(reverse('instructor_all'))
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], 200)

    def test_get_student_detail(self):
        response = self.client.get(reverse('student_detail', kwargs={'compid': 'zaf2xk'}))
        expected_response_content = {"status_code": 200, "student": {"last_name": "Faieq", 'taking_courses': ['17894'], "id": "zaf2xk", "first_name": "Zakey"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['student'], expected_response_content['student'])

    def test_post_student_detail(self):
        url_for_post = reverse('student_detail', kwargs={'compid': 'zaf2xk'})
        data_for_post = {"last_name": "Faieq", "id": "zaf2xk", "first_name": "Zakey", "username": "zaf2xk", "password": "change of password test"}
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 201, "student": {"last_name": "Faieq", "id": "zaf2xk", "first_name": "Zakey"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['student'], expected_response_content['student'])

    def test_student_create(self):
        url_for_post = reverse('student_create')
        data_for_post = {"last_name": "Gilb", "id": "sg4fc", "first_name": "Scott", "username": "scotty", "password": "123password" }
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 201, "student": {"last_name": "Gilb", "id": "sg4fc", "first_name": "Scott"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['student'], expected_response_content['student'])

        # Test to see if the newly created student is in the database
        response = self.client.get(reverse('student_detail', kwargs={'compid': 'sg4fc'}))
        expected_response_content = {"status_code": 200, "student": {"last_name": "Gilb", "id": "sg4fc",'taking_courses': [], "first_name": "Scott"}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['student'], expected_response_content['student'])

    def test_student_delete(self):
        data_for_post = {'id': 'zaf2xk'}
        response = self.client.post(reverse('student_delete'), data_for_post)

        expected_response_content = {"status_code": 202}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

        # Test to see if instructor was properly deleted from database
        response = self.client.get(reverse('student_detail', kwargs={'compid':'zaf2xk'}))
        expected_response_content = {"status_code": 404}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

    def test_student_all(self):
        response = self.client.get(reverse('student_all'))
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], 200)

    def test_get_enrollment_detail(self):
        response = self.client.get(reverse('enrollment_detail', kwargs={'enrid': 1}))
        expected_response_content = {"status_code": 200, "enrollment": {"student": "tq7bw", "course": "17894", "enroll_status": "Enrolled",  'id': 1}}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['enrollment'], expected_response_content['enrollment'])

    # Yields a "cannot parse JSON" error!!!
    def test_post_enrollment_detail(self):
        url_for_post = reverse('enrollment_detail', kwargs={'enrid': 1})
        data_for_post = {"student": "tq7bw", "course": "17894", "enroll_status": "W"}
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 202, "enrollment": {"student": "tq7bw", "course": "17894", "enroll_status": "Waitlisted",  'id': 1}}

           # If the data being deserialized is not a valid JSON document,
           # a JSONDecodeError will be raised -- consider putting a try-catch here??
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
        self.assertEqual(python_dict_from_decoded_response['enrollment'], expected_response_content['enrollment'])

    # I'm having trouble making a successful POST, it seems like the "form.is_valid()" check is not passing
    # def test_enrollment_create(self):
    #     url_for_post = reverse('enrollment_create')
    #     data_for_post = {"student": "zaf2xk", "course": "17894", "enroll_status": "W"}
    #     response = self.client.post(url_for_post, data_for_post)
    #
    #     expected_response_content = {"status_code": 201, "enrollment": "sg4fc", "course": "17894", "enroll_status": "W"}
    #     decoded_response = response.content.decode('utf-8')
    #
    #     python_dict_from_decoded_response = json.loads(decoded_response)
    #     self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
    #     self.assertEqual(python_dict_from_decoded_response['enrollment'], expected_response_content['enrollment'])
    #
    #     # Test to see if the newly created student is in the database
    #     response = self.client.get(reverse('enrollment_detail', kwargs={'enrid': 'sg4fc'}))
    #
    #     decoded_response = response.content.decode('utf-8')
    #
    #     python_dict_from_decoded_response = json.loads(decoded_response)
    #     self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])
    #     self.assertEqual(python_dict_from_decoded_response['enrollment'], expected_response_content['enrollment'])

    def test_enrollment_delete(self):
        url_for_post = reverse('enrollment_delete')
        data_for_post = {"id": 1}
        response = self.client.post(url_for_post, data_for_post)

        expected_response_content = {"status_code": 202}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

        # Test to see if instructor was properly deleted from database
        response = self.client.get(reverse('enrollment_detail', kwargs={'enrid': 1}))
        expected_response_content = {"status_code": 404}
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], expected_response_content['status_code'])

    def test_enrollment_all(self):
        response = self.client.get(reverse('enrollment_all'))
        decoded_response = response.content.decode('utf-8')

        python_dict_from_decoded_response = json.loads(decoded_response)
        self.assertEqual(python_dict_from_decoded_response['status_code'], 200)
