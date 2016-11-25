from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unittest

driver = webdriver.Chrome('./chromedriver')

class BasicTestCase(unittest.TestCase):
    def test_homepage(self):
        driver.get("http://162.243.117.39")
        self.assertEqual(driver.title, 'CS4501 Project')

class CourseTestCase(unittest.TestCase):
    def test_course_list(self):
        driver.get("http://162.243.117.39/course/")
        title = driver.find_element_by_tag_name('h1')
        self.assertEqual(title.text, 'List of All Courses')

if __name__ == '__main__':
    unittest.main()

