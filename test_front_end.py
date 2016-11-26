from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import unittest
import urllib.request, urllib.parse

global driver
driver = webdriver.Chrome('./chromedriver')

# Project 3 related: homepage, item listings, and item details
class BasicTestCase(unittest.TestCase):
    def test_home_page(self):
        driver.get("http://127.0.0.1/")
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'SIS-REBUILD')

        popular = driver.find_element_by_id('popular')
        driver.execute_script('return arguments[0].scrollIntoView();',popular)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'tp3ks'))
            )
        finally:
            ins = driver.find_element_by_partial_link_text('Thomas Pinckney')
            href = 'http://127.0.0.1/instructor/detail/tp3ks/'
            self.assertEqual(ins.get_attribute('href'), href)

    def test_course_list(self):
        driver.get("http://127.0.0.1/course/")
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'List of All Courses')

        cs1110 = driver.find_element_by_partial_link_text('CS 1110 - 001')
        self.assertIn('Introduction to Programming', cs1110.text)
        cs1110.click()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'CS 1110')
        detail_list = driver.find_elements_by_class_name('list-group-item')
        for item in detail_list:
            if 'id' in item.text:
                self.assertIn('17513', item.text)
            if 'title' in item.text:
                self.assertIn('Introduction to Programming', item.text)

    def test_instructor_list(self):
        driver.get("http://127.0.0.1/instructor/")
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'List of All Instructors')

        asb = driver.find_element_by_partial_link_text('asb2t')
        self.assertIn('Aaron Bloomfield', asb.text)
        asb.click()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Instructor: Aaron Bloomfield')
        detail_list = driver.find_elements_by_class_name('list-group-item')
        for item in detail_list:
            if 'id' in item.text:
                self.assertIn('asb2t', item.text)
            if 'last name' in item.text:
                self.assertIn('Bloomfield', item.text)

# Project 4 related: user authentication / create user
class UserAuthTestCase(unittest.TestCase):
    def test_login(self):
        driver.get('http://127.0.0.1/student/login/')
        driver.find_element_by_name('username').send_keys('tq7bw')
        driver.find_element_by_name('password').send_keys('tonyqiu')
        driver.find_element_by_class_name('btn-block').click()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Welcome, Tong')
        detail_list = driver.find_elements_by_class_name('list-group-item')
        for item in detail_list:
            if 'id' in item.text or 'username' in item.text:
                self.assertIn('tq7bw', item.text)

        driver.find_element_by_partial_link_text('logout').click()
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Thank you!')

    def test_signup(self):
        driver.get('http://127.0.0.1/instructor/signup/')
        driver.find_element_by_name('username').send_keys('james')
        driver.find_element_by_name('id').send_keys('jc7y')
        driver.find_element_by_partial_link_text('Credential').click()
        driver.find_element_by_name('password').send_keys('jimcargile')
        driver.find_element_by_name('password_again').send_keys('jimcargile')
        driver.find_element_by_partial_link_text('Profile').click()
        driver.find_element_by_name('first_name').send_keys('James')
        driver.find_element_by_name('last_name').send_keys('Cargile')
        driver.find_element_by_class_name('form-signin').submit()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Congratulations!')
        driver.find_element_by_partial_link_text('login').click()

        driver.find_element_by_name('username').send_keys('james')
        driver.find_element_by_name('password').send_keys('jimcargile')
        driver.find_element_by_class_name('btn-block').click()
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Welcome, James')
        driver.find_element_by_partial_link_text('logout').click()

# Project 4 & 5 related: create listing (course)
class CreateInstanceTestCase(unittest.TestCase):
    def setUp(self):
        driver.get('http://127.0.0.1/instructor/login/')
        driver.find_element_by_name('username').send_keys('tp3ks')
        driver.find_element_by_name('password').send_keys('thomas')
        driver.find_element_by_class_name('btn-block').click()

    def test_course_create(self):
        driver.get('http://127.0.0.1/course/create/')
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Create a New Course')

        driver.find_element_by_name('mnemonic').send_keys('CS')
        driver.find_element_by_name('number').send_keys('1000')
        driver.find_element_by_name('id').send_keys('10000')
        driver.find_element_by_name('instructor').send_keys('tp3ks')
        driver.find_element_by_name('max_students').send_keys('100')
        driver.find_element_by_name('title').send_keys('Test')
        driver.find_element_by_name('section').send_keys('001')

        driver.find_element_by_class_name('btn-block').click()
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'CS 1000')
        detail_list = driver.find_elements_by_class_name('list-group-item')
        for item in detail_list:
            if 'id' in item.text:
                self.assertIn('10000', item.text)
            if 'title' in item.text:
                self.assertIn('Test', item.text)

    def tearDown(self):
        driver.get('http://127.0.0.1/instructor/profile/')
        driver.find_element_by_partial_link_text('logout').click()

# Project 5 related: search functionality
class SearchTestCase(unittest.TestCase):
    def test_general_search(self):
        driver.get('http://127.0.0.1/search/')
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Search Page')

        driver.find_element_by_id('id_search_query').send_keys('tp3ks')
        select = Select(driver.find_element_by_name('query_specifier'))
        select.select_by_value('general')
        driver.find_element_by_class_name('btn-block').click()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Search Results')
        p_tags = driver.find_elements_by_tag_name('p')
        self.assertGreater(len(p_tags), 1)

        cs4501 = driver.find_element_by_partial_link_text('Special Topics')
        self.assertIn('Thomas Pinckney', cs4501.text)
        tp3ks = driver.find_element_by_partial_link_text('tp3ks')
        self.assertIn('Thomas Pinckney', tp3ks.text)

    def test_specific_search(self):
        driver.get('http://127.0.0.1/search/')
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Search Page')

        driver.find_element_by_id('id_search_query').send_keys('tp3ks')
        select = Select(driver.find_element_by_name('query_specifier'))
        select.select_by_value('instructor')
        driver.find_element_by_class_name('btn-block').click()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Search Results')
        p_tags = driver.find_elements_by_tag_name('p')
        self.assertEqual(len(p_tags), 1)
        tp3ks = driver.find_element_by_partial_link_text('tp3ks')
        self.assertIn('Thomas Pinckney', tp3ks.text)

    def test_search_bar(self):
        driver.get('http://127.0.0.1/')
        driver.find_element_by_name('search_query').send_keys('tp3ks')
        driver.find_element_by_class_name('navbar-form').submit()

        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'Search Results')
        p_tags = driver.find_elements_by_tag_name('p')
        self.assertGreater(len(p_tags), 1)

if __name__ == '__main__': # invoke the unittests from command line
    unittest.main()
