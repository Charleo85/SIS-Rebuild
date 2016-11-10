from django.test import TestCase, RequestFactory
import json

from . import views_model, views_auth


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
        resp_data = json.loads(response.context, safe=False)

        self.assertEqual(resp_data['status_code'], 200)
