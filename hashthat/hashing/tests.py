from django.test import TestCase
from selenium import webdriver

# class can be any name
class FunctionalTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    # use descriptive names for tests
    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('install', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()

