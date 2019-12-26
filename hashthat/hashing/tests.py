import hashlib

from django.test import TestCase
from selenium import webdriver

from .forms import HashForm
from .models import Hash

helloHash = '2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824'.lower()

# class can be any name
# class FunctionalTestCase(TestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     # use descriptive names for tests; MUST start with test_
#     def test_there_is_homepage(self):
#         self.browser.get('http://localhost:8000')
#         self.assertIn('Enter text here', self.browser.page_source)

#     def test_hash_of_hello(self):
#         self.browser.get('http://localhost:8000')
#         text = self.browser.find_element_by_id('id_text')
#         text.send_keys('hello')
#         self.browser.find_element_by_name('submit').click()
#         self.assertIn(helloHash, self.browser.page_source)


#     def tearDown(self):
#         self.browser.quit()


class UnitTestCase(TestCase):
    
    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')
    
    def test_hash_form(self):
        form = HashForm(data={'text': 'hello', 'algo': 'sha256'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual(text_hash, helloHash)

    def test_hash_object(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = helloHash
        hash.save()
        pulled_hash = Hash.objects.get(hash=helloHash)
        self.assertEqual(hash.text, pulled_hash.text)
