from django.test import TestCase, RequestFactory
from elasticsearch import Elasticsearch
import json, time

from . import views_model, views_auth


"""
User story #1: A client can search any keyword, using different query
specifiers (i.e. general, or specific model name). The general index
should include results from all models.
"""
class SearchTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_general_search(self):
        post_data = {
            'search_query': 'tp3ks',
            'query_specifier': 'general',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 2)

    def test_course_search(self):
        post_data = {
            'search_query': 'tp3ks',
            'query_specifier': 'course',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 1)
        self.assertEqual(resp_data['hits'][0]['model'], 'api.Course')
        label = 'CS 4501: Special Topics in Computer Science (Thomas Pinckney)'
        self.assertEqual(resp_data['hits'][0]['label'], label)

    def test_instructor_search(self):
        post_data = {
            'search_query': 'tp3ks',
            'query_specifier': 'instructor',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 1)
        self.assertEqual(resp_data['hits'][0]['model'], 'api.Instructor')
        ins_label = 'Thomas Pinckney (tp3ks)'
        self.assertEqual(resp_data['hits'][0]['label'], ins_label)

    def test_student_search(self):
        post_data = {
            'search_query': 'tq7bw',
            'query_specifier': 'student',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 1)
        self.assertEqual(resp_data['hits'][0]['model'], 'api.Student')
        stud_label = 'Tong Qiu (tq7bw)'
        self.assertEqual(resp_data['hits'][0]['label'], stud_label)


"""
User story #2: A user, when creating an account or listing properly,
should see his new account/listing being added to the search index.
"""
class CreateAndSearchTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # create a course CS 6501
        course_data = {
            'mnemonic': 'CS',
            'number': '6501',
            'section': '008',
            'instructor': 'dee2b',
            'title': 'Understanding and Securing TLS',
            'id': '30000',
            'max_students': 30,
        }
        request = self.factory.post('/course/create/', course_data)
        views_model.course_create(request)

        # create a student yz9fy
        student_data = {
            'last_name': 'Zheng',
            'first_name': 'Ian',
            'id': 'yz9fy',
            'username': 'zeizyy',
            'password': 'cs4501',
            'password_again': 'cs4501',
        }
        request = self.factory.post('/student/signup/', student_data)
        views_auth.signup(request, 1)

        # sleeps for 30s to wait for instance creation to complete
        # this looks reaaaaaaaally stupid, but have to keep it...
        time.sleep(30)

    def tearDown(self):
        # delete both instances for testing
        url = 'http://models-api:8000/api/course/delete/'
        post_data = {'id': '30000'}
        views_model._make_post_request(url, post_data)

        url = 'http://models-api:8000/api/student/delete/'
        post_data = {'id': 'yz9fy'}
        views_model._make_post_request(url, post_data)

        # delete instances in elasticsearch
        es = Elasticsearch(['es'])
        time.sleep(5) #Sleep to let Elastic Search initialize
        try:
            es.delete(index='general_index', doc_type='listing', id='30000')      
            es.delete(index='course_index', doc_type='listing', id='30000')
            es.delete(index='general_index', doc_type='listing', id='yz9fy')
            es.delete(index='student_index', doc_type='listing', id='yz9fy')
        except:
            print("Never Mind, we are done!")
            
    def test_course_create(self):
        post_data = {
            'search_query': 'TLS',
            'query_specifier': 'course',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 1)
        self.assertEqual(resp_data['hits'][0]['model'], 'api.Course')
        c_label='CS 6501: Understanding and Securing TLS (David Evans)'
        self.assertEqual(resp_data['hits'][0]['label'], c_label)

    def test_student_create(self):
        post_data = {
            'search_query': 'ian',
            'query_specifier': 'student',
        }
        request = self.factory.post('/search/', data=post_data)
        response = views_model.search(request)
        resp_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp_data['status_code'], 200)
        self.assertEqual(resp_data['size'], 1)
        self.assertEqual(resp_data['hits'][0]['model'], 'api.Student')
        stud_label='Ian Zheng (yz9fy)'
        self.assertEqual(resp_data['hits'][0]['label'], stud_label)
